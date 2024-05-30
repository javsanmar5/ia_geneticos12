from chromosomes.HousingChromosome import HousingChromosome
from chromosomes.AbstractChromosome import AbstractChromosome
from typing import List

import os

def read_data(filepath: str) -> List[AbstractChromosome]:
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
        full_filepath = os.path.join(data_dir, 'housing_data', filepath)
        return read_housing_data(full_filepath)
    elif 'synt1' in filepath:
        full_filepath = os.path.join(data_dir, 'synt1_data', filepath)
        pass
    elif 'toy1' in filepath:
        full_filepath = os.path.join(data_dir, 'toy1_data', filepath)
        pass
    else: # default
        raise ValueError("No existen esos datos de prueba.")



def read_housing_data(full_filepath: str) -> List[HousingChromosome]:
    
    with open(full_filepath, 'r') as file:
        
        lines = file.readlines()[1:]  # Saltar la cabecera
        chromosomes = []
        
        for line in lines:
            parts = list(map(float, line.strip().split(',')))
            features = parts[:-1]
            target = parts[-1]
            chromosomes.append(HousingChromosome(features, target))
            
    return chromosomes

def read_synt1_data(filepath: str) -> List[str]: # Cambiar lo que devuelve a la lista correcta
    pass

def read_toy1_data(filepath: str) -> List[str]: # Cambiar lo que devuelve a la lista correcta
    pass
