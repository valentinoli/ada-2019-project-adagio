# -*- coding: utf-8 -*-
"""Scripts for Emissions data loading and manipulation, i.e. generating schemas from raw data"""

import pandas as pd


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


def estimate_emissions(domestic, emissions):
    # define function to estimate emissions for each row
    # NOTE this depends on the index of these two dataframes being the same,
    # which is currently not the case... Not sure how we should resolve this, my friend regex?
    
    def emis(food, name):
        return food[name] * 1000000 * emissions.loc[food["Product"], "Mean"]

    # apply this to some different columns
    domestic["Domestic Equivalent CO2"] = domestic.apply(emis, args=["Domestic Consumption"], axis=1)
    domestic["Imported Equivalent CO2"] = domestic.apply(emis, args=["Imported Consumption"], axis=1)
    domestic["Total Equivalent CO2"] = domestic.apply(emis, args=["Total Consumption"], axis=1)

    return domestic


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

