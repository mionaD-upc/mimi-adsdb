import pandas as pd
import utils
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def pre_join(DB):
    """
    Adds a version (year) column to all `DB` tables in order to do the joining.
    Returns all the `DB` tables in data frame format.
    """
    tablesDB = utils.get_tables(DB)
    dfs = []
    for table in tablesDB:
        year = table[-4:]
        df = utils.DBtable_to_df(DB, table)
        df['Year'] = year
        dfs.append(df)
    return dfs

def trusted_zone(DB,table):
    """
    Joins all the tables found in the database `DB` into one called `table`.
    Returns the dataframe
    """
    dfs = pre_join(DB)
    df = pd.concat(dfs, axis=0, ignore_index=True)
    utils.df_to_DBtable(DB,df,table)
    return df

## Household - Trust zone
def gaussianity_plot(df): 
    """
    Creates a gaussian plot
    """  
    fig, axes = plt.subplots(6, 4, figsize=(15, 15))

    for i, c in enumerate(df.columns[1:-1]):
        ax = axes.reshape(-1)[i]

        count, bins, ignore = ax.hist(df[c], 15, density=True)
        sigma = df[c].std()
        mu = df[c].mean()
        dbins = np.linspace(bins[0], bins[-1])
        ax.plot(dbins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp(- (dbins - mu)**2
                                                            / (2 * sigma**2)), linewidth=2, color='red')
        c = c.replace('_', ' ')
        title = f'{c[:35]}-\n{c[35:]}' if len(c) > 35 else c
        t = ax.set_title(title)
    plt.tight_layout()
    fig.savefig('./figures/household_gaussPlot')
    plt.clf()
    
   
def corr_plot(df):
    """
    Creates a correlation plot
    """
    plt.figure(figsize=(20, 20))
    ax=sns.heatmap(df.iloc[:,1:-1].corr(), annot=True)
    ax.set_title('Correlation heatmap household data source', fontdict={'fontsize':18}, pad=12)
    plt.tight_layout()
    plt.savefig('./figures/hosehold_corrPlot')
    plt.clf()

def data_quality_household(DB,df):
    """
    Executes all the household data quality done in the trusted zone
    """
    if not os.path.exists('./figures/'):
        os.makedirs('./figures/')
    gaussianity_plot(df)
    corr_plot(df)
    print('        - [Household] Profiling (incoherent values) done')
    print('        - [Household] Duplicates done')
    print('        - [Household] Missing values done')
    print('        - [Household] Outliers done')
    return df
    

## Nationalities - trusted zone
def remove_nat_duplicates(DB):
    """
    Treats the duplicated nationalities values
    """
    n2018 = utils.select_version(DB, 'nationalities', '2018')
    n2018 = n2018[n2018.columns.difference(['Belarús','República_Democrática_del_Congo' ])] 
    n2018 = n2018.rename(columns = {'Bielorrusia':'Belarús', 'República_Democrática_del_Cong':'República_Democrática_del_Congo'})  

    n2019 = utils.select_version(DB, 'nationalities', '2019')
    n2019 = n2019[n2019.columns.difference(['Bielorrusia','República_Democrática_del_Cong' ])] 

    n2020 = utils.select_version(DB, 'nationalities', '2020')
    n2020 = n2020[n2020.columns.difference(['Bielorrusia','República_Democrática_del_Cong' ])] 

    df =  pd.concat([n2018, n2019, n2020],ignore_index = True)
    utils.df_to_DBtable(DB,df, 'nationalitiesClean')
    return df


def data_quality_nationalities(DB, df):
    """
    Executes all the nationalities data quality done in the trusted zone
    """
    if not os.path.exists('./figures/'):
        os.makedirs('./figures/')
    print('        - [Nationalities] Profiling (incoherent values) done')
    df = remove_nat_duplicates(DB)
    print('        - [Nationalities] Duplicates done')
    print('        - [Nationalities] Missing values done')
    print('        - [Nationalities] Outliers done')
    return df

## MAIN
def main():
    print('\nSTART TRUSTED')
    print(' - Generating a single table from the different versions...')
    path = os.getcwd()

    DBh = f'{path}/household.duckdb'
    dfh = trusted_zone(DBh, 'household')
    print('    - All the ./household.duckdb tables are joined into a household table')
    print('    - Executing the data quality process...')
    data_quality_household(DBh, dfh)

    DBn = f'{path}/nationalities.duckdb'
    dfn = trusted_zone(DBn, 'nationalities')
    print('    - All the ./nationalities.duckdb tables are joined into a nationalities table')
    print('    - Executing the data quality process...')
    data_quality_nationalities(DBn,dfn)


