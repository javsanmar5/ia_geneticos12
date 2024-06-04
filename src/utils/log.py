import os

def records(file: str, rmse: float, r2: float, time: float) -> None:
    '''
    Guardamos los datos obtenidos en caso de que sean 
    mejores que los records existentes.

    :param file: Nombre del fichero con el que estamos trabajando
    :param rmse: Nuevo rmse obtenido, aqui comprobamos que sea menor 
    o no que el que ya poseemos
    :param r2: Nuevo r2 obtenido
    :param time: Nuevo tiempo obtenido
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
            file_found = True
            break

    # Si no se encontró, es decir, estamos ante un nuevo
    # fichero, agregamos una nueva entrada
    if not file_found:
        new_entry = [
            f"\nfile: {file}\n",
            f"\trmse:\t{rmse:.4f}\n",
            f"\tr2:\t\t{r2:.4f}\n",
            f"\ttime:\t{time:.2f}\n"
        ]
        lines.extend(new_entry)

    # Escribimos los datos actualizados de nuevo en el archivo
    with open(data_dir, 'w') as f:
        f.writelines(lines)
