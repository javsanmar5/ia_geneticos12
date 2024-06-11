from sklearn.metrics import root_mean_squared_error, r2_score
from ag.AG import AG
from utils.log import records

import pandas as pd
import time
import sys


def main(*args, **kwargs):

	# Nombre generico del dataset
	if len(kwargs["argv"]) == 1:
		nombre_dataset = 'toy1'	
	else: 
		nombre_dataset = kwargs["argv"][1]

	print(f"Fichero: {nombre_dataset.capitalize()}")

	nombre_dataset_train 	= nombre_dataset + "_data/" + nombre_dataset + "_train.csv"
	nombre_dataset_val 		= nombre_dataset + "_data/" + nombre_dataset + "_val.csv"

	seed = 124

	# Creamos la instancia del algoritmo genético. Mirar la documentación del constructor 
	# para ver que parámetros son modificables.
	ag = AG(
		# datos de entrenamiento (para el proceso del AG)
		datos_train = nombre_dataset_train, 
		# datos de validacion/test (para predecir)
		datos_test = nombre_dataset_val, 
		# semilla para numeros aleatorios
		seed=seed, 
		# numero de individuos
		nInd = 50,
		# maximo de iteraciones
		maxIter = 300
	)

	# Ejecucion del AG midiendo el tiempo
	inicio = time.time()
	winner_chromosome, predicted = ag.run()
	fin = time.time()
	print(f'Tiempo ejecucion: {(fin-inicio):.2f}')


	# Imprimir mejor solución encontrada
	print(f'Coeficientes del mejor individuo: {winner_chromosome.coefficients}')
	print(f'Exponentes del mejor individuo: {winner_chromosome.exponents}')
	output = 'Los valores se obtendrían de la forma:\n' + ' + '.join(
		f'{winner_chromosome.coefficients[i]} * (x[{i}] ** {winner_chromosome.exponents[i]})'
		for i in range(len(winner_chromosome.exponents))
	)
	output += f' + {winner_chromosome.coefficients[-1]}'
	print(output)



	# Imprimir predicciones sobre el conjunto de test
	n = 10
	print(f'{n} primeras predicciones: {predicted[:n]}')


	# Cargar valores reales de 'y' en el conjunto de validacion/test 
	#  y calcular RMSE y R2 con las predicciones del AG
	y_true = pd.read_csv("./data/" +  nombre_dataset_val)['y']
	rmse = root_mean_squared_error(y_true, predicted)
	print(f'RMSE: {rmse:.4f}')

	r2 = r2_score(y_true, predicted)
	print(f'R2: {r2:.4f}')


	# Guardamos en el log si hemos conseguido un nuevo record.
	records(nombre_dataset.upper(), rmse, r2, fin-inicio, seed)


if __name__ == '__main__':
	main(argv = sys.argv)
	