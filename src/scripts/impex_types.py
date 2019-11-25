"""Includes dictionary of info for loading the Impex data from custom-downloaded Excel sheets"""

# if separate_files=True load each subtype from
# separate file and sum the sheets
TYPES = {
    "fruits": {
        "separate_files": False,
        "subtypes": [
            "coconuts_brazil_cashew",
            "other_nuts",
            "bananas",
            "exotic_fruit",
            "citrus_fruit",
            "grapes",
            "melons",
            "apples_pears",
            "stone_fruit",
            "berries",
            "dried",
        ],
    },
    "vegetables": {
        "separate_files": False,
        "subtypes": [
            "potatoes",
            "tomatoes",
            "onions_garlic_shallots_leeks",
            "cabbage_cauliflower_kohlrabi_kale",
            "lettuce_chicory",
            "edible_roots",
            "cucumbers_gherkins",
            "leguminous",
            "other",
        ],
    },
    "meat": {
        "separate_files": True,
        "subtypes": [
            "chicken",
            "pork",
            "beef",
            "turkey",
            "duck_goose",
            "equine",
            "sheep_goat",
        ],
    },
    "animal_products": {
        "separate_files": False,
        "subtypes": [
            "milk_cream",
            "yogurt",
            "whey",
            "butter",
            "cheese",
            "eggs",
            "honey",
        ],
    },
}
