
import utils 
import os

def etl_household(dfh):
    """
    Integration and transforming of the household data to be joinable with the other 
    data source in the ETL-ish way.
    """
    dfh['section'] = dfh.section.astype('int32').astype('str')
    dfh['section'] = dfh.section.apply(lambda s: '0796' + s if len(s) == 5 else '07960' + s)
    dfh = dfh.rename(columns = {'section':'Madrid_section', 'habitantes':'suma de categorías de hogares'})  
    utils.df_to_DBtable(f'integration.duckdb',dfh, 'householdClean_Madrid')
    return dfh


def etl_nationalities(dfn):
    """
    Integration and transforming of the nationalities data to be joinable with the other 
    data source in the ETL-ish way.
    """
    dfn = dfn[dfn['Madrid_section'].str.contains('0796', regex=False)] 
    dfn = dfn.rename(columns = {'Habitantes':'suma de categorías de nacionalidad'}) 
    dfn['Madrid_section'] = dfn['Madrid_section'].str.strip() 
    utils.df_to_DBtable('integration.duckdb',dfn, 'nationalitiesClean_Madrid')
    return dfn


def explotation_zone(path):
    """
    Generates form two different data sources one table.
    """
    dfh = utils.DBtable_to_df(f'{path}/household.duckdb','household')
    dfn = utils.DBtable_to_df(f'{path}/nationalities.duckdb','nationalitiesClean')

    dfh = etl_household(dfh)
    dfn = etl_nationalities(dfn)

    df = dfh.merge(dfn, how='inner', on=["Madrid_section","Year"])
    return df


def main():
    print('\nSTART EXPLOTATION')

    path = os.getcwd()
    explotation_zone(path)
    print('  - Explotation zone finished')
