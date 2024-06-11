#####################################
#                                   #
#      Trabajo realizado por:       #
#    Javier Ruíz y Javier Santos    #
#                                   #
#   uvus: javruigar2; javsanmar5    #
#                                   #
#####################################

from chromosomes.Chromosome import Chromosome
from utils.csv_reader import *
from typing import List 

import random

class AG():

    
    def __init__(self, datos_train: str, datos_test: str, seed: int, nInd: int, maxIter: int,
                 **kwargs) -> None:
        '''
        Creamos la instancia del algoritmo genético con los parámetros seleccionados.
        También se puede modificar cualquier otro parámetro del algoritmo especificándolo
        en el constructor vía: **kwargs, estas opciones son:
        - mutation_rate: Tasa de mutación.
        - mutation_range: Rango de mutación.
        - initial_range: Rango de valores iniciales.
        - cross_rate: Tasa de cruce.
        - elitism_rate: Tasa de elitismo.
        Todos estos valores deben ser asignados como float.

        :param datos_train: String | Fichero de entrenamiento.
        :param datos_test: String | Fichero de testeo.
        :param seed: Integer | Semilla para la aleatorización.
        :param nInd: Integer | Número de inviduos de la población.
        :param maxIter: Integer | Número máximo de iteraciones.
        '''


        random.seed(seed) # Generamos los números aleatorios con la semilla dada

        # Variables recibidas como parámetro
        self.train_data:            str = read_data(datos_train)
        self.test_data:             str = read_data(datos_test)
        self.population_size:       int = nInd
        self.max_iterations:        int = maxIter

        # Variables seleccionadas para el algoritmo. Estos valores también pueden ser 
        # pasados como parámetro. 
        self.mutation_rate:         float = kwargs.get('mutation_rate', 0.2)
        self.mutation_range:        float = kwargs.get('mutation_range', 0.6)
        self.initial_range:         float = kwargs.get('initial_range', 1.0)
        self.cross_rate:            float = kwargs.get('cross_rate', 0.7)
        self.elitism_rate:          float = kwargs.get('elitism_rate', 0.2)

        self.population: List[List[Chromosome, float]] = [
            [Chromosome(variables_amount=len(self.train_data[0]) - 1, 
                        initial_range=self.initial_range)]
            for _ in range(self.population_size)
        ]


    def run(self) -> Tuple[Chromosome, List[float]]:
        '''
        Algoritmo genético en el que se seleccionan el mejor cromosoma para resolver 
        el problema dado. Este proceso se repite max_iterations veces

        :param self: AG | Instancia de la clase AG.
        :return: Tuple[Chromosome, List[Float]] | El cromosoma con la mejor aptitud 
        encontrada y una predicción para cada dato del conjunto de prueba.
        '''

        # Cantidad de individuos que pasan directamente a la siguiente poblacion.
        elitism_count = int(self.elitism_rate * self.population_size)
        for generation in range(self.max_iterations):

            # Modificamos la población añadiendo la valoración de cada cromosoma.
            self.population = [[pair[0], pair[0].fitness(self.train_data)] for pair in self.population]
            # Ordena la poblacion de cromosomas seleccionados segun la funcion de fitness de mayor a menor
            self.population = (sorted(self.population, key=lambda x:x[1]))

            # Añade en la siguiente generación los elitism_count elementos
            next_generation = [[pair[0]] for pair in self.population[:elitism_count]]
            while len(next_generation) < self.population_size:
                # Asigna a parent1 y parent2 los dos cromosomas ganadores del torneo
                parent1, parent2 = self.tournament_selection(), self.tournament_selection()
                # Se genera el cruce entra ambos padres, offspring contiene dos cromosomas hijos
                offspring = Chromosome.crossover(parent1[0], parent2[0], self.cross_rate)
                for child in offspring:
                    if len(next_generation) < self.population_size: 
                        # Para cada hijo, se somete a la probabilidad de ser mutado
                        child.mutate(self.mutation_rate, self.mutation_range)
                        next_generation.append([child])
            

            best_fitness = self.population[0][1]
            self.population = next_generation
            print(f'Generación {generation}: Mejor RMSE obtenido = {best_fitness}')

        winner_chromosome = min(self.population, key=lambda chromo: chromo[0].fitness(self.train_data))[0]
        
        return winner_chromosome, self.test(winner_chromosome)


    def tournament_selection(self, k: int = 3) -> Chromosome:
        '''
        Toma una muestra aleatoria de k cromosomas de la poblacion y 
        devuelve el cromosoma con la mejor aptitud.
        
        :param self: Instancia de la clase AG
        :param k: Numero de cromosomas elegidos para el torneo, por defecto es 3.
        :return: Cromosoma con la mejor aptitud, de tipo Chromosome.
        '''
        tournament = random.sample(self.population, k)

        # Devolvemos el cromosoma con menor fitness, es decir, menor RMSE.
        return min(tournament, key = lambda x:x[1])
    

    def test(self, chromosome: Chromosome) -> List[float]:
        '''
        Proceso de testeo del cromosoma ganador con el conjunto de datos de prueba.

        :param self: AG | Instancia de la clase AG.
        :param chromosome: Chromosome | Cromosoma ganador.
        :return: List[Float] | Lista de valores predichos.
        '''

        # En este caso, al solo tener que calcular una lista, utilizamos comprensión
        # (a diferencia del método fitness).
        return [chromosome.predict(datum) for datum in self.test_data]