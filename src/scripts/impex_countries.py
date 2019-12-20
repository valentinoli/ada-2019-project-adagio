# -*- coding: utf-8 -*-
"""Function for loading country-data from Impex"""

import pandas as pd

def load_countries_continents():
    """Load countries and the continents they belong to"""
    return pd.read_excel(
        "../data/impex/countries/impex-countries.xlsx",
        usecols=[0, 1, 2]
    )

