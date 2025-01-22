#####################################
#                                   #
#      Trabajo realizado por:       #
#    Javier Ruíz y Javier Santos    #
#                                   #
#   uvus: javruigar2; javsanmar5    #
#                                   #
#####################################

from chromosomes.AbstractChromosome import AbstractChromosome
from sklearn.metrics import root_mean_squared_error
from typing import List, Tuple

import random


class Chromosome(AbstractChromosome):

    def __init__(self, coefficients: List[float] = None, exponents: List[float] = None, 
                 variables_amount: int = 0, initial_range: float = 1.) -> None:
        '''
        Constructor del cromosoma. Existen dos formas de construir un cromosoma:
        - Inicio: Primeros cromosomas, se establecen con números aleatorios contenidos
        en el rango (-initial_range, initial_range). Contamos con n exponentes y n+1
        coeficientes, donde n = variables_amount.
        - Tras proceso de cruce: Recibimos como parametros los coeficientes y exponentes
        que debe poseer nuestro cromosoma.

        :param self: Chromosome | Instancia a crear.
        :param coefficientes: List[Float] | Lista de coeficientes para establecer como 
        self.coefficients.
        :param exponents: List[Float] | Lista de exponentes para establecer como 
        self.exponents.
        :param variables_amount: Integer | Número de variables que tiene el problema al
        que aplicar regresión.
        :param initial_range: Float | Rango de valores que puede adoptar el cromosoma inicialmente.
        '''

        # Primera opción: no recibimos coeficientes ni exponentes. Caso inicial.
        if coefficients is None and exponents is None:
            # Establecemos tanto coeficientes como exponentes con números aleatorios dentro del rango.
            self.coefficients:  List[float] = [random.uniform(-initial_range, initial_range) 
                                               for _ in range(variables_amount + 1)]
            self.exponents:     List[float] = [random.uniform(-initial_range, initial_range) 
                                               for _ in range(variables_amount)]
        
        # En caso contrario, asignamos los coeficientes y los exponentes recibidos.
        else:
            self.coefficients:  List[float] = coefficients
            self.exponents:     List[float] = exponents
                

    def fitness(self, train_data: List[Tuple[float]]) -> float:
        # Función encargada de valorar un cromosoma, para ello calculará el RMSE 
        # entre los valores predichos y los valores esperados, utilizamos predict()
        # establecemos un valor máximo de datos para aumentar la eficiencia, en este
        # caso 500. El subconjunto de prueba irá variando de forma aleatoria.

        # Declaramos las dos listas. No lo realizamos con listas por comprensión 
        # para utilizar un mismo bucle para ambas. 
        predicted: List[float] = []
        expected: List[float] = []

        subset = random.sample(train_data, min(len(train_data), 500))

        for datum in subset:
            predicted.append(self.predict(datum)) # Agregamos la predicción para un dato.
            expected.append(datum[-1]) # Agregamos el último valor de los datos, la y.

        # Utilizamos la función de sklearn para calcular el RMSE.
        rmse = root_mean_squared_error(expected, predicted)
        
        return rmse
    
    
    def predict(self, datum: Tuple[float]) -> float:
        '''
        Cada predicción se calcula sobre un dato del conjunto.
        Esta predicción se calcula como sum(c[j] * (x[j] ** e[j])) + c[n]
        con j perteneciente al intervalo [0, n]; n = número de variables.
        donde: 
            - c[j] = Coeficiente.
            - x[j] = Variable.
            - e[j] = Exponente.

        :param self: Chromosome | Cromosoma con el que aplicar la predicción.
        :param datum: Tuple[Float] | Datos sobre el que aplicar la predicción.
        :return: Float | Predicción
        '''
        prediction: float = 0.

        for j in range(len(datum) - 1):

            # Si la base es 0 y el exponente negativo obtenemos una indeterminación.
            # Por ello, en este caso, nos quedamos con la parte positiva.
            if datum[j] == 0.:
                self.exponents[j] = abs(self.exponents[j])
            
            # Para solucionar el problema de obtener números complejos trabajamos con el
            # módulo del número complejo y el signo de la base. Toda la explicación de este
            # proceso y el por qué de este en la documentación.
            power_term = abs(datum[j] ** self.exponents[j]) if datum[j] > 0 else -abs(datum[j] ** self.exponents[j])
            
            prediction += self.coefficients[j] * power_term

        prediction += self.coefficients[-1] # Agregamos el término independiente.
        return prediction
    

    @staticmethod
    def crossover(parent1: 'Chromosome', parent2: 'Chromosome', 
                  cross_rate: float) -> List['Chromosome']:
        # Generamos un número aleatorio entre 0 y 1, y la probabilidad de que
        # este número sea menor que la tasa de cruce es la propia tasa de cruce.

        # Si el número es menor que la tasa: generamos un punto aleatorio al que 
        # llamamos punto de cruce. Y creamos dos hijos con las mitades de sus dos
        # padres intercambiadas.

        # Si el número aleatorio es mayor devolvemos a los padres sin cruzar.
        if random.random() > cross_rate:
            return [parent1, parent2]

        point = random.randint(1, len(parent1.exponents) - 1) # Escogemos el punto de cruce.

        #Establecemos el primer hijo, con la primera mitad de uno y la segunda mitad del otro.
        child1_coefficients = parent1.coefficients[:point] + parent2.coefficients[point:] 
        child1_exponents = parent1.exponents[:point] + parent2.exponents[point:] 
        
        #Establecemos el segundo hijo, con las mitades opuestas al primer hijo.
        child2_coefficients = parent2.coefficients[:point] + parent1.coefficients[point:]
        child2_exponents = parent2.exponents[:point] + parent2.exponents[point:]
        
        return [Chromosome(child1_coefficients, child1_exponents),
                Chromosome(child2_coefficients, child2_exponents)]


    def mutate(self, mutation_rate: float, mutation_range: float) -> None:
        # Generamos un número aleatorio entre 0 y 1, y la probabilidad de que
        # este número sea menor que la tasa de mutación es la propia tasa.
        # En caso de que se cumpla esta condición modificamos todas las propiedades
        # con números dentro del rango recibido como parámetro.
            
        random_number = random.random()
                
        if random_number < mutation_rate: 
            
            # Lo hacemos de esta forma para poder utilizar un solo bucle.
            for i in range(len(self.exponents)):
                self.coefficients[i] += random.uniform(-mutation_range, mutation_range)
                self.exponents[i] += random.uniform(-mutation_range, mutation_range)

            self.coefficients[-1] += random.uniform(-mutation_range, mutation_range)
