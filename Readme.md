# Predicción de Cargas Energéticas con Prophet

Este proyecto permite predecir series temporales relacionadas con la demanda y generación de energía eléctrica en distintas regiones, utilizando el modelo `Prophet` de Meta. Las predicciones se visualizan y se evalúan con métricas de error como MAE, RMSE y MAPE.

## 📄 Archivo principal

El script principal del proyecto es:  
**`predictor_prophet.py`**

Este archivo:

- Carga un dataset de series temporales (`time_series_30min_singleindex.csv`).
- Aplica el modelo Prophet a varias variables de interés.
- Grafica las predicciones comparándolas con los valores reales.
- Calcula métricas de desempeño (MAE, RMSE, MAPE).
- Muestra un resumen de resultados.

## 📦 Librerías necesarias

Asegúrate de tener instaladas las siguientes librerías de Python:

- [`pandas`](https://pandas.pydata.org/)
- [`matplotlib`](https://matplotlib.org/)
- [`prophet`](https://facebook.github.io/prophet/)
- [`scikit-learn`](https://scikit-learn.org/stable/)

Puedes instalarlas todas con:

```bash
pip install pandas matplotlib prophet scikit-learn

## ⚙️ Nota importante sobre Prophet

> La instalación de `prophet` puede requerir compilar dependencias.  
> Si usas **Windows**, se recomienda instalarlo dentro de un entorno virtual (`venv`) o mediante `conda`.

---

## 📁 Dataset

El dataset utilizado debe estar en la raíz del proyecto con el siguiente nombre:

`time_series_30min_singleindex.csv`

Este archivo contiene múltiples columnas relacionadas con:

- Carga eléctrica real y pronosticada
- Generación eólica y solar
- Capacidad instalada  
Todo en diferentes regiones europeas, en intervalos de **30 minutos**.

---

## 📊 Variables utilizadas

En este ejemplo se utilizan las siguientes columnas del dataset:

- `CY_load_actual_entsoe_transparency`
- `GB_GBN_load_actual_entsoe_transparency`
- `GB_GBN_wind_generation_actual`
- `IE_sem_load_actual_entsoe_transparency`

Estas variables pueden modificarse fácilmente dentro del script, en la lista `variables`.

---

## 📈 Resultados esperados

Por cada variable analizada, el script generará:

- Un **gráfico** comparativo entre los valores reales y la predicción generada por `Prophet`.
- Una **tabla resumen** con las métricas de evaluación del modelo:
