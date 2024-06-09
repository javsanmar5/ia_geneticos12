import pandas as pd
import time
import sys

from sklearn.metrics import root_mean_squared_error, r2_score
from ag.AG import AG
from utils.log import records



def main(*args, **kwargs):

	# Nombre generico del dataset
	if len(kwargs["argv"]) == 1:
		nombre_dataset = 'housing'	
	else: 
		nombre_dataset = kwargs["argv"][1]

	print(f"Fichero: {nombre_dataset.capitalize()}")

	nombre_dataset_train 	= nombre_dataset + "_data/" + nombre_dataset + "_train.csv"
	nombre_dataset_val 		= nombre_dataset + "_data/" + nombre_dataset + "_val.csv"

	parameters = {
		"housing": (36, 300),
		"synt1": (20, 100),
		"toy1": (200, 500)
	}

	seed = 22

	if nombre_dataset not in parameters.keys():
		raise ValueError(f"No contamos con los datos {nombre_dataset} de momento.")

	# La clase AG debe estar implementada	
	# (importe los ficheros necesarios antes de ejecutar las siguientes lineas)
	ag = AG(
		# datos de entrenamiento (para el proceso del AG)
		datos_train = nombre_dataset_train, 
		# datos de validacion/test (para predec	ir)
		datos_test = nombre_dataset_val, 
		# semilla para numeros aleatorios
		seed=seed, 
		# numero de individuos
		nInd = parameters.get(nombre_dataset, 50)[0], 
		# maximo de iteraciones
		maxIter = parameters.get(nombre_dataset, 500)[1]
	)

	# winner_chromosome, y_pred  = ag.run()

	# Ejecucion del AG midiendo el tiempo
	inicio = time.time()
	ind, y_pred = ag.run()
	fin = time.time()
	print(f'Tiempo ejecucion: {(fin-inicio):.2f}')

	# Imprimir mejor solución encontrada
	print(f'Coeficientes del mejor individuo: {ind.coefficients}')
	print(f'Exponentes del mejor individuo: {ind.exponents}')
	# 0.5*(a1^2) + -0.3*(a2^1) + ... + 10 # --> Se trata de un ejemplo

	# Imprimir predicciones sobre el conjunto de test
	n = 10
	print(f'{n} primeras predicciones: {y_pred[:n]}')
	#  [-1.53, 1.49, 2.15, ..., -2.77] # --> Se trata de un ejemplo

	# Cargar valores reales de 'y' en el conjunto de validacion/test 
	#   y calcular RMSE y R2 con las predicciones del AG
	y_true = pd.read_csv("./data/" +  nombre_dataset_val)['y']
	rmse = root_mean_squared_error(y_true, y_pred)
	print(f'RMSE: {rmse:.4f}')

	r2 = r2_score(y_true, y_pred)
	print(f'R2: {r2:.4f}')

	records(nombre_dataset.upper(), rmse, r2, fin-inicio, seed)


if __name__ == '__main__':
	main(argv = sys.argv)
	