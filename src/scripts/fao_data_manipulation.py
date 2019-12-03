# -*- coding: utf-8 -*-
"""Scripts for FAO data loading and manipulation, i.e. generating schemas from raw data"""

import pandas as pd
from scripts.fao_types import TYPES


def manipulate_fruits(df):
    """Manipulate dataframe for fruit production"""
    # Combine gooseberries and currants to match impex dataset
    gooseberries_currants = df[df["subtype"].isin(["gooseberries", "currants"])]
    df = df.append(
        {
            "subtype": "gooseberries_and_currants",
            "production": gooseberries_currants.sum().production,
        },
        ignore_index=True,
    )
    df = df[~df.subtype.isin(["gooseberries", "currants"])].sort_values("subtype")
    

def manipulate_meat(df):
    """Manipulate dataframe for meat production"""
    # Combine sheep and goat to match impex dataset
    sheep_goat = df[df["subtype"].isin(["sheep", "goat"])]
    df = df.append(
        {
            "subtype": "sheep_goat",
            "production": sheep_goat.sum().production,
        },
        ignore_index=True,
    )
    df = df[~df.subtype.isin(["sheep", "goat"])].sort_values("subtype")
    

def load_fao_type(key):
    """Load the FAO data on Swiss Crop Production"""
    path = f"../data/fao/swiss_{key}_production.csv"
    
    production = pd.read_csv(
        path,
        header=0,
        names=["subtype", "production"],
        usecols=[7, 11],
        converters={
            # convert subtype name to match the impex dataset
            7: lambda x: x.lower().replace(",", "").replace("meat ", "").replace(" ", "_"),
        },
    )
    
    # Replace NaN with 0 (no production)
    production.fillna(0, inplace=True)
    
    # tonnes --> kg
    production["production"] = production.production.astype(float) * 1000
    
    if key == "fruits":
        manipulate_fruits(production)
        
    elif key == "meat":
        manipulate_meat(production)
        
    
    production.set_index("subtype", inplace=True)
    production.columns.set_names("indicator", inplace=True)
    return production


def load_fao():
    dfs = []
    for key in TYPES:
        dfs.append(load_fao_type(key))
    
    return pd.concat(dfs)