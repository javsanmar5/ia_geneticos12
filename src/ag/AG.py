# Trabajo realizado por: Javier Ruíz, Javier Santos 

from chromosomes.Chromosome import Chromosome
from ag.csv_reader import *
import time


from typing import List, Tuple # Ayudas para documentacion
import random

class AG():
    
    def __init__(self, datos_train: str, datos_test: str, 
                    seed: int, nInd: int, maxIter: int,
                    mutation_rate: float = 0.06,
                    cross_rate: float = 0.7,
                    elitism_rate: float = 0.3,
                    selection_method: str = "elitism") -> None:
        
        random.seed(seed) # Generamos los números aleatorios con la semilla dada

        # Asignamos las variables
        self.train_data:            str = read_data(datos_train)
        self.test_data:             str = read_data(datos_test)
        self.population_size:       int = nInd
        self.max_iterations:        int = maxIter

        self.mutation_rate:         float = mutation_rate
        self.cross_rate:            float = cross_rate
        self.elitism_rate:          float = elitism_rate
        self.selection_method:      str = selection_method

        self.population: List[Chromosome] = []
        for i in range(self.population_size):
            variables_amount = len(self.train_data[0]) - 1
            self.population.append(Chromosome(variables_amount=variables_amount))


    #     self.population: List[AbstractChromosome] = self.initialize_population(
    #         datos_train.split("_train.csv")[0], lambda: random.sample(train_chromosomes, self.population_size))


    # def initialize_population(self, file_prefix, *args) -> List[AbstractChromosome]:

    #     chromosome_classes = {
    #         # Añadir el resto de cromosomas
    #         'housing': HousingChromosome, 
    #         'synt1': None,
    #         'toy1': None
    #     }

    #     # Obtener el tipo de cromosoma basado en el nombre del archivo de datos
    #     chromosome_class = chromosome_classes.get(file_prefix, None)
    #     # Verificar si se encontró una clase de cromosoma
    #     if chromosome_class is None:
    #         raise ValueError(f"No se encontró una clase de cromosoma para el prefijo {file_prefix}")
        
    #     return [chromosome_class(args) for _ in range(self.population_size)]

    def run(self) -> Chromosome:
        '''
        Ejecuta el algoritmo genético y devuelve el cromosoma con la mejor aptitud encontrada después de todas las iteraciones.

        :param self: Instancia de la clase AG.
        :return: El cromosoma con la mejor aptitud encontrada, de tipo AbstractChromosome.
        '''

        #Cantidad de individuos que pasan directamente a la siguiente poblacion
        elitism_count = int(self.elitism_rate * self.population_size)
 
        for generation in range(self.max_iterations):
            #Ordena la poblacion de cromosomas seleccionados segun la funcion de fitness de mayor a menor
            self.population.sort(key=lambda chromo: chromo.fitness(self.train_data), reverse=False)
            next_generation = []

            if self.selection_method == 'elitism':
                #Añade en la siguiente generación los elitism_count elementos
                next_generation = self.population[:elitism_count]
                while len(next_generation) < self.population_size:
                    #Asigna a parent1 y parent2 los dos cromosomas ganadores del torneo
                    parent1, parent2 = self.tournament_selection(), self.tournament_selection()
                    #Se genera el cruce entra ambos padres, offspring contiene dos cromosomas hijos
                    offspring = parent1.crossover(parent2, self.cross_rate)
                    for child in offspring:
                        if len(next_generation) < self.population_size: 
                            #Para cada hijo, se somete a la probabilidad de ser mutado
                            child.mutate(self.mutation_rate)
                            next_generation.append(child)
            
            
            elif self.selection_method == 'roulette':
                combined_population = self.population[:]
                #En combined_population se añaden todos los individuos de la poblacion y todos sus hijos
                while len(combined_population) < 2 * self.population_size:
                    #Asigna a parent1 y parent2 los dos cromosomas ganadores del torneo
                    parent1, parent2 = self.tournament_selection(), self.tournament_selection()
                    #Se genera el cruce entra ambos padres, offspring contiene dos cromosomas hijos
                    offspring = parent1.crossover(parent2, self.cross_rate)
                    for child in offspring:
                        #Para cada hijo, se somete a la probabilidad de ser mutado
                        child.mutate(self.mutation_rate)
                        combined_population.append(child)
                #Se calcula la suma total de la funcion fitness de cada cromosoma de combined_population
                fitness_values = [chromosome.fitness(self.train_data) for chromosome in combined_population]
                total_fitness = sum(fitness_values)
                #Se calcula la probabilidad de cada cromosoma
                selection_probs = [fitness / total_fitness for fitness in fitness_values]
                #Se selecciona la siguiente generacion aleatoriamente teniendo en cuenta las probabilidades de cada cromosoma
                next_generation = random.choices(combined_population, weights=selection_probs, k=self.population_size)
                

            self.population = next_generation
            best_fitness = self.population[0].fitness(self.train_data)
            print(f'Generation {generation}: Best Fitness = {best_fitness}')

        winner_chromosome = min(self.population, key=lambda chromo: chromo.fitness(self.train_data))
        return winner_chromosome, self.test(winner_chromosome)

    def tournament_selection(self, k: int = 3) -> Chromosome:
        '''
        Toma una muestra aleatoria de k cromosomas de la poblacion y devuelve el cromosoma con la mejor aptitud
        
        :param self: Instancia de la clase AG
        :param k: Numero de cromosomas elegidos para el torneo, por defecto es 3.
        :return: Cromosoma con la mejor aptitud, de tipo Chromosome.
        '''

        tournament = random.sample(self.population, k)
        tournament.sort(key=lambda chromo: chromo.fitness(self.train_data), reverse=False)
        return tournament[0]
    

    def test(self, chromosome: Chromosome) -> List[float]:

        y_pred: List[float] = []

        for datum in self.test_data:
            predicted = chromosome.predict(datum)
            y_pred.append(predicted)
        
        return y_pred