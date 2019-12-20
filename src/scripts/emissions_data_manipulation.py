# -*- coding: utf-8 -*-
"""Scripts for Emissions data loading and manipulation, i.e. generating schemas from raw data"""

import pandas as pd
import numpy as np

from scripts.impex_countries import load_countries_continents
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# constants for geolocalisation and distance calculations
geolocator = Nominatim(user_agent='adagio')
ch = geolocator.geocode("Switzerland")
switzerland = (ch.latitude, ch.longitude)
nl = geolocator.geocode("Rotterdam, Holland")
rotterdam = (nl.latitude, nl.longitude)
distance_rotterdam = geodesic(switzerland, rotterdam).km


def load_dic():
    """load dictionary to match categories impex/emissions categories"""
    fruit_veg = {}
    with open("../data/categories.txt") as f:
        for line in f:
            (key, val) = line.split("\t")
            fruit_veg[key] = val.strip("\n")
    return fruit_veg


def load_emissions():
    """load emissions tables from excel file, and match with existing food categories, account for multiple growing methods, dried foods etc."""
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


def load_tomatoes(suisse, transport, transportCO2, countries):
    """loads an example looking at different growing methods for a single product, and the effect that transport has on its carbon emissions"""
    # load the different tomato emission categories for an example
    tomatoes = pd.read_excel(r"../data/food_emissions.xlsx")
    tomatoes = tomatoes[tomatoes.Name.str.startswith('Tomat')]
    tomatoes.at[119,'Name'] = 'Tomatoes: non greenhouse'
    tomatoes = tomatoes.set_index('Name')
    
    # inherent CO2e as a result of growing method, based on one month's consumption in Switzerland
    tomatoes['total_consumption'] = suisse['consumption']['vegetables','tomatoes']
    tomatoes['produced_in_CH_month'] = (tomatoes['Median']*tomatoes['total_consumption'])/12
    
    # processing to include shipping cost for a month's tomatoes from Spain and Morocco, taking into account the various transport methods used
    tomatoes['imported_from_ES_month'] = tomatoes['produced_in_CH_month']+((tomatoes.total_consumption*((transport[['other_fresh_fruits_vegetables']].loc['Spain','Air traffic'].iat[0]*transportCO2['Air traffic']*countries['distance_CH']['Spain'])+(transport[['other_fresh_fruits_vegetables']].loc['Spain','Inland waterways'].iat[0]*transportCO2['Inland waterways']*countries['distance_CH']['Spain'])+(transport[['other_fresh_fruits_vegetables']].loc['Spain','Road traffic'].iat[0]*transportCO2['Road traffic']*countries['distance_CH']['Spain'])+(transport[['other_fresh_fruits_vegetables']].loc['Spain','Rail traffic'].iat[0]*transportCO2['Rail traffic']*countries['distance_CH']['Spain'])))/12)
    
    tomatoes['imported_from_MO_month'] = tomatoes['produced_in_CH_month']+((tomatoes.total_consumption*((transport[['other_fresh_fruits_vegetables']].loc['Morocco','Air traffic'].iat[0]*transportCO2['Air traffic']*countries['distance_CH']['Morocco'])+(transport[['other_fresh_fruits_vegetables']].loc['Morocco','Inland waterways'].iat[0]*transportCO2['Inland waterways']*countries['distance_CH']['Morocco'])+(transport[['other_fresh_fruits_vegetables']].loc['Morocco','Road traffic'].iat[0]*transportCO2['Road traffic']*countries['distance_CH']['Morocco'])+(transport[['other_fresh_fruits_vegetables']].loc['Morocco','Rail traffic'].iat[0]*transportCO2['Rail traffic']*countries['distance_CH']['Morocco'])))/12)
    
    tomatoes['transport_percent'] = ((tomatoes['imported_from_ES_month'] - tomatoes['produced_in_CH_month'])/tomatoes['produced_in_CH_month'])*100
    
    return tomatoes.drop('total_consumption', axis=1)


def add_emissions_data(suisse, emissions):
    """map the emissions data to each category in the Suisse dataframe"""
    
    dic = load_dic()
    suisse.reset_index(inplace=True)
    suisse['emissions_category'] = suisse['subtype'].map(dic)
    suisse.emissions_category.fillna(suisse['subtype'], inplace=True)
    suisse = pd.merge(suisse, emissions[['Median']].reset_index(), left_on='emissions_category', right_on='name').set_index(['type','subtype']).drop("name", axis=1).rename({'Median': 'median_emissions'}, axis='columns')
    
    return suisse


def production_emissions(suisse):
    """multiplies production values (kg) by the average production emissions (kg CO2-eq/kg produce)"""
    
    suisse['emissions_sans_transport'] = suisse['consumption'] * suisse['median_emissions']
    
    return suisse


def country_distances():
    "calculates distance from the centre of each country to the centre of Switzerland, or to Rotterdam (port, intermediate step on route to CH"""
    
    countries = load_countries_continents()[["country"]]

    def find_coord(x):
        location = geolocator.geocode(x, timeout=100)
        if location != None:
            return [location.latitude, location.longitude]
        else:
            return np.nan

    countries['coord'] = countries.country.apply(find_coord)

    def find_distance(x):
        try:
            return geodesic(switzerland, tuple(x)).km
        except:
            return np.nan
        
    def find_distance_NL(x):
        try:
            return geodesic(rotterdam, tuple(x)).km
        except:
            return np.nan

    countries['distance_CH'] = countries.coord.apply(find_distance).round()
    countries['distance_NL'] = countries.coord.apply(find_distance_NL).round()
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


def swiss_consumption_transport(row, transport, transportCO2, countries, colmap, NL=False):
    trans_nl = 0
    
    # get the fractions for a given country and food product imported by each method of transport
    trans = transport.loc[row['country']][[colmap[row['type']]]]
    
    # multiply the fractions by the amount consumed in Switzerland from that country to get kilos imported
    # by each method of transport
    trans['kilos_consumed'] = trans.iloc[:,0] * row['swiss_consumption']
    
    # multiply the carbon cost of each method of transport by the kilos imported by that transport method
    trans = trans.reset_index()
    trans['carbon_cost_per_km'] = trans.iloc[:,2] * trans['mode_of_transport'].map(transportCO2)
    
    def transport_rotterdam(row_2):
        # alternative route via ship to Rotterdam for countries outside of Europe
        if row_2['mode_of_transport'] == 'Air traffic':
             return (row_2['carbon_cost_per_km'] * countries.loc[row['country']][1])
        else:
            # transport to Rotterdam by Container ship
            trans_nl = row_2['kilos_consumed'] * transportCO2['Inland waterways']
            return ((row_2['carbon_cost_per_km'] * distance_rotterdam) + (trans_nl * countries.loc[row['country']][2]))
    
    if NL:
        if row['continent'] != 'Europe':
            trans['carbon_cost'] = trans.apply(transport_rotterdam, axis=1)

        else:

            # multiply the carbon cost by the km between that country and Switzerland to get total kg of CO2e produced
            trans['carbon_cost'] = trans.iloc[:,3] * countries.loc[row['country']][1]
            # IF YOU WANT DETAILS LATER (E.G. CARBON COST BY TRANSPORT METHOD), GRAB THE DATAFRAME HERE BEFORE THE NEXT STEP
            # return trans
    else:
        trans['carbon_cost'] = trans.iloc[:,3] * countries.loc[row['country']][1]
    
    # sum the total carbon cost of transport for this food item coming from this country
    return trans.iloc[:,4].sum()


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

