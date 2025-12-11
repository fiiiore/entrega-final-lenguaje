# Proyecto Final Lenguajes 2025  
## Integrantes
-Testa Fiorella.
-Rocha Milagros.

Este proyecto trabaja con el dataset TMDB 5000 Movies, realizando un análisis para estudiar diferentes características del cine, como rating, presupuesto, etc.

El proceso incluye: lectura e inspección del dataset, limpieza y preparación de datos, desarrollo de cuatro ejes de análisis, generación de gráficos y archivos CSV, y la construcción de una mini-API que permite consultar los resultados.

La API y el análisis se encuentran conectados: el notebook genera los CSV y la API los expone mediante endpoints y un dashboard visual.


## Cómo ejecutar el notebook
1. Abrir VS Code o Jupyter. (O cualquier entorno compatible con Jupyter Notebook)
2. Abrir `analisis.ipynb`.
3. Ejecutar las celdas con Run All.

Los gráficos y CSV se generan automáticamente en la carpeta del proyecto.

---

## Cómo ejecutar la API  
El archivo `app.py` levanta una API local con FastAPI.

Instalar dependencias (en caso de ser necesario):
pip install -r requirements.txt

Ejecutar la API
Desde la terminal ubicada en la carpeta del proyecto:
python app.py

Luego abrir el navegador (si no se abre solo):
http://127.0.0.1:8000

En esa dirección se muestra el dashboard con:
* vista previa de datos,
* gráficos en base64,
* enlaces de descarga de los CSV.
* endpoints JSON para consultar los resultados.

---

## Endpoints disponibles

Homepage:
GET /

Descarga de CSV:
GET /descargar/presupuesto_rating
GET /descargar/duracion_decadas
GET /descargar/roi_genero
GET /descargar/directores_rating

Endpoints JSON del análisis:
GET /api/presupuesto_rating
GET /api/duracion_decadas
GET /api/roi_genero
GET /api/directores_rating

## Notas 

* Los cuatro ejes analíticos y sus gráficos están en el notebook.
* La API utiliza los CSV generados por el análisis.
* El dashboard sirve para visualizar resultados de forma rápida.
* Todo el proyecto se ejecuta de manera local.








