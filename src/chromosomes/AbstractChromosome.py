from abc import ABC, abstractmethod
from typing import List

# Esta es una clase abstracta por lo que los metodos definidos 
# en esta no tienen definida una logica, su proposito es ser
# utilizados en las extensiones de esta.
class AbstractChromosome(ABC):

    @abstractmethod
    def fitness(self) -> float:
        '''
        Se realizará la valoración del cromosoma.
        
        :param self: AbstractChromosome | Instancia de la clase a evaular.
        :return: Float | Valoración del cromosoma.
        '''
        pass

    @staticmethod
    @abstractmethod
    def crossover(parent1: 'AbstractChromosome', parent2: 'AbstractChromosome',
                  cross_rate: float) -> List['AbstractChromosome']:
        '''
        Generamos el cruce entre una pareja de cromosomas padres con
        la probabilidad recibida como parametro.
        Devolvemos dos cromosomas hijos cruzados si se da la probabilidad.
        En caso contrario devolvemos los dos padres.

        :param parent1: AbstractChromosome | Instancia del primer padre.  
        :param parent2: AbstractChromosome | Instancia del segundo padre. 
        :param cross_rate: float | Probabilidad de que ocurra el cruce.
        :return: List[AbstractChromosome] | Lista de cromosomas hijos cruzados con la 
        información de los padres o los padres en su defecto.
        '''
        pass

    @abstractmethod
    def mutate(self, mutation_rate: float) -> None:
        '''
        Generamos la mutación aleatoria de un cromosoma.
        
        :param self: AbstractChromosome | Instancia del cromosoma a mutar.
        :param mutation_rate: Float | Ratio de mutación.
        '''
        pass
        