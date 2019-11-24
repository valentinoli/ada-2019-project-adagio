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


def compute_nearby_imports_ratio(imports):
    """Compute the ratio of imported products which come from nearby countries"""
    imported_nearby = imports[imports.commercial_partner.isin(nearby_countries)]
    total_nearby = imported_nearby.quantity_kg.sum()
    total_overall = imports.iloc[0, 1]
    return total_nearby / total_overall
