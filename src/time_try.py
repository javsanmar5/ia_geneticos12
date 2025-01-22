import time
import pandas as pd
from utils.csv_reader import read_data

FILEPATH="./data/housing_data/housing_train.csv"

initial_pandas = time.time()
for _ in range(10):
    read_by_pandas = pd.read_csv(FILEPATH)

print(f"Pandas time: {time.time() - initial_pandas}")


# ------------------------------------------------------------------------

initial_custom = time.time()
for _ in range(10):
    read_customly = read_data("housing_data/housing_train.csv")

print(f"Pandas time: {time.time() - initial_custom}")