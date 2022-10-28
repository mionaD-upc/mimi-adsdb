import os
import requests
import shutil
from datetime import date

DATA = {
    'household2018.xls':'https://datos.madrid.es/egob/catalogo/300438-9-hogares-tama%C3%B1o.xls',
    'household2019.xls':'https://datos.madrid.es/egob/catalogo/300438-10-hogares-tama%C3%B1o.xls',
    'household2020.xls':'https://datos.madrid.es/egob/catalogo/300438-11-hogares-tama%C3%B1o.xls',
    'nationalities2018.xls':'https://www.madrid.org/iestadis/fijas/estructu/demograficas/padron/descarga/pc18t18z4_secci.xls',
    'nationalities2019.xls':'https://www.madrid.org/iestadis/fijas/estructu/demograficas/padron/descarga/pc19t19z4_secci.xls',
    'nationalities2020.xls':'https://www.madrid.org/iestadis/fijas/estructu/demograficas/padron/descarga/pc20t20z4_secci.xls',  
}

def temporal_zone():
    """
    Creates the `temporal` folder and downloads the data if does not exist.
    Returns the folder path
    """
    if not os.path.exists('./temporal'): 
        os.makedirs('./temporal')

    for file, url in DATA.items():
        if not os.path.exists(f'./temporal/{file}'):
            data_request = requests.get(url)
            open(f'./temporal/{file}', 'wb').write(data_request.content)
            print(f'    - ./temporal/{file} downloaded')

    return os.path.abspath('.')



def persistent_zone():
    """
    Creates the `persistent` folder and copies the temporary file to the persistent storage
    adding the current date in the file name.
    Returns the folder path
    """
    if not os.path.exists('./persistent'): 
        os.makedirs('./persistent')
    
    today = date.today()
    for file in list(DATA.keys()): 
        source = f'./temporal/{file}'
        destination = f'./persistent/{today}_{file}'
        shutil.copy(source,destination)
        print(f'    - {destination} copied')  
    
    return os.path.abspath('.')

