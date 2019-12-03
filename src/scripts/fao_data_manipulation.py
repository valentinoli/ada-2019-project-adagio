import pandas as pd

def load_fao():
    """Load the FAO data on Swiss Crop Production"""
    production = pd.read_csv(
        "../data/swiss_crop_production.csv",
        header=0,
        names=["subtype", "production"],
        usecols=[7, 11],
        converters={
            # convert subtype name to match the impex dataset
            7: lambda x: x.lower().replace(",", "").replace(" ", "_"),
        },
    )
    
    # Replace NaN with 0 (no production)
    production.fillna(0, inplace=True)
    
    # tonnes --> kg
    production["production"] = production.production.astype(float) * 1000
    
    # combine gooseberries and currants to match impex dataset
    gooseberries_currants = production[production["subtype"].isin(["gooseberries", "currants"])]
    production = production.append(
        {
            "subtype": "gooseberries_and_currants",
            "production": gooseberries_currants.sum().production,
        },
        ignore_index=True,
    )
    production = production[~production.subtype.isin(["gooseberries", "currants"])].sort_values("subtype")
    
    production.set_index("subtype", inplace=True)
    production.columns.set_names("variable", inplace=True)
    return production


