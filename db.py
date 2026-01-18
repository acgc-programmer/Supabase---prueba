from psycopg2 import connect
from dotenv import load_dotenv, find_dotenv
import os

# find_dotenv() asegura que encuentre el archivo aunque estés en una subcarpeta
load_dotenv(find_dotenv(), override=True) 

def conectar_db():
    # DIAGNÓSTICO: Esto te dirá exactamente qué está leyendo Python
    print(f"Intentando conectar a: {os.getenv('DB_HOST')}")
    
    try:
        conexion = connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            # Para Supabase con Pooler (6543) a veces es necesario sslmode
            sslmode='require' 
        )
        print("¡Conexión exitosa a Supabase!")
        return conexion
    except Exception as e:
        print("Error de conexión:", e)
        return None