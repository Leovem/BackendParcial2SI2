
import psycopg2
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from datetime import datetime 

# Configura tu conexión a PostgreSQL
conn = psycopg2.connect(
    host="shinkansen.proxy.rlwy.net",
    port="53892",
    database="railway",
    user="postgres",
    password="wiTtIywQiWBbuEeEsCimaLyqVpAWoXZK"
)

# Leer datos desde la vista
#df = pd.read_sql("SELECT * FROM vista_resumen_rendimiento", conn)
try:
    df = pd.read_sql("SELECT * FROM vista_resumen_rendimiento", conn)
    print("Consulta ejecutada correctamente. Filas obtenidas:", len(df))
except Exception as e:
    print("Error al ejecutar la consulta:", e)
    conn.close()
    exit()

# Eliminar filas con valores nulos
df.dropna(subset=["promedio_nota", "porcentaje_asistencia", "puntaje_participacion"], inplace=True)

# Variables predictoras y objetivo
X = df[["porcentaje_asistencia", "puntaje_participacion", "promedio_nota"]]
y_regresion = df["promedio_nota"]

# ------------------- MODELO DE REGRESIÓN -----------------------
x_train, x_test, y_train, y_test = train_test_split(X, y_regresion, test_size=0.2, random_state=42)

modelo_regresion = LinearRegression()
modelo_regresion.fit(x_train, y_train)
predicciones = modelo_regresion.predict(X)

# ------------------- CLASIFICACIÓN -----------------------
def categorizar_rendimiento(nota):
    if nota > 80:
        return "Alto"
    elif nota >= 50:
        return "Medio"
    return "Bajo"

df["rendimiento"] = df["promedio_nota"].apply(categorizar_rendimiento)
y_clasificacion = df["rendimiento"]

X_train, X_test, y_train, y_test = train_test_split(X, y_clasificacion, test_size=0.2, random_state=42)
modelo_clasificacion = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_clasificacion.fit(X_train, y_train)
predicciones_clas = modelo_clasificacion.predict(X)

# Calcular probabilidades de riesgo
proba_riesgo = modelo_clasificacion.predict_proba(X)
clases = modelo_clasificacion.classes_
riesgo_idx = list(clases).index("Bajo")

# ------------------ GUARDAR RESULTADOS ------------------------
cursor = conn.cursor()

for i, row in df.iterrows():
    puntaje = round(predicciones[i], 2)
    riesgo = round(proba_riesgo[i][riesgo_idx] * 100, 2)

    cursor.execute("""
        INSERT INTO prediccion_ml (estudiante_id, bimestre_id, gestion_id, puntaje_predicho, probabilidad_riesgo)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (estudiante_id, bimestre_id, gestion_id) DO UPDATE
        SET puntaje_predicho = EXCLUDED.puntaje_predicho,
            probabilidad_riesgo = EXCLUDED.probabilidad_riesgo,
            fecha_prediccion = CURRENT_TIMESTAMP;
    """, (
        row["estudiante_id"],
        row["bimestre_id"],
        row["gestion_id"],
        puntaje,
        riesgo
    ))

    # ---------------- RECOMENDACIONES ------------------
    recomendaciones = []
    if row["porcentaje_asistencia"] < 70:
        recomendaciones.append("Mejorar la asistencia a clases.")
    if row["puntaje_participacion"] < 30:
        recomendaciones.append("Aumentar la participación en clase.")
    if row["promedio_nota"] < 51:
        recomendaciones.append("Buscar apoyo académico para mejorar las calificaciones.")

    if not recomendaciones:
        recomendaciones.append("¡Buen trabajo! Sigue así.")
    print("Insertando recomendaciones para estudiante", row["estudiante_id"], recomendaciones)
    print("Valores:", row["porcentaje_asistencia"], row["puntaje_participacion"], row["promedio_nota"])
    print("Total filas después del dropna:", len(df))

    # Inserta una sola fila con el arreglo completo de recomendaciones
    cursor.execute("""
        INSERT INTO recomendaciones_ia (estudiante_id, bimestre_id, gestion_id, recomendaciones)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (estudiante_id, bimestre_id, gestion_id) DO UPDATE
        SET recomendaciones = EXCLUDED.recomendaciones,
            fecha_generacion = CURRENT_TIMESTAMP;
    """, (
        row["estudiante_id"],
        row["bimestre_id"],
        row["gestion_id"],
        recomendaciones  # se convierte en arreglo PostgreSQL automáticamente
    ))


conn.commit()
cursor.close()
conn.close()
print("Predicciones y recomendaciones guardadas correctamente.")
