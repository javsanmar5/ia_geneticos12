# Trabajo realizado por: Javier Ruíz, Javier Santos 

from chromosomes.AbstractChromosome import AbstractChromosome 
from chromosomes.HousingChromosome import HousingChromosome
from ag.csv_reader import *

from typing import List, Tuple # Ayudas para documentacion
import random

class AG():
    
    def __init__(self, datos_train: str, datos_test: str, 
                    seed: int, nInd: int, maxIter: int,
                    mutation_rate: float = 0.01,
                    elitism_rate: float = 0.2,
                    selection_method: str = "elitism") -> None:
        
        random.seed(seed) # Generamos los números aleatorios con la semilla dada
        train_chromosomes = read_data(datos_train)

        # Asignamos las variables
        self.train_data:            str = datos_train
        self.test_data:             str = datos_test
        self.population_size:       int = nInd
        self.max_iterations:        int = maxIter

        self.mutation_rate:         float = mutation_rate
        self.elitism_rate:          float = elitism_rate
        self.selection_method:      str = selection_method

        self.population: List[AbstractChromosome] = random.sample(
            train_chromosomes, self.population_size)


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

    def run(self) -> AbstractChromosome:
        elitism_count = int(self.elitism_rate * self.population_size)
        for generation in range(self.max_iterations):
            self.population.sort(key=lambda chromo: chromo.fitness(), reverse=True)
            next_generation = []

            if self.selection_method == 'elitism':
                next_generation = self.population[:elitism_count]
                while len(next_generation) < self.population_size:
                    parent1, parent2 = self.tournament_selection(), self.tournament_selection()
                    offspring = parent1.crossover(parent2)
                    for child in offspring:
                        if len(next_generation) < self.population_size:
                            child.mutate(self.mutation_rate)
                            next_generation.append(child)
            
            elif self.selection_method == 'roulette':
                combined_population = self.population[:]
                while len(combined_population) < 2 * self.population_size:
                    parent1, parent2 = self.tournament_selection(), self.tournament_selection()
                    offspring = parent1.crossover(parent2)
                    for child in offspring:
                        child.mutate(self.mutation_rate)
                        combined_population.append(child)
                fitness_values = [chromosome.fitness() for chromosome in combined_population]
                total_fitness = sum(fitness_values)
                selection_probs = [fitness / total_fitness for fitness in fitness_values]
                next_generation = random.choices(combined_population, weights=selection_probs, k=self.population_size)

            self.population = next_generation
            best_fitness = self.population[0].fitness()
            print(f'Generation {generation}: Best Fitness = {best_fitness}')

        return max(self.population, key=lambda chromo: chromo.fitness())

    def tournament_selection(self, k: int = 3) -> AbstractChromosome:
        tournament = random.sample(self.population, k)
        tournament.sort(key=lambda chromo: chromo.fitness(), reverse=True)
        return tournament[0]
