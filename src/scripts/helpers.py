# -*- coding: utf-8 -*-
"""Various helper constants and functions"""

import pandas as pd

# Selected countries near Switzerland
nearby_countries = [
    "Portugal",
    "Spain",
    "France",
    "Germany",
    "Italy",
    "Austria",
    "Belgium",
    "Netherlands",
    "Czech Republic",
    "Slovenia",
    "Croatia",
]


def load_countries_continents():
    """Load countries and the continents they belong to"""
    return pd.read_excel(
        "../data/impex/countries/impex-countries.xlsx",
        usecols=[0, 1, 2]
    )

