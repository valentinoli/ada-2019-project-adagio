# -*- coding: utf-8 -*-
"""Scripts for FAO data loading and manipulation, i.e. generating schemas from raw data"""

import pandas as pd
from scripts.impex_types import TYPES
from scripts.fao_types import FAO_PARTS, FAO_TO_IMPEX_TYPE

def get_metatype(subtype):
    """Gets the metatype of the given commodity subtype;
    returns 'other' if not found"""
    return next(
        (k for k, v in TYPES.items() if subtype in v["subtypes"]),
        "other"
    )


def load_fao_part(key):
    """Load part of FAO data given by key"""
    path = f"../data/fao/swiss_{key}_production.csv"
    
    production = pd.read_csv(
        path,
        header=0,
        names=["subtype", "production"],
        usecols=[7, 11],
        converters={
            # pre-process the subtype to match impex types
            7: lambda x: x.lower().replace(",", "").replace(" ", "_"),
        },
    )
    
    # Interpret NaN as 0 production
    production.fillna(0, inplace=True)
    
    # tonnes --> kg
    production["production"] = production.production.astype(float) * 1000
    
    return production


def load_fao():
    """Load all FAO data"""
    dfs = []
    for key in FAO_PARTS:
        # For each FAO part we load the data
        dfs.append(load_fao_part(key))
    
    # Concatenate all dataframes
    df = pd.concat(dfs)
    
    # Convert the subtype names to match impex types
    df.subtype.replace(regex=FAO_TO_IMPEX_TYPE, inplace=True)
    
    # Get the metatype for each subtype
    df["type"] = df.subtype.apply(get_metatype)
    
    # Group by type-subtype and sum values for each group
    # (since sometimes there are two or more rows we want to aggregate)
    df = df.groupby(["type", "subtype"]).sum()
    
    # Drop "other" metatype, since we explicitly decided to eliminate these
    df.drop("other", level=0, inplace=True)
    
    df.sort_values(["type", "subtype"], inplace=True)
    df.columns.set_names("indicator", inplace=True)
    
    return df

