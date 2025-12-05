import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

sns.set(style="whitegrid", rc={"figure.figsize": (10,6)})

def convertir_json(texto):
    try:
        return ast.literal_eval(texto)
    except:
        return []

# Cargar datasets
peliculas = pd.read_csv("tmdb_5000_movies.csv")
creditos  = pd.read_csv("tmdb_5000_credits.csv")

# Columnas JSON
columnas_json_peliculas = ["genres", "keywords", "production_countries", "production_companies"]
for col in columnas_json_peliculas:
    if col in peliculas.columns:
        peliculas[col] = peliculas[col].apply(convertir_json)

columnas_json_creditos = ["cast", "crew"]
for col in columnas_json_creditos:
    creditos[col] = creditos[col].apply(convertir_json)

# Limpieza
peliculas["release_date"] = pd.to_datetime(peliculas["release_date"], errors="coerce")
peliculas["año"] = peliculas["release_date"].dt.year
peliculas = peliculas[(peliculas["budget"] > 0) & (peliculas["revenue"] > 0)].copy()
peliculas["ROI"] = peliculas["revenue"] / peliculas["budget"]
peliculas["rating"] = pd.to_numeric(peliculas["vote_average"], errors="coerce")
peliculas["runtime"] = pd.to_numeric(peliculas["runtime"], errors="coerce")

# EDA Básico
print("Forma del dataset:", peliculas.shape)
display(peliculas.head())
display(peliculas[["budget","revenue","runtime","rating","ROI"]].describe())

sns.histplot(peliculas["rating"], bins=25)
plt.title("Distribución del rating")
plt.show()

sns.histplot(np.log10(peliculas["budget"]), bins=25)
plt.title("Distribución del presupuesto (log10)")
plt.show()

sns.histplot(peliculas["runtime"], bins=25)
plt.title("Duración de las películas")
plt.show()

# EJE 2 — Presupuesto vs Rating
df_eje2 = peliculas.dropna(subset=["budget", "rating"])
df_eje2 = df_eje2[df_eje2["budget"] > 0]

pearson  = df_eje2["budget"].corr(df_eje2["rating"], method="pearson")
spearman = df_eje2["budget"].corr(df_eje2["rating"], method="spearman")

print("Correlación Pearson:", pearson)
print("Correlación Spearman:", spearman)

plt.scatter(np.log10(df_eje2["budget"]), df_eje2["rating"], alpha=0.4)
plt.title("Presupuesto (log10) vs Rating")
plt.xlabel("log10(budget)")
plt.ylabel("Rating")
plt.show()

df_eje2[["title","budget","rating"]].to_csv("result_presupuesto_vs_rating.csv", index=False)

# EJE 3 — Evolución de duración en últimos 50 años
current_year = 2025
start_year = current_year - 50

df_eje3 = peliculas.dropna(subset=["año","runtime"])
df_eje3 = df_eje3[(df_eje3["año"] >= start_year) & (df_eje3["año"] <= current_year)]
df_eje3["decada"] = (df_eje3["año"] // 10) * 10

duracion_por_decada = df_eje3.groupby("decada")["runtime"].agg(["count","mean","median"]).reset_index()
display(duracion_por_decada)

sns.lineplot(data=duracion_por_decada, x="decada", y="median", marker="o")
plt.title("Duración mediana de películas por década")
plt.xlabel("Década")
plt.ylabel("Duración mediana (min)")
plt.show()

duracion_por_decada.to_csv("result_duracion_por_decada.csv", index=False)

print("\nCSV generados:")
print("result_presupuesto_vs_rating.csv")
print("result_duracion_por_decada.csv")
