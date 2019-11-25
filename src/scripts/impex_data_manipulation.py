# -*- coding: utf-8 -*-
"""Scripts for data loading and manipulation, i.e. generating schemas from raw data"""

import pandas as pd
from scripts.impex_types import TYPES

def read_excel(path, names):
    """Read Impex Excel file
    
    :param path:  filepath
    :param names: column names
    :returns:     single sheet - dataframe
                  many sheets  - dictionary of dataframes
    """
    return pd.read_excel(
        path,
        sheet_name=None,  # load all sheets
        names=names,
        usecols=[1, 2, 3, 5, 6],
        skiprows=5,
        converters={
            # strip whitespace from country name
            0: lambda x: x.strip()
        }
    )


def dfs_dict_to_list(dfs):
    """Convert a dataframe (dictionary) to a list"""
    if isinstance(dfs, pd.DataFrame):
        # dfs is a single dataframe
        return [dfs]
    
    return list(dfs.values())
    

def impex_dfs_manipulate(dfs, index):
    """Set the index of each dataframe and impute missing values
    
    :param dfs:   list of dataframes
    :param index: name of the index
    """
    for df in dfs:
        df.set_index(index, inplace=True)  
        df.rename(index={"Total trade": "total"}, inplace=True)
        
        # drop nan-rows and impute missing values
        df.dropna(how="all", inplace=True)
        df.fillna(0, inplace=True)


def load_impex_type(key, val):
    """Load imports/exports excel-file from Impex"""
    index = "commercial_partner"   # dataframe's index
    cols = ["quantity", "value"]   # lowest column header level
    impex = ["imports", "exports"] # second-lowest level
    
    colnames = [index] + cols + cols  # lowest column header on each sheet
    separate_files = val["separate_files"]  # True/False
    subtypes = val["subtypes"]              # list of subtypes
    
    if separate_files:
        res = []
        for s in subtypes:
            # for each subtype, we load data
            # from the file and sum up the numbers
            # in each sheet
            path = f"../data/impex/{s}.xlsx"            
            dfs = read_excel(path, colnames)
            
            dfs = dfs_dict_to_list(dfs)
            impex_dfs_manipulate(dfs, index)
            
            # sum up the dataframes (sheets)
            dfs_stacked = pd.concat(dfs)
            df_subtype = dfs_stacked.groupby(dfs_stacked.index).sum()
            
            # append the summed up frame to the result list
            res.append(df_subtype)
        
    else:
        path = f"../data/impex/{key}.xlsx"
        res = read_excel(path, colnames)
        
        res = dfs_dict_to_list(res)
        impex_dfs_manipulate(res, index)
    
    
    level_1 = key      # meta-type
    level_2 = subtypes # sub-type
    level_3 = impex    # imports/exports
    level_4 = cols     # quantity/value

    for i, df in enumerate(res):
        # for each dataframe, convert the header into a multi-index
        l2 = level_2[i]
        columns = [
            (level_1, l2, l3, l4)
            for l3 in level_3 for l4 in level_4
        ]
        df.columns = pd.MultiIndex.from_tuples(columns)
    
    return res


def load_impex():
    dfs = []
    for k, v in TYPES.items():
        dfs_type = load_impex_type(k, v)
        
        if len(dfs_type):
            # join dataframes if there are more than one
            # and add to the list of sub-frames 
            # (each corresponds to a meta-type)
            joined = dfs_type[0].join(dfs_type[1:], how="outer")
            dfs.append(joined)
    
    # join the list of sub-frames
    return dfs[0].join(dfs[1:], how="outer")

def load_emissions():
    # load dictionary to match categories with impex categories
    fruit_veg = {}
    with open("../data/categories.txt") as f:
        for line in f:
            (key, val) = line.split('\t')
            fruit_veg[key] = val.strip('\n')
            
    # load global emissions data
    emissions = pd.read_excel(r'../data/food_emissions.xlsx')
    
    # add category column
    emissions['Category'] = emissions.Name.map(fruit_veg)
    emissions.set_index('Name', inplace=True)
    
    return emissions

def estimate_emissions(domestic, emissions):
    # define function to estimate emissions for each row
    # NOTE this depends on the index of these two dataframes being the same, which is currently not the case... Not sure how we should resolve this, my friend regex?
    def emis(food, name):
        return food[name] * 1000000 * emissions.loc[food['Product'],'Mean']
    
    # apply this to some different columns
    domestic['Domestic Equivalent CO2'] = domestic.apply(emis, args = ['Domestic Consumption'], axis = 1)
    domestic['Imported Equivalent CO2'] = domestic.apply(emis, args = ['Imported Consumption'], axis = 1)
    domestic['Total Equivalent CO2'] = domestic.apply(emis, args = ['Total Consumption'], axis = 1)
    
    return domestic

def glimpse():
    # load data
    imported_goods = pd.read_excel('../data/nature-of-goods-imports.xlsx', skiprows=5, sheet_name='01.1')
    imported_goods.dropna(how='all',inplace=True)
    imported_goods.drop(columns=['Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8'], inplace=True) #empty columns
    imported_goods.rename({'Unnamed: 0':'Year', 'Unnamed: 1':'Commercial Partner'}, inplace=True, axis=1)
    imported_goods['Commercial Partner'] = imported_goods['Commercial Partner'].str.strip() # get rid of leading whitespace
    
    # filter for nearby countries
    nearby_countries = ['Portugal', 'Spain', 'France', 'Germany', 'Italy', 'Austria', 'Belgium', 'Netherlands', 'Czech Republic', 'Slovenia', 'Croatia', 'Luxembourg', 'Montenegro', 'Serbia', 'Slovakia', 'Poland', 'United Kingdom']
    imported_goods_nearby = imported_goods[imported_goods['Commercial Partner'].isin(nearby_countries)].copy()
    
    # calculate percentage of goods imported from nearby countries
    total_nearby_imported = imported_goods_nearby['Quantity (kg)'].sum()
    
    return 100*total_nearby_imported/imported_goods.iloc[0][2]

