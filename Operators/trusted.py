import duckdb
import pandas as pd

def df_to_DBtable(df,DB,table): # repeated
    """
    Creates a persistent table in DuckDB from the DataFrame content.
    """
    con = duckdb.connect(DB)
    con.register(table, df)
    con.execute(f'CREATE TABLE {table} AS SELECT * FROM {table}')
    con.close()

def DBtable_to_df(DB,table):
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

def pre_join(DB):
    """
    Adds a version (year) column to all `DB` tables in order to do the joining.
    Returns all the `DB` tables in data frame format.
    """
    tablesDB = get_tables(DB)
    dfs = []
    for table in tablesDB:
        year = ''.join(filter(str.isnumeric,table))
        df = DBtable_to_df(DB,table)
        df['Year'] = year
        dfs.append(df)
    return dfs

def trusted_zone(DB,table):
    """
    Joins all the `DB` tables into one and stores it in the `DB`.
    """
    dfs = pre_join(DB)
    df = pd.concat(dfs, axis=0, ignore_index=True)
    df_to_DBtable(df,DB,table)
