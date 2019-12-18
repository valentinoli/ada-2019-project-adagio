# -*- coding: utf-8 -*-
"""Scripts for Emissions data loading and manipulation, i.e. generating schemas from raw data"""

import pandas as pd
import numpy as np

from scripts.helpers import load_countries_continents


def load_dic():
    # load dictionary to match categories impex/emissions categories
    fruit_veg = {}
    with open("../data/categories.txt") as f:
        for line in f:
            (key, val) = line.split("\t")
            fruit_veg[key] = val.strip("\n")
    return fruit_veg


def load_emissions():
    # load dictionary to match categories with impex categories
    fruit_veg = load_dic()

    # load global emissions data
    emissions = pd.read_excel(r"../data/food_emissions.xlsx")

    # add category column
    emissions["name"] = emissions.Name.map(fruit_veg)
    emissions.Name = emissions.Name.str.lower()
    emissions.name.fillna(emissions.Name, inplace=True)
    
    # average emissions for multiple growing methods (ie field and greenhouse)
    emissions = emissions.reset_index().groupby('name').mean().round(2).reset_index()
    
    # add honey + account for dried onions and beans
    emissions = pd.concat([emissions,pd.DataFrame({"name":['honey', 'beans_dry', 'onions_dry'], "Median":[0, 0, 0]})], ignore_index=True, sort=False)
    emissions.set_index("name", inplace=True)
    emissions.at['beans_dry', 'Median'] = emissions.loc['beans_fresh'].Median * 2.5
    emissions.at['onions_dry', 'Median'] = emissions.loc['onions_shallots_green'].Median * 2.5

    return emissions.drop("index", axis=1)

def load_tomatoes(suisse, transport, transportCO2):
    # load the different tomato emission categories for an example
    tomatoes = pd.read_excel(r"../data/food_emissions.xlsx")
    tomatoes = tomatoes[tomatoes.Name.str.startswith('Tomat')].set_index('Name')[['Median']]
    
    # processing to include shipping cost for a month's tomatoes from Spain
    tomatoes['total_consumption'] = suisse['consumption']['vegetables','tomatoes']
    tomatoes['produced_in_CH_month'] = (tomatoes['Median']*tomatoes['total_consumption'])/12
    tomatoes['imported_from_ES_month'] = tomatoes['produced_in_CH_month']+((tomatoes.total_consumption*((transport[['other_fresh_fruits_vegetables']].loc['Spain','Air traffic'].iat[0]*transportCO2['Air traffic'])+(transport[['other_fresh_fruits_vegetables']].loc['Spain','Inland waterways'].iat[0]*transportCO2['Inland waterways'])+(transport[['other_fresh_fruits_vegetables']].loc['Spain','Road traffic'].iat[0]*transportCO2['Road traffic'])+(transport[['other_fresh_fruits_vegetables']].loc['Spain','Rail traffic'].iat[0]*transportCO2['Rail traffic'])))/12)
    
    return tomatoes.drop('total_consumption', axis=1)


def add_emissions_data(suisse, emissions):
    # map the emissions data to each category in the Suisse dataframe
    
    dic = load_dic()
    suisse.reset_index(inplace=True)
    suisse['emissions_category'] = suisse['subtype'].map(dic)
    suisse.emissions_category.fillna(suisse['subtype'], inplace=True)
    suisse = pd.merge(suisse, emissions[['Median']].reset_index(), left_on='emissions_category', right_on='name').set_index(['type','subtype']).drop("name", axis=1).rename({'Median': 'median_emissions'}, axis='columns')
    
    return suisse


def production_emissions(suisse):
    # multiplies production values (kg) by the average production emissions (kg CO2-eq/kg produce)
    
    suisse['emissions_sans_transport'] = suisse['consumption'] * suisse['median_emissions']
    
    return suisse


def country_distances():
    #distance from the centre of each country to the centre of Switzerland
    
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
    geolocator = Nominatim(user_agent='adagio')
    
    countries = load_countries_continents()[["country"]]

    def find_coord(x):
        location = geolocator.geocode(x, timeout=100)
        if location != None:
            return [location.latitude, location.longitude]
        else:
            return np.nan

    countries['coord'] = countries.country.apply(find_coord)
    
    ch = geolocator.geocode("Switzerland")
    switzerland = (ch.latitude, ch.longitude)

    def find_distance(x):
        try:
            return geodesic(switzerland, tuple(x)).km
        except:
            return np.nan

    countries['distance_CH'] = countries.coord.apply(find_distance).round()
    countries.set_index('country', inplace=True)
    
    # fill in incompatible countries (same method used, but country names entered manually
    countries.at['Congo, Rep. of', 'distance_CH'] = 5315.0
    countries.at['Guinea, Equat.', 'distance_CH'] = 5011.0
    countries.at['Dominican Rep.', 'distance_CH'] = 7623.0
    countries.at['Kyrgyz, Rep.', 'distance_CH'] = 5191.0
    countries.at['Serbia/Mtnegro', 'distance_CH'] = 1050.0
    countries.at['Marshall Isl.', 'distance_CH'] = 13813.0
    countries.at['Pitcairn Isl.', 'distance_CH'] = 15626.0
    
    return countries


def transport_emissions(suisse):
    #TODO
    
    return suisse


# def estimate_emissions(domestic, emissions):
#     # define function to estimate emissions for each row
#     # NOTE this depends on the index of these two dataframes being the same,
#     # which is currently not the case... Not sure how we should resolve this, my friend regex?
    
#     def emis(food, name):
#         return food[name] * 1000000 * emissions.loc[food["Product"], "Mean"]

#     # apply this to some different columns
#     domestic["Domestic Equivalent CO2"] = domestic.apply(emis, args=["Domestic Consumption"], axis=1)
#     domestic["Imported Equivalent CO2"] = domestic.apply(emis, args=["Imported Consumption"], axis=1)
#     domestic["Total Equivalent CO2"] = domestic.apply(emis, args=["Total Consumption"], axis=1)

#     return domestic


def glimpse():
    # load data
    imported_goods = pd.read_excel("../data/nature-of-goods-imports.xlsx", skiprows=5, sheet_name="01.1")
    imported_goods.dropna(how="all",inplace=True)
    imported_goods.drop(columns=["Unnamed: 5", "Unnamed: 6", "Unnamed: 7", "Unnamed: 8"], inplace=True) #empty columns
    imported_goods.rename({"Unnamed: 0": "Year", "Unnamed: 1": "Commercial Partner"}, inplace=True, axis=1)
    imported_goods["Commercial Partner"] = imported_goods["Commercial Partner"].str.strip() # get rid of leading whitespace

    # filter for nearby countries
    nearby_countries = ["Portugal", "Spain", "France", "Germany", "Italy", "Austria", "Belgium", "Netherlands", "Czech Republic", "Slovenia", "Croatia", "Luxembourg", "Montenegro", "Serbia", "Slovakia", "Poland", "United Kingdom"]
    imported_goods_nearby = imported_goods[imported_goods["Commercial Partner"].isin(nearby_countries)].copy()

    # calculate percentage of goods imported from nearby countries
    total_nearby_imported = imported_goods_nearby["Quantity (kg)"].sum()
    return 100*total_nearby_imported/imported_goods.iloc[0][2]

