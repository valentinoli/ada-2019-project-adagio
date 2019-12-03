import pandas as pd

def clean_impex_dataset(file_location, sheet):
    df = pd.read_excel(file_location, skiprows=5, sheet_name=sheet)
    df.dropna(how='all',inplace=True)
    df.drop(columns=['Unnamed: 0','Unnamed: 8'], inplace=True) #unnecessary/empty columns
    df.rename({'Unnamed: 1':'Commercial Partner',\
               'Quantity (kg)':'Import Quantity (kg)', 'Value (CHF)':'Import Value (CHF)', \
              'Value +/- %':'Import Value +/- %', 'Quantity (kg).1':'Export Quantity (kg)', \
               'Value (CHF).1':'Export Value (CHF)', \
              'Value +/- %.1':'Export Value +/- %',}, inplace=True, axis=1)
    df['Commercial Partner'] = df['Commercial Partner'].str.strip() # get rid of leading whitespace
    return df


def merge_two_sheets(sheet1, sheet2):
    merged = pd.merge(sheet1, sheet2, on='Commercial Partner', how='outer')
    
    merged.replace(to_replace ='*', value =0, inplace=True)
    merged.replace(to_replace ='**', value =1000, inplace=True)
    merged.replace(to_replace ='***', value =0, inplace=True)
    merged.fillna(0, inplace=True)
    merged['Import Value +/- %_x'] = merged['Import Value +/- %_x'].astype(float)
    merged['Import Value +/- %_y'] = merged['Import Value +/- %_y'].astype(float)
    merged['Export Value +/- %_x'] = merged['Export Value +/- %_x'].astype(float)
    merged['Export Value +/- %_y'] = merged['Export Value +/- %_y'].astype(float)

    # get rid of a few rows which are just all 0s that snuck in from the bottom of the sheet data
    merged = merged[(merged.T != 0).any()]
    
    merged['Import Quantity (kg)'] = merged['Import Quantity (kg)_x'] + merged['Import Quantity (kg)_y']
    merged.drop(columns=['Import Quantity (kg)_x', 'Import Quantity (kg)_y'], inplace=True)

    merged['Import Value (CHF)'] = merged['Import Value (CHF)_x'] + merged['Import Value (CHF)_y']
    merged.drop(columns=['Import Value (CHF)_x', 'Import Value (CHF)_y'], inplace=True)

    merged['Import Value +/- %'] = merged['Import Value +/- %_x'] + merged['Import Value +/- %_y']
    merged.drop(columns=['Import Value +/- %_x', 'Import Value +/- %_y'], inplace=True)

    merged['Export Quantity (kg)'] = merged['Export Quantity (kg)_x'] + merged['Export Quantity (kg)_y']
    merged.drop(columns=['Export Quantity (kg)_x', 'Export Quantity (kg)_y'], inplace=True)

    merged['Export Value (CHF)'] = merged['Export Value (CHF)_x'] + merged['Export Value (CHF)_y']
    merged.drop(columns=['Export Value (CHF)_x', 'Export Value (CHF)_y'], inplace=True)

    merged['Export Value +/- %'] = merged['Export Value +/- %_x'] + merged['Export Value +/- %_y']
    merged.drop(columns=['Export Value +/- %_x', 'Export Value +/- %_y'], inplace=True)
    
    merged.sort_values(by='Commercial Partner', inplace=True) 
    # this sorts alphabetically, so let's now move the 'total trade' to the top row:
    # pick out and set aside the total trade value
    total = merged[merged['Commercial Partner'] == 'Total trade']
    # take the total trade out of the dataframe, then add it back in at the top
    merged.drop(0, axis=0, inplace=True)
    merged = pd.concat([total, merged])
    
    return merged