
import duckdb
import os, sys 
from pathlib import Path


def clear_datebase(path):
    print(path)
    dbFileName = path + '/household.duckdb' 
    if(os.path.exists(dbFileName)):
        os.remove(dbFileName)
    dbFileName = path + '/nationalities.duckdb'  
    if(os.path.exists(dbFileName)):
        os.remove(dbFileName)
    dbFileName = path + '/integration.duckdb'
    if(os.path.exists(dbFileName)):
        os.remove(dbFileName)
    dbFileName = path + '/household.duckdb.wal'
    if(os.path.exists(dbFileName)):
        os.remove(dbFileName)
    dbFileName =  path + '/nationalities.duckdb.wal'
    if(os.path.exists(dbFileName)):
        os.remove(dbFileName)
    dbFileName = path +  '/integration.duckdb.wal'
    if(os.path.exists(dbFileName)):
        os.remove(dbFileName)


def df_to_DBtable(DB,df,table):
  
    """
    Creates a persistent table in DuckDB from the DataFrame content.
    """

    con = duckdb.connect(DB)
    con.register(table, df)
    con.execute(f'CREATE TABLE {table} AS SELECT * FROM {table}')
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