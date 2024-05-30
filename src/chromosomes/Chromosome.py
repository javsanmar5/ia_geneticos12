from chromosomes.AbstractChromosome import AbstractChromosome
import random
from typing import List

class Chromosome(AbstractChromosome):

    def __init__(self, features: List[float], target: float, 
                 chromosome: List[float] = None) -> None:
        '''
        La idea del cromosoma es ser una lista de tamaño 2*n
        donde n es el numero de features (características).
        Los valores con índice par serán los coeficientes y
        los valores con índice impar los exponentes.

        De esta forma, la posición 2i será el coeficiente de
        la feature i y la posicion 2i + 1 será su exponente.
        
        Inicialmente numeros aleatorios entre -3 y 3.
        '''

        self.features:  List[float]     = features
        self.target:    float           = target

        if chromosome is None:
            self.chromosome: List[float]= [random.uniform(-3,3) for _ in range(2 * len(features))]
        else:
            self.chromosome: List[float]= chromosome
        

    def fitness(self) -> float:
        # Valoraremos al cromosoma como la inversa de la distancia
        # entre el valor predicho y el target. 
        # Esta distancia la calcularemos con el MSE visto en la asignatura,
        # en este caso, la diferencia entre target y predicted al cuadrado.
        
        predicted:  float = self.__predict()
        # print(f"{self.target} -> {predicted}")
        
        error:      float = (self.target - predicted) ** 2 

        # print(1 / error)
        return 1 / error

    def __predict(self) -> float:
        '''
        El valor predicho será la suma de c[i](x[i]**e[i]) donde:

        x[i]: son las distintas features de la lista self.features.
        c[i]: son los coeficientes del cromosoma. Posiciones pares.
        e[i]: son los exponentes del cromosoma. Posiciones impares. 
        '''

        # OPCION 1
        prediction: float = 0.

        for i in range(len(self.features)):

            while type(self.features[i] ** self.chromosome[2*i + 1]) == complex:
                self.chromosome[2*i + 1] *= random.random() # Puede ser que no funcione por esto
                
            prediction += self.chromosome[2*i] * (self.features[i] ** self.chromosome[2*i + 1])
            
        return prediction
    
        # OPCION 2
        # return sum(self.chromosome[2*i] * (self.features[i] ** self.chromosome[2*i + 1]) 
        #            for i in range(len(self.features)))
    


    def crossover(self, chromosomeToCrossWith: 'Chromosome', 
                  cross_rate: float,) -> List['Chromosome']:
        # La idea es mezclar dos cromosomas dados, eligiendo 
        # el punto de cruce de manera aleatoria.
        # Una vez escogemos el punto, creamos dos hijos eligiendo
        # una parte del cromosoma de cada padre.
        # Para calcular cuando cruzar utilizaremos una tasa de cruce entre 
        # 0 y 1, escogemos un número aleatorio, también entre 0 y 1, y la
        # probabilidad de que este número sea menor que la tasa es exactamente 
        # la tasa. Por tanto, cuando sea mayor debemos devolver los cromosomas 
        # sin cruzar

        if random.random() > cross_rate:
            return [self, chromosomeToCrossWith]

        point = random.randint(1, len(self.chromosome) - 1) # Escogemos el punto de cruce

        child1_chromosomes = self.chromosome[:point] + chromosomeToCrossWith.chromosome[point:]
        child2_chromosomes = chromosomeToCrossWith.chromosome[:point] + self.chromosome[point:]
        
        return [Chromosome(self.features, self.target, child1_chromosomes),
                Chromosome(chromosomeToCrossWith.features, chromosomeToCrossWith.target, child2_chromosomes)]


    def mutate(self, mutation_rate: float) -> None:
        # Debemos mutar o no aleatoriamente el cromosoma en el que estamos.
        # Esta mutación será alterar, también con números aleatorios, los 
        # valores del cromosoma.
        # Para calcular cuando mutar utilizaremos una tasa de mutación entre 
        # 0 y 1, escogemos un número aleatorio, también entre 0 y 1, y la
        # probabilidad de que este número sea menor que la tasa es exactamente 
        # la tasa.
        
        random_number = random.random() # Generamos un numero aleatorio entre 0 y 1
        if random_number < mutation_rate: 
            self.chromosome = [value + random.uniform(-0.1, 0.1) for value in self.chromosome]
