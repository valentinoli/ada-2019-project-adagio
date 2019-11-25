def load_emissions():
    # load dictionary to match categories with impex categories
    fruit_veg = {}
    with open("../data/categories.txt") as f:
        for line in f:
            (key, val) = line.split('\t')
            fruit_veg[key] = val.strip('\n')

    # load global emissions data
    emissions = pd.read_excel(r'../data/food_emissions.xlsx')

    # add category column
    emissions['Category'] = emissions.Name.map(fruit_veg)
    emissions.set_index('Name', inplace=True)

    return emissions


def estimate_emissions(domestic, emissions):
    # define function to estimate emissions for each row
    # NOTE this depends on the index of these two dataframes being the same,
    # which is currently not the case... Not sure how we should resolve this, my friend regex?
    
    def emis(food, name):
        return food[name] * 1000000 * emissions.loc[food['Product'],'Mean']

    # apply this to some different columns
    domestic['Domestic Equivalent CO2'] = domestic.apply(emis, args = ['Domestic Consumption'], axis = 1)
    domestic['Imported Equivalent CO2'] = domestic.apply(emis, args = ['Imported Consumption'], axis = 1)
    domestic['Total Equivalent CO2'] = domestic.apply(emis, args = ['Total Consumption'], axis = 1)

    return domestic


def glimpse():
    # load data
    imported_goods = pd.read_excel('../data/nature-of-goods-imports.xlsx', skiprows=5, sheet_name='01.1')
    imported_goods.dropna(how='all',inplace=True)
    imported_goods.drop(columns=['Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8'], inplace=True) #empty columns
    imported_goods.rename({'Unnamed: 0':'Year', 'Unnamed: 1':'Commercial Partner'}, inplace=True, axis=1)
    imported_goods['Commercial Partner'] = imported_goods['Commercial Partner'].str.strip() # get rid of leading whitespace

    # filter for nearby countries
    nearby_countries = ['Portugal', 'Spain', 'France', 'Germany', 'Italy', 'Austria', 'Belgium', 'Netherlands', 'Czech Republic', 'Slovenia', 'Croatia', 'Luxembourg', 'Montenegro', 'Serbia', 'Slovakia', 'Poland', 'United Kingdom']
    imported_goods_nearby = imported_goods[imported_goods['Commercial Partner'].isin(nearby_countries)].copy()

    # calculate percentage of goods imported from nearby countries
    total_nearby_imported = imported_goods_nearby['Quantity (kg)'].sum()
    return 100*total_nearby_imported/imported_goods.iloc[0][2]

