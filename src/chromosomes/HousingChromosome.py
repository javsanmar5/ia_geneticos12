from chromosomes.AbstractChromosome import AbstractChromosome
import random
from typing import List

class HousingChromosome(AbstractChromosome):

    def __init__(self, features: List[float], target: float):

        self.features:  List[float]     = features
        self.target:    float           = target

        # Inicializamos los coeficientes aleatorios de manera uniforme para cada característica
        self.coefficients: List[float] = [random.uniform(-1, 1) for _ in range(len(features))]

    def fitness(self) -> float:
        predictions = [self.predict(self.features)]
        squared_errors = [(prediction - self.target) ** 2 for prediction in predictions]
        total_error = sum(squared_errors)
        return 1.0 / (1.0 + total_error)

    def predict(self, features: List[float]) -> float:
        
        return sum(coef * feature for coef, feature in zip(self.coefficients, features))

    def crossover(self, other: 'HousingChromosome') -> List['HousingChromosome']:

        point = random.randint(1, len(self.coefficients) - 1)
        child1_coefficients = self.coefficients[:point] + other.coefficients[point:]
        child2_coefficients = other.coefficients[:point] + self.coefficients[point:]
        return [HousingChromosome(self.features, self.target), 
                HousingChromosome(self.features, self.target)]

    def mutate(self, mutation_rate: float) -> None:
        self.coefficients = [coef if random.random() > mutation_rate else coef + random.uniform(-0.1, 0.1) for coef in self.coefficients]
