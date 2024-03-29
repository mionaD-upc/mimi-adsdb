import pandas as pd
import os
import utils


household_columns = ['section','delete','delete','single_women_aged_16_to_64','single_men_aged_16_to_64','single_women_aged_65_or_over','single_men_aged_65_or_over',
    'adult_women_with_one_or_more_minors','adult_men_with_one_or_more_minors','two_adults_from_16_to_64_and_without_minors',
    'two_adults_one_at_least_65_and_without_minors','two_adults_and_one_minor','two_adults_and_two_minors','two_adults_and_three_or_more_minors',
    'two_adults_over_35_and_one_adult_from_16_to_34','two_adults_over_35_and_one_adult_from_16_to_34_and_one_minor',
    'two_adults_over_35_and_one_adult_from_16_to_34_and_two_minors','three_adults_and_0_or_more_minors','two_adults_over_35_and_two_adults_from_16_to_34',
    'two_adults_over_35_and_two_adults_from_16_to_34_and_one_minor','two_adults_over_35_and_two_adults_from_16_to_34_and_two_or_more_minors',
    'four_adults_and_0_or_more_minors','five_adults_and_0_or_more_minors','fifteen_or_more_inhabitants','only_minors']

def read_household(path):
    """
    Prepares the Household excel file, 
    Returns the data in DataFrame format
    """
    df = pd.read_excel(path,sheet_name='Composicion del hogar', header=[5], names=household_columns)

    # Formatting the excel format to dataframe
    df['section'].fillna(df['delete'],inplace=True)
    df.drop(df.filter(like='delete'),axis=1, inplace=True)
    df.dropna(inplace = True)

    # Removes the total rows 
    newDF = df[pd.to_numeric(df['section'], errors='coerce').notnull()]
    assert df.shape[0] - newDF.shape[0] == 22

    return newDF


def read_nationalities(path):
    """
    Reads the Nationalities Excel
    Returns the data in DataFrame format
    """
    df = pd.read_excel(path, sheet_name='Total', header=[7])

    # Formatting excel format to dataframe
    df.rename(columns = {'Unnamed: 0':'Madrid_section','Unnamed: 3':'Españoles'}, inplace = True)
    df.drop(df.filter(regex='Unname'),axis=1, inplace=True)
    df.dropna(inplace = True)

    # Removes the total columns
    df.drop(df.filter(like='Total'),axis=1, inplace=True)

    # Formatting the column name
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(' ', '_')

    # Removes the total rows 
    newDF = df[df['Madrid_section'].apply(lambda x: len(x.strip()) == 9)]

    return newDF


def formatted_zone():
    """
    Stores the excel tables from `/persistent` in a relational data base.
    Returns the relational data base
    """
    path = os.getcwd()
    utils.clear_database(path)

    dfhs = []
    dfns = []
    for file in os.listdir('persistent'):
        file_path = f'{path}/persistent/{file}'
        table = file.split('_')[1].split('.')[0]
        repo = ''.join(filter(str.isalpha,table))

        if repo == 'household':
            df = read_household(file_path)
            dfhs.append(df)

        elif repo == 'nationalities':
            df = read_nationalities(file_path)
            dfns.append(df)

        utils.df_to_DBtable(f'{repo}.duckdb',df,table)
        print(f'    - ./persistent/{file} stored in {repo} DuckDB') 
    return dfhs, dfns


def main():
    print('\nSTART FORMATTED')
    print(' - Storing the data in a relational database...')
    formatted_zone() 
