import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error

class ProphetPredictor:
    def __init__(self, df, variables, fecha_fin_entrenamiento, fecha_inicio_prediccion, fecha_fin_prediccion):
        self.df = df
        self.variables = variables
        self.fecha_fin_entrenamiento = fecha_fin_entrenamiento
        self.fecha_inicio_prediccion = fecha_inicio_prediccion
        self.fecha_fin_prediccion = fecha_fin_prediccion
        self.resultados = []

    def procesar_todo(self):
        for variable in self.variables:
            serie = self.df[variable].dropna()
            serie.name = variable

            serie_entrenamiento = serie.loc[:self.fecha_fin_entrenamiento]
            serie_real = serie.loc[self.fecha_inicio_prediccion:self.fecha_fin_prediccion]

            df_prophet = serie_entrenamiento.reset_index()
            df_prophet.columns = ['ds', 'y']

            modelo = Prophet(daily_seasonality=True, weekly_seasonality=True, yearly_seasonality=True)
            modelo.fit(df_prophet)

            periodo_pred = int((self.fecha_fin_prediccion - self.fecha_inicio_prediccion).total_seconds() / 1800) + 1
            futuro = modelo.make_future_dataframe(periods=periodo_pred, freq='30min')
            futuro = futuro[futuro['ds'] >= self.fecha_inicio_prediccion]
            pred = modelo.predict(futuro)['yhat'].values[:len(serie_real)]

            mae = mean_absolute_error(serie_real, pred)
            rmse = mean_squared_error(serie_real, pred)
            mape = np.mean(np.abs((serie_real.values - pred) / serie_real.values)) * 100

            self.resultados.append({
                "variable": variable,
                "real": serie_real,
                "pred": pred,
                "mae": mae,
                "rmse": rmse,
                "mape": mape
            })

    def mostrar_metricas(self):
        resumen = pd.DataFrame([{
            "Variable": r["variable"],
            "MAE": round(r["mae"], 2),
            "RMSE": round(r["rmse"], 2),
            "MAPE (%)": round(r["mape"], 2)
        } for r in self.resultados])
        print("\nResumen de métricas:")
        print(resumen)

    def graficar_todo(self):
        fig, axs = plt.subplots(len(self.resultados), 1, figsize=(14, 5 * len(self.resultados)), sharex=True)
        if len(self.resultados) == 1:
            axs = [axs]
        for i, r in enumerate(self.resultados):
            axs[i].plot(r["real"].index, r["real"].values, label="Real", color="blue")
            axs[i].plot(r["real"].index, r["pred"], label="Predicci\u00f3n", color="green")
            axs[i].set_title(f"{r['variable']} (MAE={r['mae']:.1f}, MAPE={r['mape']:.1f}%)")
            axs[i].grid(True)
            axs[i].legend()
        axs[-1].set_xlabel("Fecha")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    df = pd.read_csv("time_series_30min_singleindex.csv", parse_dates=["utc_timestamp"], index_col="utc_timestamp")
    df.index = df.index.tz_convert(None)

    variables = [
        "CY_load_actual_entsoe_transparency",
        "GB_GBN_load_actual_entsoe_transparency",
        "GB_GBN_wind_generation_actual",
        "IE_sem_load_actual_entsoe_transparency"
    ]
    fecha_fin_entrenamiento = pd.to_datetime("2020-09-28 23:30:00")
    fecha_inicio_prediccion = pd.to_datetime("2020-09-29 00:00:00")
    fecha_fin_prediccion = pd.to_datetime("2020-09-30 23:30:00")

    predictor = ProphetPredictor(df, variables, fecha_fin_entrenamiento, fecha_inicio_prediccion, fecha_fin_prediccion)
    predictor.procesar_todo()
    predictor.mostrar_metricas()
    predictor.graficar_todo()
