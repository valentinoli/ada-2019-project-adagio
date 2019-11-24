# -*- coding: utf-8 -*-
"""Scripts for data loading and manipulation, i.e. generating schemas from raw data"""

import pandas as pd

# paths
FOOD_IMPORTS_PATH = '../data/nature-of-goods-imports.xlsx'
MEAT_IMPORTS_PATH = '../data/selected-meat-imports.xlsx'
FRUITS_VEGGIES_IMPORTS_PATH = '../data/fruits_and_veggies_imported.xlsx'
CONSUMPTION_PATH = '../data/food_consumption_by_type_of_food.xlsx'

PKL = ".pkl"

def read_pickle(path, postfix=""):
    pickle_path = path + postfix + PKL
    return pd.read_pickle(pickle_path)


def to_pickle(df, path, postfix=""):
    pickle_path = path + postfix + PKL
    df.to_pickle(pickle_path)


def load_imports(filepath, sheet=0):
    """Loads specific imports/exports data from Swiss Impex"""
    colnames = ["commercial_partner", "quantity_kg", "value_chf", "value_change_%"]
    
    res = pd.read_excel(
        filepath,
        sheet_name=sheet,
        names=colnames,
        usecols=[1, 2, 3, 4],
        skiprows=5,
        converters={
            # strip whitespace from country name
            0: lambda x: x.strip()
        }
    )
    
    if isinstance(res, pd.DataFrame):
        return res.set_index("commercial_partner").dropna(how="all")
    
    # return dictionary of dataframes
    for df in res.values():
        df.set_index("commercial_partner", inplace=True)
        df.dropna(how="all", inplace=True)
        
    return res


def load_imported_food():
    """Load imports: food, beverages, and tobacco"""
    try:
        return read_pickle(FOOD_IMPORTS_PATH)
    except:
        df = load_imports(FOOD_IMPORTS_PATH)
        to_pickle(FOOD_IMPORTS_PATH, df)
        return df


def load_imported_feed():
    """Load imports: feeding stuffs for animals"""
    pickle_postfix = "feed"
    try:
        return read_pickle(FOOD_IMPORTS_PATH, postfix=pickle_postfix)
    except:
        df = load_imports(FOOD_IMPORTS_PATH, sheet=1)
        to_pickle(FOOD_IMPORTS_PATH, postfix=pickle_postfix)


def load_imported_meat():
    """Load imports: meat and edible meat offal"""
    try:
        return read_pickle(MEAT_IMPORTS_PATH)
    except:
        df = load_imports(MEAT_IMPORTS_PATH, sheet="02")
        to_pickle(MEAT_IMPORTS_PATH)


def load_imported_fruits():
    """Load imports: fruits"""
    # bananas, exotic fruit, citrus fruit, grapes,
    # melons, apples, stone fruit, berries
    sheets = list(range(19, 27))
    names = [
        "bananas", "exotic_fruit", "citrus fruit", "grapes",
        "melons", "apples", "stone_fruit", "berries"
    ]
    dfs = load_imports(FRUITS_VEGGIES_IMPORTS_PATH, sheet=sheets)
    print(dfs)


def load_food_consumption():
    colnames = [
        "food_type",
        "quantity_total_1k_tonnes",
        "quantity_kg_person_year",
        "protein_total_tonnes",
        "protein_g_person_day",
        "protein_%_local_production",
        "energy_intake_total_tj",
        "energy_intake_kj_person_day",
        "energy_intake_%_local_production"
    ]
    
    df = pd.read_excel(
        CONSUMPTION_PATH,
        sheets=0,  # first sheet, year 2017
        names=colnames,
        skiprows=9,
        converters={
            # strip whitespace from first column
            0: lambda x: x.strip()
        }
    ).dropna()  # remove all rows with NaN values
    
    df.set_index("food_type", inplace=True)
    
    return df



