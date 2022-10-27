import os
import pandas as pd
import duckdb 

household_columns = ['section','delete','population','single_women_aged_16_to_64','single_men_aged_16_to_64','single_women_aged_65_or_over','single_men_aged_65_or_over',
    'adult_women_with_one_or_more_minors','adult_men_with_one_or_more_minors','two_adults_from_16_to_64_and_without_minors',
    'two_adults_one_at_least_65_and_without_minors','two_adults_and_one_minor','two_adults_and_two_minors','two_adults_and_three_or_more_minors',
    'two_adults_over_35_and_one_adult_from_16_to_34','two_adults_over_35_and_one_adult_from_16_to_34_and_one_minor',
    'two_adults_over_35_and_one_adult_from_16_to_34_and_two_minors','three_adults_and_0_or_more_minors','two_adults_over_35_and_two_adults_from_16_to_34',
    'two_adults_over_35_and_two_adults_from_16_to_34_and_one_minor','two_adults_over_35_and_two_adults_from_16_to_34_and_two_or_more_minors',
    'four_adults_and_0_or_more_minors','five_adults_and_0_or_more_minors','fifteen_or_more_inhabitants','only_minors']

def read_household(file):
    """
    Prepares the Household excel file, 
    Returns the data in DataFrame format
    """
    path = f'./persistent/{file}'
    df = pd.read_excel(path,sheet_name='Composicion del hogar', header=[5], names=household_columns)

    # Formatting the excel format to dataframe
    df['section'].fillna(df['delete'],inplace=True)
    df.drop(labels='delete', axis=1, inplace=True)
    df.dropna(inplace = True)

    # Removes the total rows 
    newDF = df[pd.to_numeric(df['section'], errors='coerce').notnull()]
    assert df.shape[0] - newDF.shape[0] == 22

    return newDF


def read_nationalities(file):
    """
    Reads the Nationalities Excel
    Returns the data in DataFrame format
    """
    path = f'./persistent/{file}'
    df = pd.read_excel(path, sheet_name='Total', header=[7])

    # Formatting excel format to dataframe
    df.rename(columns = {'Unnamed: 0':'Madrid_section','Unnamed: 2':'Habitantes','Unnamed: 3':'Españoles','Unnamed: 4':'Extranjeros'}, inplace = True)
    df.drop('Unnamed: 1', axis=1, inplace=True)
    df.drop(df.filter(regex='Unname'),axis=1, inplace=True)
    df.dropna(inplace = True)

    # Removes the total columns
    df.drop(df.filter(like='Total'),axis=1, inplace=True)

    # Formatting the column name
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(' ', '_')
    return df


def df_to_DBtable(DB,df,table):
    """
    Creates a persistent table in DuckDB from the DataFrame content.
    """
    con = duckdb.connect(DB)
    con.register(table, df)
    con.execute(f'CREATE TABLE {table} AS SELECT * FROM {table}')
    con.close()


def formatted_zone():
    """
    Stores the excel tables in a relational data base.
    """
    for file in os.listdir('./persistent/'):  
        table = file.split('_')[1].split('.')[0]
        repo = ''.join(filter(str.isalpha,table))
        df = read_household(file) if repo == 'household' else read_nationalities(file)
        df_to_DBtable(f'../{repo}.duckdb',df,table)

