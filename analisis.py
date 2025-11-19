
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx


creditos = pd.read_csv("datos/tmdb_5000_credits.csv")
peliculas = pd.read_csv("datos/tmdb_5000_movies.csv")
print("peliculas:")
print(peliculas.head())
print("creditos:")
print(creditos.head())
peliculas.info()
creditos.info()
