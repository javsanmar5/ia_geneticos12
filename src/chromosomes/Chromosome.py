from chromosomes.AbstractChromosome import AbstractChromosome
from sklearn.metrics import root_mean_squared_error
import random
from typing import List, Tuple

class Chromosome(AbstractChromosome):

    def __init__(self, coefficients: List[float] = None,
                 exponents: List[float] = None, 
                 variables_amount: int = 0,
                 initial_range: float = 1.) -> None:
        '''
        La idea del cromosoma es ser una lista de tamaño 2*n
        donde n es el numero de features (características).
        Los valores con índice par serán los coeficientes y
        los valores con índice impar los exponentes.

        De esta forma, la posición 2i será el coeficiente de
        la feature i y la posicion 2i + 1 será su exponente.
        
        Inicialmente numeros aleatorios entre -3 y 3.
        '''

        if coefficients is None and exponents is None:
            self.coefficients:  List[float] = [random.uniform(-initial_range, initial_range) for _ in range(variables_amount + 1)]
            self.exponents:     List[float] = [random.uniform(-initial_range, initial_range) for _ in range(variables_amount)]
        else:
            self.coefficients:  List[float] = coefficients
            self.exponents:     List[float] = exponents
                

    def fitness(self, train_data: List[Tuple[float]]) -> float:
        # Valoraremos al cromosoma como la inversa de la distancia
        # entre el valor predicho y el target. 
        # Esta distancia la calcularemos con el MSE visto en la asignatura,
        # en este caso, la diferencia entre target y predicted al cuadrado.
        
        y_pred: List[float] = []
        y_true: List[float] = []

        selected_data = random.sample(train_data, min(len(train_data), 1000))

        for datum in selected_data:
            y_pred.append(self.predict(datum))
            y_true.append(datum[-1])

        #y_true = [datum[-1] for datum in train_data]
        rmse = root_mean_squared_error(y_true, y_pred)

        return rmse
    
    def predict(self, datum: Tuple[float]) -> float:
        '''
        El valor predicho será la suma de c[i](x[i]**e[i]) donde:

        x[i]: son las distintas features de la lista self.features.
        c[i]: son los coeficientes del cromosoma. Posiciones pares.
        e[i]: son los exponentes del cromosoma. Posiciones impares. 
        '''

        prediction: float = 0.

        for i in range(len(datum) - 1):

            # if datum[i] < 0.:
            #     self.exponents[i] = round(self.exponents[i], 0)
            if datum[i] == 0.:
                self.exponents[i] = abs(self.exponents[i])

            # value = -abs(datum[i] ** self.exponents[i]) if datum[i] < 0 else abs(datum[i] ** self.exponents[i])
            value = (datum[i] ** self.exponents[i]).real
            
            prediction += self.coefficients[i] * value

        prediction += self.coefficients[-1]
        return prediction
    

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

        point = random.randint(1, len(self.exponents) - 1) # Escogemos el punto de cruce

        child1_coefficients = self.coefficients[:point] + chromosomeToCrossWith.coefficients[point:] 
        child2_coefficients = chromosomeToCrossWith.coefficients[:point] + self.coefficients[point:]
        child1_exponents = self.exponents[:point] + chromosomeToCrossWith.exponents[point:] 
        child2_exponents = chromosomeToCrossWith.exponents[:point] + self.exponents[point:]
        
        return [Chromosome(child1_coefficients, child1_exponents),
                Chromosome(child2_coefficients, child2_exponents)]


    def mutate(self, mutation_rate: float, mutation_range: float) -> None:
        # Debemos mutar o no aleatoriamente el cromosoma en el que estamos.
        # Esta mutación será alterar, también con números aleatorios, los 
        # valores del cromosoma.
        # Para calcular cuando mutar utilizaremos una tasa de mutación entre 
        # 0 y 1, escogemos un número aleatorio, también entre 0 y 1, y la
        # probabilidad de que este número sea menor que la tasa es exactamente 
        # la tasa.

            
        random_number = random.random() # Generamos un numero aleatorio entre 0 y 1
                
        if random_number < mutation_rate: 
            
            for i in range(len(self.exponents)):
                self.coefficients[i] += random.uniform(-mutation_range, mutation_range)
                self.exponents[i] += random.uniform(-mutation_range, mutation_range)

            self.coefficients[-1] += random.uniform(-mutation_range, mutation_range)


        # for i in range(len(self.exponents)):

        #     random_number = random.random() # Generamos un numero aleatorio entre 0 y 1
        #     if random_number < mutation_rate: 

        #         self.coefficients[i] += random.uniform(-mutation_range, mutation_range)

        #     self.exponents[i] += random.uniform(-mutation_range, mutation_range)

        # random_number = random.random()
        # if random_number < mutation_rate: 
        #     self.coefficients[-1] += random.uniform(-mutation_range, mutation_range)
