# Trabajo IA

### Algoritmos genéticos.

Trabajo realizado por Javier Ruíz y Javier Santos para la asignatura de IA.
Grupo: geneticos12



## Pasos explicados para probar el proyecto

Sigue estos pasos para probar el repositorio

1. **Clonar el Repositorio**:
    - Ejecuta el comando `git clone` con la URL del repositorio y el comando `cd` para entrar en el directorio clonado.

```sh
git clone https://github.com/javsanmar5/ia_geneticos12.git
cd ia_geneticos12
```

### Ahora existen dos alternativas:
Podemos utilizar un entorno virtual o el entorno de *Python* instalado en su equipo. Si no desea crear un entorno virtual, mire los requisitos en el apartado [Requisitos](#requisitos) y pase directamente al **Paso 4**.     

2. **Crear y Activar un Entorno Virtual**:
    - Instrucciones separadas para Windows y macOS/Linux para crear y activar un entorno virtual.

    *Activar entorno en Windows*
    ```sh
    python -m venv env
    env\Scripts\activate
    ```

    *Activar entorno en Linux/MaxOS*

    ```sh
    python -m venv env
    source env/bin/activate
    ```
        

3. **Instalar las Dependencias**:
    - El comando `pip install -r requirements.txt` instalará todas las dependencias listadas en el archivo `requirements.txt`.

    ```sh
    pip install -r requirements.txt
    ```

4. **Ejecutar el Proyecto**:
    Lanza el fichero de prueba *src/test/prueba_AG.py*.
    Opciones:

    - Ejecución por defecto: De manera predeterminada, se utilizará el archivo ubicado en src/prueba_AG.py. Este archivo se puede modificar manualmente. Para ejecutarlo de esta forma, se debe utilizar el siguiente comando:   
        ```sh
        python src/prueba_AG.py
        ```

    - Pasar el nombre del fichero como parámetro: Para ejecutarlo de esta forma, se debe utilizar el siguiente comando:
        ```sh
        python src/prueba_AG.py nombre_fichero
        ```

    En ambos casos las opciones de fichero son: **housing**, **synt1** y **toy1**. Y el comando *python* puede ser modificado por *python3* si es necesario.



## Requisitos

- Python 3.x
- pip

En caso de no utilizar un entorno virtual también será necesario:

- pandas
- scikit-learn 



