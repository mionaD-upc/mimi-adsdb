import pandas as pd
import utils
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

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
def gaussianity_plot(df, repo): 
    """
    Creates a gaussian plot
    """  
    fig, axes = plt.subplots(6, 4, figsize=(15, 15))
    col = df.columns[1:-1] if repo == 'household' else df.columns[0:24]
    for i, c in enumerate(col):
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
    fig.savefig(f'./figures/{repo}_gaussPlot')
    plt.clf()
    
   
def corr_plot(df, repo):
    """
    Creates a correlation plot
    """
    plt.figure(figsize=(20, 20))
    col = df.iloc[:,1:-1].corr() if repo == 'household' else df.iloc[:,0:20].corr()
    ax=sns.heatmap(col, annot=True)
    ax.set_title('Correlation heatmap household data source', fontdict={'fontsize':18}, pad=12)
    plt.tight_layout()
    plt.savefig(f'./figures/{repo}_corrPlot')
    plt.clf()

def missing_plot(df):
    """
    Creates a missing values plot
    """
    dftmp = df.replace(0,np.nan)
    count = dftmp.isnull().mean()

    fig, ax = plt.subplots(figsize =(20, 20))
    ax.barh(df.columns,count)

    for s in ['top', 'bottom', 'left', 'right']: # Remove axes splines
        ax.spines[s].set_visible(False)

    for i in ax.patches: # Add annotation to bars
        plt.text(i.get_width()+0.02, i.get_y()+0.4, str(round((i.get_width()), 3)), fontsize = 15, fontweight ='bold')

    ax.set_title('Percentage of missing values', loc ='left', fontsize=18,fontweight='bold' )
    ax.tick_params(axis = 'both', labelsize=15)
    plt.tight_layout()
    fig.savefig('./figures/household_missings')
    plt.clf()

def outliers_plot(df,repo):
    """
    Creates a distribution plots
    """
    fig, axes = plt.subplots(6, 4, figsize=(15, 15))
    col = df.columns[1:-1] if repo == 'household' else df.columns[0:24]
    for i, c in enumerate(col):
        ax = axes.reshape(-1)[i]
        sns.distplot(df[c],ax=ax)

        c = c.replace('_', ' ')
        title = f'{c[:35]}-\n{c[35:]}' if len(c) > 35 else c
        t = ax.set_title(title)
        ax.set(xlabel=None)  # remove the axis label
    plt.tight_layout()
    fig.savefig(f'./figures/{repo}_distribution')
    plt.clf()

def boxplot(df,repo):
    """
    Crates a boxplot plots
    """
    fig, axes = plt.subplots(6, 4, figsize=(15, 15))
    col = df.columns[1:-1] if repo == 'household' else df.columns[0:24]
    for i, c in enumerate(col):
        ax = axes.reshape(-1)[i]
        sns.boxplot(df[c],ax=ax)

        c = c.replace('_', ' ')
        title = f'{c[:35]}-\n{c[35:]}' if len(c) > 35 else c
        t = ax.set_title(title)
    plt.tight_layout()
    fig.savefig(f'./figures/{repo}_boxplot')
    plt.clf()


def data_quality_household(DB,df):
    """
    Executes all the household data quality done in the trusted zone
    """
    if not os.path.exists('./figures/'):
        os.makedirs('./figures/')
    gaussianity_plot(df, 'household')
    corr_plot(df, 'household')
    print('        - [Household] Profiling (incoherent values) done')
    print('        - [Household] Duplicates done')
    missing_plot(df)
    print('        - [Household] Missing values done')
    outliers_plot(df,'household')
    boxplot(df, 'household')
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

def kde_plot(df,a1):
    sns.kdeplot(data = df[a1])
    plt.xlabel(a1, size=12)    
    plt.ylabel("Frequency", size=12)                
    plt.grid(True, alpha=0.3, linestyle="--")     
    plt.tight_layout()
    plt.savefig(f'./figures/nationalities_KDE_{a1}')
    plt.clf()

def data_quality_nationalities(DB, df):
    """
    Executes all the nationalities data quality done in the trusted zone
    """
    if not os.path.exists('./figures/'):
        os.makedirs('./figures/')

    df = remove_nat_duplicates(DB)
    print('        - [Nationalities] Duplicates done')

    gaussianity_plot(df,'nationalities')
    corr_plot(df,'nationalities')
    kde_plot(df,'Extranjeros')
    kde_plot(df,'Españoles')
    print('        - [Nationalities] Profiling (incoherent values) done')

    nas = df.loc[:, df.isnull().any()].columns.tolist()
    for col in nas:
        df[col]=df[col].fillna(0)
    utils.df_to_DBtable('nationalities.duckdb', df, 'nationalitiesClean')
    print('        - [Nationalities] Missing values done')

    outliers_plot(df, 'nationalities')
    boxplot(df, 'nationalities')
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


