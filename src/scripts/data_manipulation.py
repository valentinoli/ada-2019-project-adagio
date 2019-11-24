# -*- coding: utf-8 -*-
"""Scripts for data loading and manipulation, i.e. generating schemas from raw data"""

import pandas as pd

# paths
FOOD_IMPORTS_PATH = '../data/nature-of-goods-imports.xlsx'
MEAT_IMPORTS_PATH = '../data/selected-meat-imports.xlsx'
FRUITS_VEGGIES_IMPORTS_PATH = '../data/fruits_and_veggies_imported.xlsx'
FRUITS_VEGGIES_EXPORTS_PATH = '../data/fruits_veggies_exported.xlsx'
CONSUMPTION_PATH = '../data/food_consumption_by_type_of_food.xlsx'


def load_imports_exports(filepath, sheet=0):
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
        return res.dropna(how="all")
    
    # return dictionary of dataframes
    for df in res.values():
        df.set_index("commercial_partner", inplace=True)
        df.dropna(how="all", inplace=True)
        
    return res


# obsolete function
def load_imported_food():
    """Load imports: food, beverages, and tobacco"""
    return load_imports_exports(FOOD_IMPORTS_PATH)


def load_imported_feed():
    """Load imports: feeding stuffs for animals"""
    return load_imports_exports(FOOD_IMPORTS_PATH, sheet=1)


def load_imported_meat():
    """Load imports: meat and edible meat offal"""
    return load_imports_exports(MEAT_IMPORTS_PATH, sheet="02")


def load_traded_fruits_veggies(trade_direction, food_type):
    """Load imports: fruits or vegetables"""
    # fruits: bananas, exotic fruit, citrus fruit, grapes,
    # melons, apples, stone fruit, berries
    # vegetables: 
    if food_type == 'fruits':
        sheets = list(range(19, 27))
        names = [
            "bananas", "exotic_fruit", "citrus fruit", "grapes",
            "melons", "apples", "stone_fruit", "berries"
        ]
    elif food_type == 'vegetables':
        sheets = list(range(2, 10))
        names = [
            "potatoes", "tomatoes", "onions_garlic_shallots_leeks", "cabbage_cauliflower_kohlrabi_kale",
            "lettuce_chicory", "edible_roots", "cucumbers_gherkins", "leguminous"
        ]
    # else:
        # throw an error, should be either "fruits" or "vegetables"
        
    if trade_direction == 'imports':
        dfs = load_imports_exports(FRUITS_VEGGIES_IMPORTS_PATH, sheet=sheets)
    elif trade_direction == 'exports':
        dfs = load_imports_exports(FRUITS_VEGGIES_EXPORTS_PATH, sheet=sheets)
    #else:
        # throw an error, should be either "imports" or "exports"
    
    # create a two-level multi-index
    level_1 = dict(zip(sheets, names))
    level_2 = dfs[sheets[0]].columns
    
    for k, v in dfs.items():
        # for each dataframe, change the columns into a multi-index
        # where the first level is the fruit type
        columns = [(level_1[k], j) for j in level_2]
        v.columns = pd.MultiIndex.from_tuples(columns)
    
    # outer join the dataframes
    frames = list(dfs.values())
    return frames[0].join(frames[1:], how="outer")


# this function is obsolete (no longer using this dataset)
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



