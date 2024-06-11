import os

def records(file: str, rmse: float, r2: float, time: float, seed: int) -> None:
    '''
    Guardamos los datos obtenidos en caso de que sean mejores 
    que los records existentes. 
    Si el fichero no existe creamos una nueva entrada en el 
    registro, todos los datos se guardan en: './data/log.txt'.

    :param file: String | Nombre del fichero con el que estamos trabajando.
    :param rmse: Float | Nuevo rmse obtenido, aqui comprobamos que sea menor 
    o no que el que ya poseemos.
    :param r2: Float | Nuevo r2 obtenido.
    :param time: Float | Nuevo tiempo obtenido.
    :param seed: Integer | Semilla utilizada.
    '''

    current_dir = os.path.dirname(__file__)
    data_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'data', 'log.txt'))

    # Leemos el archivo
    with open(data_dir, 'r') as f:
        lines = f.readlines()

    # Verificamos si el archivo existe en el log
    file_found = False
    for i in range(len(lines)):
        if lines[i].strip() == f"file: {file}":
            # Extraer el rmse existente
            existing_rmse = float(lines[i + 1].split()[1])
            
            # Actualizamos si se ha batido un record, es decir,
            # si el nuevo rmse es menor que el existente
            if round(rmse, 4) < existing_rmse or existing_rmse == 0.:
                print("Nuevo récord obtenido. Consultar records en data/log.txt")
                lines[i + 1] = f"\trmse:\t{rmse:.4f}\n"
                lines[i + 2] = f"\tr2:\t\t{r2:.4f}\n"
                lines[i + 3] = f"\ttime:\t{time:.2f}\n"
                lines[i + 4] = f"\tseed:\t{seed}\n"
            file_found = True
            break

    # Si no se encontró, es decir, estamos ante un nuevo
    # fichero, agregamos una nueva entrada
    if not file_found:
        print(f"Nuevo fichero {file}. Datos añadidos a data/log.txt")
        new_entry = [
            f"\nfile: {file}\n",
            f"\trmse:\t{rmse:.4f}\n",
            f"\tr2:\t\t{r2:.4f}\n",
            f"\ttime:\t{time:.2f}\n"
            f"\tseed:\t{seed}\n"
        ]
        lines.extend(new_entry)

    # Escribimos los datos actualizados de nuevo en el archivo
    with open(data_dir, 'w') as f:
        f.writelines(lines)
