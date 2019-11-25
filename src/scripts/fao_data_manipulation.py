import pandas as pd

def load_fao():
    production = pd.read_csv(
        "../data/swiss_crop_production.csv",
        header=0,
        names=["subtype", "total"],
        usecols=[7, 11],
        converters={
            7: lambda x: x.lower().replace(",", "").replace(" ", "_"),
        },
    )

    production = production.fillna(0)
    production["total"] = production.total.apply(lambda x: float(x) * 1000)  # tonnes --> kg
    production["metric"] = "production"
    
    gooseberries_currants = production[production["subtype"].isin(["gooseberries", "currants"])]
    production = production.append(
        {
            "subtype": "gooseberries_and_currants",
            "total": gooseberries_currants.sum().total,
        },
        ignore_index=True,
    )
    production = production[~production.subtype.isin(["gooseberries", "currants"])].sort_values("subtype")
    
    production.set_index(["subtype", "metric"], inplace=True)
    return production


