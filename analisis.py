import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast

sns.set(style="whitegrid", rc={"figure.figsize": (10,6)})


# ======================================================
# 1) Funciones auxiliares
# ======================================================

def convertir_json(texto):
    """Convierte columnas tipo string a listas/dicts reales."""
    try:
        return ast.literal_eval(texto)
    except:
        return []


# ======================================================
# 2) Carga y limpieza inicial
# ======================================================

# Convertir columnas JSON de películas
columnas_json_peliculas = ["genres", "keywords", "production_countries", "production_companies"]
for col in columnas_json_peliculas:
    peliculas[col] = peliculas[col].apply(convertir_json)

# Convertir JSON de créditos
columnas_json_creditos = ["cast", "crew"]
for col in columnas_json_creditos:
    creditos[col] = creditos[col].apply(convertir_json)

# Fechas y año
peliculas["release_date"] = pd.to_datetime(peliculas["release_date"], errors="ignore")
peliculas["año"] = peliculas["release_date"].dt.year

# Filtrar pelis sin presupuesto o revenue
peliculas = peliculas[(peliculas["budget"] > 0) & (peliculas["revenue"] > 0)].copy()

# Crear ROI
peliculas["ROI"] = peliculas["revenue"] / peliculas["budget"]

# rating y duración
peliculas["rating"] = pd.to_numeric(peliculas["vote_average"], errors="coerce")
peliculas["runtime"] = pd.to_numeric(peliculas["runtime"], errors="coerce")


# ======================================================
# 3) Análisis Exploratorio Inicial (EDA)
# ======================================================

print("Forma del dataset:", peliculas.shape)
display(peliculas.head())

print("\nEstadísticas numéricas:")
display(peliculas[["budget", "revenue", "runtime", "rating", "ROI"]].describe())

# Gráficos EDA
plt.figure()
sns.histplot(peliculas["rating"], bins=25)
plt.title("Distribución del rating")
plt.xlabel("Rating")
plt.show()

plt.figure()
sns.histplot(np.log10(peliculas["budget"]), bins=25)
plt.title("Distribución del presupuesto (log10)")
plt.xlabel("log10(budget)")
plt.show()

plt.figure()
sns.histplot(peliculas["runtime"].dropna(), bins=25)
plt.title("Duración de películas")
plt.xlabel("Minutos")
plt.show()


# ======================================================
# 4) EJE 2 — Relación entre Presupuesto y Rating
# ======================================================

df_eje2 = peliculas.dropna(subset=["budget", "rating"])
df_eje2 = df_eje2[df_eje2["budget"] > 0]

pearson = df_eje2["budget"].corr(df_eje2["rating"], method="pearson")
spearman = df_eje2["budget"].corr(df_eje2["rating"], method="spearman")

print(f"\nCorrelación Pearson: {pearson:.4f}")
print(f"Correlación Spearman: {spearman:.4f}")

plt.figure(figsize=(10,6))
plt.scatter(np.log10(df_eje2["budget"]), df_eje2["rating"], alpha=0.4)
plt.title("Relación entre presupuesto (log10) y rating")
plt.xlabel("Presupuesto (log10)")
plt.ylabel("Rating")
plt.show()

# Guardar para API
df_eje2[["title","budget","rating"]].to_csv("result_presupuesto_vs_rating.csv", index=False)


# ======================================================
# 5) EJE 3 — Evolución de la Duración en Últimos 50 Años
# ======================================================

current_year = 2025
start_year = current_year - 50

df_eje3 = peliculas.dropna(subset=["año", "runtime"])
df_eje3 = df_eje3[(df_eje3["año"] >= start_year) & (df_eje3["año"] <= current_year)]

df_eje3["decada"] = (df_eje3["año"] // 10) * 10

duracion_por_decada = df_eje3.groupby("decada")["runtime"].agg(["count","mean","median"]).reset_index()

print("\nDuración promedio y mediana por década:")
display(duracion_por_decada)

plt.figure(figsize=(10,6))
sns.lineplot(data=duracion_por_decada, x="decada", y="median", marker="o")
plt.title("Duración mediana de películas por década")
plt.xlabel("Década")
plt.ylabel("Duración mediana (min)")
plt.show()

duracion_por_decada.to_csv("result_duracion_por_decada.csv", index=False)


# ======================================================
# 6) Final
# ======================================================
print("\n=====================================")
print("CSV generados:")
print("- result_presupuesto_vs_rating.csv")
print("- result_duracion_por_decada.csv")
print("=====================================")
