from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import pandas as pd

app = FastAPI(
    title="Mini API - Proyecto Lenguajes 2025",
    description="API que expone los resultados de análisis del dataset TMDB 5000.",
    version="1.0.0"
)

# ---------------------------------------
# Helper: cargar archivo CSV con formato
# ---------------------------------------
def cargar_csv(path):
    try:
        df = pd.read_csv(path)
        return df
    except:
        raise HTTPException(status_code=404, detail=f"No se encontró el archivo: {path}")

# ---------------------------------------
# Endpoints
# ---------------------------------------

@app.get("/")
def root():
    return {
        "mensaje": "Bienvenidos a la Mini API del proyecto de Lenguajes 2025",
        "endpoints_disponibles": [
            "/presupuesto_rating",
            "/duracion_decadas",
            "/descargar/presupuesto_rating",
            "/descargar/duracion_decadas",
            "/docs"
        ]
    }

@app.get("/presupuesto_rating", summary="Rating promedio por rango de presupuesto")
def presupuesto_rating():
    df = cargar_csv("result_presupuesto_vs_rating.csv")
    return df.to_dict(orient="records")

@app.get("/duracion_decadas", summary="Duración mediana por década")
def duracion_decadas():
    df = cargar_csv("result_duracion_por_decada.csv")
    return df.to_dict(orient="records")

# ---------------------------------------
# Endpoints para DESCARGAR archivos
# ---------------------------------------

@app.get("/descargar/presupuesto_rating", summary="Descargar CSV - presupuesto vs rating")
def descargar_presupuesto_rating():
    return FileResponse("result_presupuesto_vs_rating.csv")


@app.get("/descargar/duracion_decadas", summary="Descargar CSV - duración por década")
def descargar_duracion_decadas():
    return FileResponse("result_duracion_por_decada.csv")
