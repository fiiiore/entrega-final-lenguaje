from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "API funcionando correctamente"}

@app.get("/presupuesto_rating")
def presupuesto_rating():
    df = pd.read_csv("result_presupuesto_vs_rating.csv")
    return df.to_dict(orient="records")

@app.get("/duracion_decadas")
def duracion_decadas():
    df = pd.read_csv("result_duracion_por_decada.csv")
    return df.to_dict(orient="records")
