

from landing import temporal_zone, persistent_zone
from formatted import formatted_zone
from trusted import trusted_zone, household, nationalities
from explotation import explotation_zone

def landing():
    print('\nSATART LANDING')
    print(' - Downloading data in the temporal zone...')
    temporal_zone()
    print(' - Moving the temporal data in the persistent zone...')
    return persistent_zone()


def formatted(path):
    print('\nSTART FORMATTED')
    print(' - Storing the data in a relational database...')
    formatted_zone(path)


def trusted(path):
    print('\nSTART TRUSTED')
    print(' - Generating a single table from the different versions...')

    DB = f'{path}/household.duckdb'
    df = trusted_zone(DB, 'household')
    print('    - All the ./household.duckdb tables are joined into a household table')
    print('    - Executing the data quality process...')
    household(DB,df)

    DB = f'{path}/nationalities.duckdb'
    df = trusted_zone(DB, 'nationalities')
    print('    - All the ./nationalities.duckdb tables are joined into a nationalities table')
    print('    - Executing the data quality process...')
    nationalities(DB,df)


def explotation(path):
    print('\nSTART EXPLOTATION')
    explotation_zone(path)
    print('  - Explotation zone finished')


if __name__ == '__main__':
    path = landing()
    formatted(path)
    trusted(path)
    explotation(path)
    print('\nEND OF THE PROGRAM')
    
    
