print("✅ INICIO DEL SCRIPT")

try:
    import psycopg2
    import pandas as pd
    print("✅ Librerías importadas correctamente")

    conn = psycopg2.connect(
        host="shinkansen.proxy.rlwy.net",
        port="53892",
        database="railway",
        user="postgres",
        password="wiTtIywQiWBbuEeEsCimaLyqVpAWoXZK"
    )
    print("✅ Conexión exitosa")

    df = pd.read_sql("SELECT * FROM vista_resumen_rendimiento LIMIT 1", conn)
    print("✅ Consulta ejecutada, filas:", len(df))

except Exception as e:
    print("❌ ERROR:", e)

print("✅ FIN DEL SCRIPT")
