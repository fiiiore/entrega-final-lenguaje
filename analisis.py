
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import ast

creditos = pd.read_csv("datos/tmdb_5000_credits.csv")
peliculas = pd.read_csv("datos/tmdb_5000_movies.csv")
print("peliculas:")
print(peliculas.head())
print("creditos:")
print(creditos.head())
peliculas.info()
creditos.info()

def convertir_json(texto):
    try:
        return ast.literal_eval(texto)
    except:
        return []


columnas_json_peliculas = ["genres", "keywords", "production_countries", "production_companies"]
for col in columnas_json_peliculas:
    peliculas[col] = peliculas[col].apply(convertir_json)

columnas_json_creditos = ["cast", "crew"]
for col in columnas_json_creditos:
    creditos[col] = creditos[col].apply(convertir_json)

peliculas["release_date"] = pd.to_datetime(peliculas["release_date"], errors="coerce")
peliculas["año"] = peliculas["release_date"].dt.year

peliculas = peliculas[(peliculas["budget"] > 0) & (peliculas["revenue"] > 0)]

peliculas["ROI"] = peliculas["revenue"] / peliculas["budget"]
