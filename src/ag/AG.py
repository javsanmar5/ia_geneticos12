# Trabajo realizado por: Javier Ruíz, Javier Santos 

from chromosomes.Chromosome import Chromosome
from utils.csv_reader import *


from typing import List, Tuple # Ayudas para documentacion
import random

class AG():

    
    def __init__(self, datos_train: str, datos_test: str, seed: int, nInd: int, maxIter: int):

        random.seed(seed) # Generamos los números aleatorios con la semilla dada
        # Orden de los parametros: tasa de mutación, tango de mutación, tasa de cruce,
        # tasa de elitismo, rango inicial del cromosoma, porcentaje de datos, método.
        parameters = {
            "housing_data/housing_train.csv": (0.25, 0.6, 0.7, 0.2, 0.7, 0.1),
            "synt1_data/synt1_train.csv": (0.2, 0.4, 0.8, 0.1, 1., 0.2),
            "toy1_data/toy1_train.csv": (0.25, 0.6, 0.7, 0.2, 3., 1.)
        }

        # Asignamos las variables
        self.train_data:            str = read_data(datos_train)
        self.test_data:             str = read_data(datos_test)
        self.population_size:       int = nInd
        self.max_iterations:        int = maxIter

        self.mutation_rate:         float = parameters.get(datos_train)[0]
        self.mutation_range:        float = parameters.get(datos_train)[1]
        self.cross_rate:            float = parameters.get(datos_train)[2]
        self.elitism_rate:          float = parameters.get(datos_train)[3]
        self.initial_range:         float = parameters.get(datos_train)[4]
        self.data_percentage:       float = parameters.get(datos_train)[5]

        self.population: List[Chromosome] = [
            [Chromosome(variables_amount=len(self.train_data[0]) - 1, initial_range = self.initial_range)]
            for _ in range(self.population_size)
        ]


    def run(self) -> Chromosome:
        '''
        Ejecuta el algoritmo genético y devuelve el cromosoma con la mejor aptitud encontrada después de todas las iteraciones.

        :param self: Instancia de la clase AG.
        :return: El cromosoma con la mejor aptitud encontrada, de tipo AbstractChromosome.
        '''

        #Cantidad de individuos que pasan directamente a la siguiente poblacion
        elitism_count = int(self.elitism_rate * self.population_size)
        for generation in range(self.max_iterations):

            self.population = [[pair[0], pair[0].fitness(self.train_data, self.data_percentage)] for pair in self.population]
            #Ordena la poblacion de cromosomas seleccionados segun la funcion de fitness de mayor a menor
            # self.population.sort(key=lambda chromo: chromo.fitness(self.train_data), reverse=False)
            self.population = (sorted(self.population, key=lambda x:x[1]))

            #Añade en la siguiente generación los elitism_count elementos
            next_generation = [[pair[0]] for pair in self.population[:elitism_count]]
            while len(next_generation) < self.population_size:
                #Asigna a parent1 y parent2 los dos cromosomas ganadores del torneo
                parent1, parent2 = self.tournament_selection(), self.tournament_selection()
                #Se genera el cruce entra ambos padres, offspring contiene dos cromosomas hijos
                offspring = parent1[0].crossover(parent2[0], self.cross_rate)
                for child in offspring:
                    if len(next_generation) < self.population_size: 
                        #Para cada hijo, se somete a la probabilidad de ser mutado
                        child.mutate(self.mutation_rate, self.mutation_range)
                        next_generation.append([child])
            

            best_fitness = self.population[0][1]
            self.population = next_generation
            print(f'Generation {generation}: Best Fitness = {best_fitness}')

        winner_chromosome = min(self.population, key=lambda chromo: chromo[0].fitness(self.train_data, self.data_percentage))[0]
        
        return winner_chromosome, self.test(winner_chromosome)

    def tournament_selection(self, k: int = 3) -> Chromosome:
        '''
        Toma una muestra aleatoria de k cromosomas de la poblacion y devuelve el cromosoma con la mejor aptitud
        
        :param self: Instancia de la clase AG
        :param k: Numero de cromosomas elegidos para el torneo, por defecto es 3.
        :return: Cromosoma con la mejor aptitud, de tipo Chromosome.
        '''
        tournament = random.sample(self.population, k)
        # tournament.sort(key=lambda chromo: chromo.fitness(self.train_data), reverse=False)
        sorted_tournament = sorted(tournament, key=lambda x:x[1])

        return sorted_tournament[0]
    

    def test(self, chromosome: Chromosome) -> List[float]:

        y_pred: List[float] = []

        for datum in self.test_data:
            predicted = chromosome.predict(datum)
            y_pred.append(predicted)
        
        return y_pred