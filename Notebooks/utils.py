
import duckdb
import os
import pandas as pd
from sklearn import metrics
import numpy as np

def clear_database(path):
    """
    Clears all the duckdb files generated 
    in the path location
    """
    for item in os.listdir(path):
        if ".duckdb" in item:
            os.remove(f'{path}/{item}')


def df_to_DBtable(DB,df,table):
    """
    Creates or replace a persistent table in DuckDB from the DataFrame content.
    """
    con = duckdb.connect(DB)
    con.register(table, df)
    con.execute(f'CREATE OR REPLACE TABLE {table} AS SELECT * FROM {table}')
    con.close()


def DBtable_to_df(DB, table):
    """
    Converts the DB `table` in a data frame format 
    """
    con = duckdb.connect(DB)
    df = con.execute(f'SELECT * FROM {table}').df()
    con.close()
    return df


def get_tables(DB):
    """
    Gets all the tables from the `DB`
    """
    con = duckdb.connect(DB)
    tables = con.execute(f'SELECT table_name FROM information_schema.tables').df()['table_name']
    con.close()
    return tables


def select_version(DB,table,version):
    """
    Selects a specific version (verion) of the table
    """
    con = duckdb.connect(DB)
    df = con.execute(f"SELECT *  FROM {table} WHERE  Year = {version}").df()
    con.close()
    return df


def load_data(path):
    """
    Loads the train and test data
    """
    X_train = pd.read_pickle(f'{path}/data-X_train.pkl.bz2', compression='bz2')
    y_train = pd.read_pickle(f'{path}/data-y_train.pkl.bz2', compression='bz2')
    X_test  = pd.read_pickle(f'{path}/data-X_test.pkl.bz2', compression='bz2')
    y_test  = pd.read_pickle(f'{path}/data-y_test.pkl.bz2', compression='bz2')
    return X_train, X_test, y_train, y_test


def regression_results(y_true, y_pred):
    """
    Reports regressor metrics to evaluate the model
    """
    explained_variance = metrics.explained_variance_score(y_true, y_pred)
    mae = metrics.mean_absolute_error(y_true, y_pred) 
    mse = metrics.mean_squared_error(y_true, y_pred) 
    print('  - Explained variance: ', round(explained_variance,4))    
    print('  - MAE: ', round(mae,4))
    print('  - MSE: ', round(mse,4))
    print('  - RMSE: ', round(np.sqrt(mse),4))