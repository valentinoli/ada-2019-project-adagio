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
    """Load imports/exports excel-file(s) from Impex"""
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
    """Loads all the impex data and returns as a single dataframe"""
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

