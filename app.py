from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import pandas as pd
import uvicorn
import webbrowser
import threading
import time
import base64

app = FastAPI(
    title="Dashboard - Proyecto Lenguajes 2025",
    description="Panel visual de resultados del análisis TMDB 5000",
    version="3.0"
)

def cargar_csv(path):
    try:
        return pd.read_csv(path)
    except:
        raise HTTPException(status_code=404, detail=f"No se encontró el archivo: {path}")

# ================================================
# Convertir PNG → Base64 para mostrar dentro del dashboard
# ================================================
def cargar_imagen_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except:
        return None

# ================================================
# HOMEPAGE — DASHBOARD
# ================================================
@app.get("/", response_class=HTMLResponse)
def home():

    # Cargar datasets generados por el análisis
    df_pres = cargar_csv("result_presupuesto_vs_rating.csv")
    df_dura = cargar_csv("result_duracion_por_decada.csv")
    df_roi = cargar_csv("result_roi_por_genero.csv")
    df_dir = cargar_csv("result_directores_rating.csv")

    # Tomar las primeras 8 filas como vista previa
    preview_pres = df_pres.head(8).to_html(index=False)
    preview_dura = df_dura.head(8).to_html(index=False)
    preview_roi = df_roi.head(8).to_html(index=False)
    preview_dir = df_dir.head(8).to_html(index=False)

    # Cargar gráficos
    img1 = cargar_imagen_base64("grafico_presupuesto_vs_rating.png")
    img2 = cargar_imagen_base64("grafico_duracion_por_decada.png")
    img3 = cargar_imagen_base64("grafico_roi_por_genero.png")
    img4 = cargar_imagen_base64("grafico_directores_rating.png")


    html = f"""
    <html>
    <head>
        <title>Dashboard Lenguajes 2025</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f3f4f6;
                margin: 0;
            }}
            h1 {{
                text-align: center;
                padding: 20px;
                background: #1e3a8a;
                color: white;
                margin: 0;
            }}
            .container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                padding: 30px;
                gap: 40px;
            }}
            .card {{
                background: white;
                width: 450px;
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }}
            .card h2 {{
                font-size: 20px;
                color: #1e40af;
                margin-bottom: 10px;
            }}
            img {{
                width: 100%;
                border-radius: 10px;
            }}
            .btn {{
                display: inline-block;
                padding: 10px 14px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                margin-top: 10px;
                font-size: 14px;
            }}
            .btn:hover {{
                background: #1e3a8a;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 14px;
            }}
            th, td {{
                padding: 6px;
                border: 1px solid #ddd;
                text-align: center;
            }}
        </style>
    </head>

    <body>
        <h1>📊 Dashboard del Proyecto Lenguajes 2025</h1>

        <div class="container">

            <!-- CARD 1 -->
            <div class="card">
                <h2>🎬 Rating Promedio por Rango de Presupuesto</h2>
                <img src="data:image/png;base64,{img1}">
                <h3>Vista previa de los datos</h3>
                {preview_pres}
                <a class="btn" href="/descargar/presupuesto_rating">⬇️ Descargar CSV</a>
            </div>

            <!-- CARD 2 -->
            <div class="card">
                <h2>⏳ Duración Mediana por Década</h2>
                <img src="data:image/png;base64,{img2}">
                <h3>Vista previa de los datos</h3>
                {preview_dura}
                <a class="btn" href="/descargar/duracion_decadas">⬇️ Descargar CSV</a>
            </div>

            <!-- CARD 3 -->
            <div class="card">
                <h2>💸 ROI Promedio por Género</h2>
                <img src="data:image/png;base64,{img3}">
                <h3>Vista previa de los datos</h3>
                {preview_roi}
                <a class="btn" href="/descargar/roi_genero">⬇️ Descargar CSV</a>
            </div>

            <!-- CARD 4 -->
             <div class="card">
                <h2>🎥 Directores con Mejor Rating Promedio</h2>
                <img src="data:image/png;base64,{img4}">
                <h3>Vista previa de los datos</h3>
                {preview_dir}
                <a class="btn" href="/descargar/directores_rating">⬇️ Descargar CSV</a>
            </div>

        </div>

        <div class="card" style="max-width: 900px; margin: 30px auto 40px auto;">
            <h2> Endpoints JSON del análisis</h2>

            <p>Resultados en formato JSON.</p>

            <ul style="line-height: 1.8;">
                <li>
                    <a href="/api/presupuesto_rating" style="color: #2563eb; font-weight: bold;">
                        /api/presupuesto_rating
                    </a>
                     Rating promedio por rango de presupuesto
                </li>

                <li>
                    <a href="/api/duracion_decadas" style="color: #2563eb; font-weight: bold;">
                        /api/duracion_decadas
                    </a>
                     Duración mediana por década
                </li>
                
                <li>
                    <a href="/api/roi_genero" style="color: #2563eb; font-weight: bold;">
                        /api/roi_genero
                    </a>
                     ROI promedio por género
                </li>

                <li>
                    <a href="/api/directores_rating" style="color: #2563eb; font-weight: bold;">
                        /api/directores_rating
                    </a>
                     Directores con mejor rating promedio
                </li>
             </ul>


            <p style="font-size: 13px; color: #555;">
            </p>
        </div>

    </body>
</html>

    """

    return HTMLResponse(html)


# ================================================
# ENDPOINTS DE DESCARGA
# ================================================
@app.get("/descargar/presupuesto_rating")
def descargar_presupuesto_rating():
    return FileResponse("result_presupuesto_vs_rating.csv")

@app.get("/descargar/duracion_decadas")
def descargar_duracion_decadas():
    return FileResponse("result_duracion_por_decada.csv")

@app.get("/descargar/roi_genero")
def descargar_roi_genero():
    return FileResponse("result_roi_por_genero.csv")

@app.get("/descargar/directores_rating")
def descargar_directores_rating():
    return FileResponse("result_directores_rating.csv")

# ================================================
# ENDPOINTS JSON
# ================================================
@app.get("/api/presupuesto_rating")
def api_presupuesto_rating():
    df = cargar_csv("result_presupuesto_vs_rating.csv")
    return df.to_dict(orient="records")

@app.get("/api/duracion_decadas")
def api_duracion_decadas():
    df = cargar_csv("result_duracion_por_decada.csv")
    return df.to_dict(orient="records")

@app.get("/api/roi_genero")
def api_roi_genero():
    df = cargar_csv("result_roi_por_genero.csv")
    return df.to_dict(orient="records")

@app.get("/api/directores_rating")
def api_directores_rating():
    df = cargar_csv("result_directores_rating.csv")
    return df.to_dict(orient="records")

# ================================================
# Abrir navegador automáticamente
# ================================================
def abrir_navegador():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:8000")

if __name__ == "__main__":
    threading.Thread(target=abrir_navegador).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
