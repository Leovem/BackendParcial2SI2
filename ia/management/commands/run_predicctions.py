from django.core.management.base import BaseCommand
from django.db import connection
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from django.utils import timezone

class Command(BaseCommand):
    help = 'Ejecuta modelo de IA para predecir puntajes y recomendaciones'

    def handle(self, *args, **options):
        # Leer los datos desde la vista vista_resumen_rendimiento
        with connection.cursor() as cursor:
            cursor.execute("SELECT estudiante_id, bimestre_id, gestion_id, porcentaje_asistencia, puntaje_participacion, promedio_nota FROM vista_resumen_rendimiento")
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            df = pd.DataFrame(rows, columns=columns)

        # Limpieza de datos: quitar nulos
        df.dropna(inplace=True)

        if df.empty:
            self.stdout.write(self.style.WARNING('No hay datos suficientes para entrenar el modelo.'))
            return

        # Entrenamiento del modelo de regresión para predecir nota final
        X = df[["porcentaje_asistencia", "puntaje_participacion", "promedio_nota"]]
        y = df["promedio_nota"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        modelo_regresion = LinearRegression()
        modelo_regresion.fit(X_train, y_train)

        # Clasificación por rendimiento
        def categorizar(n):
            if n > 80:
                return "Alto"
            elif n >= 50:
                return "Promedio"
            else:
                return "Bajo"

        df["rendimiento"] = df["promedio_nota"].apply(categorizar)
        y_class = df["rendimiento"]
        X_class = df[["porcentaje_asistencia", "puntaje_participacion", "promedio_nota"]]

        modelo_clasificacion = RandomForestClassifier(n_estimators=100, random_state=42)
        modelo_clasificacion.fit(X_class, y_class)

        # Calcular percentiles para recomendaciones
        percentiles = df[["porcentaje_asistencia", "puntaje_participacion", "promedio_nota"]].quantile([0.25])

        # Insertar resultados en la tabla prediccion_ml y recomendaciones_ia
        now = timezone.now()
        with connection.cursor() as cursor:
            for _, row in df.iterrows():
                nuevo = pd.DataFrame({
                    "asistencia": [row.porcentaje_asistencia],
                    "participaciones": [row.puntaje_participacion],
                    "evaluaciones": [row.promedio_nota],
                })

                puntaje_predicho = modelo_regresion.predict(nuevo)[0]
                prob_riesgo = 1 - (puntaje_predicho / 100)
                rendimiento_predicho = modelo_clasificacion.predict(nuevo)[0]

                # Guardar predicción
                cursor.execute('''
                    INSERT INTO prediccion_ml (estudiante_id, gestion_id, bimestre_id, puntaje_predicho, probabilidad_riesgo, fecha_prediccion)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', [row.estudiante_id, row.gestion_id, row.bimestre_id, puntaje_predicho, prob_riesgo, now])

                # Generar recomendaciones
                recomendaciones = []
                if row.porcentaje_asistencia < percentiles.loc[0.25, "porcentaje_asistencia"]:
                    recomendaciones.append("Mejorar asistencia a clases.")
                if row.puntaje_participacion < percentiles.loc[0.25, "puntaje_participacion"]:
                    recomendaciones.append("Aumentar la participación en actividades.")
                if row.promedio_nota < percentiles.loc[0.25, "promedio_nota"]:
                    recomendaciones.append("Reforzar los contenidos académicos con tutorías.")
                if not recomendaciones:
                    recomendaciones.append("Buen desempeño general. ¡Sigue así!")

                cursor.execute('''
                    INSERT INTO recomendaciones_ia (estudiante_id, gestion_id, bimestre_id, recomendaciones, fecha_generacion)
                    VALUES (%s, %s, %s, %s, %s)
                ''', [row.estudiante_id, row.gestion_id, row.bimestre_id, recomendaciones, now])

        self.stdout.write(self.style.SUCCESS('Predicciones y recomendaciones generadas correctamente.'))
