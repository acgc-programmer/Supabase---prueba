from psycopg2 import sql, connect

def conectar_db():
    try:
        conexion = connect(
            host="localhost",
            database="general",
            user="postgres",
            password="acgc.2008"
        )
        return conexion
    except Exception as e:
        print("Error al conectar a la base de datos:", e)
        return None