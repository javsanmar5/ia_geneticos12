from chromosomes.Chromosome import Chromosome
from typing import List, Tuple

import os

def read_data(filepath: str) -> List[Tuple[float]]:
    '''
    Lee el fichero csv y lo convierte en una lista de cromosomas
    
    :param filepath: Ruta del fichero a leer
    :return: Lista de cromosomas
    '''

    # Para evitar problemas de rutas relativas en distintos ordenadores y sistemas
    # utilizaremos la librería del sistema operativo
    current_dir = os.path.dirname(__file__)  # Directorio actual de csv_reader.py
    data_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'data'))

    if 'housing' in filepath:
        full_filepath = os.path.join(data_dir, filepath)
    elif 'synt1' in filepath:
        full_filepath = os.path.join(data_dir, filepath)
    elif 'toy1' in filepath:
        full_filepath = os.path.join(data_dir, filepath)
        pass
    else: # default
        raise ValueError("No existen esos datos de prueba.")
    
    with open(full_filepath, 'r') as file:
        
        lines = file.readlines()[1:]  # Saltar la cabecera
        data = []
        
        for line in lines:
            parts = tuple(map(float, line.strip().split(',')))
            features = parts[:-1]
            target = parts[-1]
            data.append(parts)

    return data
