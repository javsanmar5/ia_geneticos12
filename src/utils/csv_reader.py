#####################################
#                                   #
#      Trabajo realizado por:       #
#    Javier Ruíz y Javier Santos    #
#                                   #
#   uvus: javruigar2; javsanmar5    #
#                                   #
#####################################

from typing import List, Tuple

import os

def read_data(filepath: str) -> List[Tuple[float]]:
    '''
    Lee el fichero csv y lo convierte en una lista de tuplas 
    para poder trabajar con los datos de forma cómoda.
    La lista resultante está compuesta por tuplas en la que
    cada tupla es un dato del conjunto y sus valores son floats.
    
    :param filepath: String | Ruta del fichero a leer.
    :return: List[Tuple[Float]] | Lista de datos parseados.
    '''

    # Para evitar problemas de rutas relativas en distintos ordenadores y sistemas
    # utilizaremos la librería del sistema operativo
    current_dir = os.path.dirname(__file__)  # Directorio en el que nos encontramos
    data_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'data'))
    full_filepath = os.path.join(data_dir, filepath)

    try:
        with open(full_filepath, 'r') as file:
            
            lines = file.readlines()[1:]  # Saltar la cabecera
            data = []
            
            for line in lines:
                parts = tuple(map(float, line.strip().split(',')))
                data.append(parts)

    except: # Controlar error en caso de no contar con los datos a leer
        raise ValueError(f"No contamos con los datos {filepath[:filepath.find("_data")]} de momento.")

    return data
