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

df = peliculas.merge(creditos, left_on="id", right_on="movie_id", how="inner")

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
# EJE 1 — Rating promedio por rango de presupuesto
# ======================================================

df_eje1 = peliculas[["budget","rating"]].dropna()
df_eje1 = df_eje1[df_eje1["budget"] > 0].copy()
df_eje1["budget_millones"] = df_eje1["budget"] / 1_000_000

max_budget = df_eje1["budget_millones"].max()

# construir bins sin romper el orden
bins = [0, 10, 50, 100, 200, 500, 1000]
bins = [b for b in bins if b < max_budget]
bins.append(max_budget)

labels = [f"{bins[i]}-{bins[i+1]}M" for i in range(len(bins)-1)]

df_eje1["rango_presupuesto"] = pd.cut(df_eje1["budget_millones"], bins=bins, labels=labels, include_lowest=True)

rating_por_presupuesto = df_eje1.groupby("rango_presupuesto")["rating"].mean().reset_index()

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
# EJE 2 — Duración mediana por década (últimos 50 años)
# ======================================================

current_year = 2025
start_year = current_year - 50

df_eje2 = peliculas.dropna(subset=["año", "runtime"])
df_eje2 = df_eje2[(df_eje2["año"] >= start_year) & (df_eje2["año"] <= current_year)]

df_eje2["decada"] = (df_eje2["año"] // 10) * 10
duracion_por_decada = df_eje2.groupby("decada")["runtime"].agg(["mean", "median", "count"]).reset_index()

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

# ======================================================
# EJE 3 — ROI promedio por género
# ======================================================

df_eje3 = peliculas[["title", "genres", "ROI"]].dropna(subset=["ROI"]).copy()

filas_genero = []

for indice, fila in df_eje3.iterrows():
    generos = fila["genres"]

    if not generos:
        continue

    for genero in generos:
        nombre_genero = genero.get("name")

        filas_genero.append({
            "titulo": fila["title"],
            "genero": nombre_genero,
            "ROI": fila["ROI"]
        })

df_roi_genero = pd.DataFrame(filas_genero)

df_roi_genero = df_roi_genero.dropna(subset=["genero"])

roi_por_genero = df_roi_genero.groupby("genero")["ROI"].mean().reset_index()

roi_por_genero = roi_por_genero.sort_values("ROI", ascending=False)

print("\nROI promedio por género:")
print(roi_por_genero)

plt.figure(figsize=(12, 6))
sns.barplot(data=roi_por_genero, x="genero", y="ROI")
plt.title("ROI promedio por género")
plt.xlabel("Género")
plt.ylabel("ROI (revenue / budget)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("grafico_roi_por_genero.png")
plt.show()

roi_por_genero.to_csv("result_roi_por_genero.csv", index=False)

# ======================================================
# EJE 4 — Directores con mejor rating promedio (mínimo 3 películas)
# ======================================================

df_eje4_creditos = creditos[["movie_id", "crew"]].copy()

filas_directores = []

for indice, fila in df_eje4_creditos.iterrows():
    movie_id = fila["movie_id"]
    crew = fila["crew"]

    for persona in crew:

        if persona.get("job") == "Director":
            filas_directores.append({
                "movie_id": movie_id,
                "director": persona.get("name")
            })

df_directores = pd.DataFrame(filas_directores)

df_pelis_rating = peliculas[["id", "title", "rating"]].dropna(subset=["rating"])

directores_peliculas = df_directores.merge(
    df_pelis_rating,
    left_on="movie_id",
    right_on="id",
    how="left"
)

directores_peliculas = directores_peliculas.dropna(subset=["rating"])

resumen_directores = directores_peliculas.groupby("director")["rating"].agg(["mean", "count"]).reset_index()
resumen_directores = resumen_directores.rename(columns={
    "mean": "rating_promedio",
    "count": "cantidad_peliculas"
})

resumen_directores = resumen_directores[resumen_directores["cantidad_peliculas"] >= 3]

resumen_directores = resumen_directores.sort_values(
    ["rating_promedio", "cantidad_peliculas"],
    ascending=False
)

print("\nDirectores con mejor rating promedio (mínimo 3 películas):")
print(resumen_directores.head(20))

top10_directores = resumen_directores.head(10)

plt.figure(figsize=(12, 6))
sns.barplot(data=top10_directores, x="director", y="rating_promedio")
plt.title("Top 10 directores por rating promedio (mínimo 3 películas)")
plt.xlabel("Director")
plt.ylabel("Rating promedio (vote_average)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("grafico_directores_rating.png")
plt.show()

resumen_directores.to_csv("result_directores_rating.csv", index=False)

print("\nCSV generados:")
print("result_presupuesto_vs_rating.csv")
print("result_duracion_por_decada.csv")
print("result_roi_por_genero.csv")
print("result_directores_rating.csv")

print("PNG generados:")
print("grafico_presupuesto_vs_rating.png")
print("grafico_duracion_por_decada.png")
print("grafico_roi_por_genero.png")
print("grafico_directores_rating.png")

