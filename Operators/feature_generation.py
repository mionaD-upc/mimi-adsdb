import utils 
import os
import numpy as np
from sklearn.model_selection import train_test_split

def data_exploration(df,x = 1):
    """
    Shows the nationalities that have more than `x`% of the total population
    the rest are shown in a new feature called Others.
    """
    cols = list(range(22, df.shape[1]))
    cols[0] =  df.columns.get_loc('Madrid_section') 

    nat = df.iloc[:,cols]
    nat.set_index('Madrid_section', inplace = True)
    nat.loc['Total (%)'] = round((nat.iloc[:,1:].sum()/(nat.iloc[:,1:].sum()).sum()) * 100,3)

    dfn = (nat.loc[:, nat.loc['Total (%)'] >= x])
    dfn['Others'] = (nat.loc[:, nat.loc['Total (%)'] < x]).sum(axis = 1)
    return df


def clean_integration(path):
    """
    Cleans the integrated df, adding a new feature called `Extranjeros` which 
    includes all nationalities except `Españoles`.
    """
    df = utils.DBtable_to_df(f'{path}/integration.duckdb','integratedTable')
    df['Extrangeros'] = (df.iloc[:,24:].drop(columns=['Españoles'])).sum(axis=1)
    df = df.drop(df.iloc[:,24:-1],axis = 1)
    utils.df_to_DBtable('../integration.duckdb',df, 'integratedTable')
    return df


def splitting(df):
    """
    Splits the data source into train and test sets and stores them.
    """
    np.random.seed(144)
    X = df[df.columns[:-1].tolist()] # features
    y = df['Extrangeros'] # target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0) # 70% training and 30% test
    print(f'    - Training cases: {X_train.shape[0]}')
    print(f'    - Test cases: {X_test.shape[0]}')

    print(' - Storing the splitted data...')
    if not os.path.exists('./analysis'): 
        os.makedirs('./analysis')
    X_train.to_pickle('./analysis/data-X_train.pkl.bz2',compression='bz2')
    y_train.to_pickle('./analysis/data-y_train.pkl.bz2',compression='bz2')
    X_test.to_pickle('./analysis/data-X_test.pkl.bz2',compression='bz2')
    y_test.to_pickle('./analysis/data-y_test.pkl.bz2',compression='bz2')


def main():
    print('\nSTART FEATURE GENERATION')
    path = os.getcwd()
    # data_exploration(path)
    print(' - Classifying nationalities into Extranjeros or Españoles..')
    df = clean_integration(path)
    print(' - Splitting data into train and test..')
    splitting(df)
