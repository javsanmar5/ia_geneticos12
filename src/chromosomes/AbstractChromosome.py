from abc import ABC, abstractmethod
from typing import List

# Esta es una clase abstracta por lo que los metodos definidos 
# en esta no tienen definida una logica, su proposito es ser
# utilizados en las extensiones de esta clase abstracta.
class AbstractChromosome(ABC):

    @abstractmethod
    def fitness(self) -> float:
        '''
        Se realizará la valoración del cromosoma
        
        :param self: Cromosoma a evaular
        :return: Valoración del cromosoma, double.
        '''
        pass

    @abstractmethod
    def crossover(self, to_cross_with: 'AbstractChromosome') -> List['AbstractChromosome']:
        '''
        Generamos el cruce entre una pareja de cromosomas

        :param self: Cromosoma al que se le aplica el cruce  
        :param to_cross_with: Cromosoma con el que se cruza 
        :return: Lista de cromosomas cruzados
        '''
        pass

    @abstractmethod
    def mutate(self, mutation_rate: float) -> None:
        '''
        Generamos la mutación aleatoria de un cromosoma
        
        :param self: Cromosoma a mutar.
        :param mutation_rate: Ratio de mutación.
        '''
        pass


    # No sé si será necesario el uso de estos dos métodos:
    # @abstractmethod
    # def to_genotype(self) -> List[float]:
    #     pass

    # @abstractmethod
    # def from_genotype(self, genotype: List[float]) -> None:
    #     pass
        