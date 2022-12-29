
import duckdb
import os


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
