import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

sns.set(style="whitegrid", rc={"figure.figsize": (11, 6)})

def convertir_json(texto):
    try:
        return ast.literal_eval(texto)
    except:
        return []

# Cargar datasets
peliculas = pd.read_csv("datos/tmdb_5000_movies.csv")
creditos = pd.read_csv("datos/tmdb_5000_credits.csv")

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
peliculas["rating"] = pd.to_numeric(peliculas["vote_average"], errors="coerce")
peliculas["runtime"] = pd.to_numeric(peliculas["runtime"], errors="coerce")

print("Filas procesadas:", peliculas.shape)

# ======================================================
# EJE 2 — Rating promedio por rango de presupuesto
# ======================================================

df_eje2 = peliculas[["budget","rating"]].dropna()
df_eje2 = df_eje2[df_eje2["budget"] > 0].copy()
df_eje2["budget_millones"] = df_eje2["budget"] / 1_000_000

max_budget = df_eje2["budget_millones"].max()

# construir bins sin romper el orden
bins = [0, 10, 50, 100, 200, 500, 1000]
bins = [b for b in bins if b < max_budget]
bins.append(max_budget)

labels = [f"{bins[i]}-{bins[i+1]}M" for i in range(len(bins)-1)]

df_eje2["rango_presupuesto"] = pd.cut(df_eje2["budget_millones"], bins=bins, labels=labels, include_lowest=True)

rating_por_presupuesto = df_eje2.groupby("rango_presupuesto")["rating"].mean().reset_index()

plt.figure(figsize=(12,6))
sns.barplot(data=rating_por_presupuesto, x="rango_presupuesto", y="rating", palette="viridis")
plt.title("Rating promedio por rango de presupuesto")
plt.xlabel("Rango de presupuesto (millones de USD)")
plt.ylabel("Rating promedio (vote_average)")
plt.xticks(rotation=45)
plt.ylim(0, 10)
plt.tight_layout()
plt.savefig("grafico_presupuesto_vs_rating.png")
plt.show()

rating_por_presupuesto.to_csv("result_presupuesto_vs_rating.csv", index=False)

# ======================================================
# EJE 3 — Duración mediana por década (últimos 50 años)
# ======================================================

current_year = 2025
start_year = current_year - 50

df_eje3 = peliculas.dropna(subset=["año", "runtime"])
df_eje3 = df_eje3[(df_eje3["año"] >= start_year) & (df_eje3["año"] <= current_year)]

df_eje3["decada"] = (df_eje3["año"] // 10) * 10
duracion_por_decada = df_eje3.groupby("decada")["runtime"].agg(["mean", "median", "count"]).reset_index()

print("\nDuración por década:")
print(duracion_por_decada)

plt.figure(figsize=(11, 6))
sns.lineplot(
    data=duracion_por_decada,
    x="decada",
    y="median",
    marker="o",
    linewidth=2.5,
    color="purple"
)
plt.title("Evolución de la Duración Mediana de Películas por Década (Últimos 50 años)")
plt.xlabel("Década")
plt.ylabel("Duración Mediana (minutos)")
plt.grid(True, linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("grafico_duracion_por_decada.png")
plt.show()

duracion_por_decada.to_csv("result_duracion_por_decada.csv", index=False)

print("\nCSV generados:")
print("result_presupuesto_vs_rating.csv")
print("result_duracion_por_decada.csv")
print("PNG generados:")
print("grafico_presupuesto_vs_rating.png")
print("grafico_duracion_por_decada.png")
