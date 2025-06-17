import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os
import json
import gspread
from google.oauth2 import service_account


# Configuración de conexión a Supabase (PostgreSQL)
load_dotenv()
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

# Autenticación con Google Sheets
creds_path = os.getenv("GOOGLE_CREDS_JSON")  # <- Asegurate de tener esta variable en tu .env
scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
gc = gspread.authorize(creds)

# ID del archivo de Google Sheets (reemplazar con el tuyo)
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# Abrir hoja de cálculo
sh = gc.open_by_key(SPREADSHEET_ID)

# Diccionario con las vistas y los nombres de archivo
vistas = {
    "vista_ingresos_mensuales": "ventas_mensuales",
    "vista_egresos_mensuales": "egresos_mensuales",
    "vista_resultado_mensual": "resultado_mensual"
}

# Procesar cada vista
for vista, nombre_hoja in vistas.items():
    df = pd.read_sql_query(f"SELECT * FROM {vista}", conn)

    # Convertir fechas a string para evitar error de serialización
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)

    # Si existe hoja, limpiarla; si no, crearla
    try:
        worksheet = sh.worksheet(nombre_hoja)
        sh.del_worksheet(worksheet)
        print(f"Hoja '{nombre_hoja}' eliminada para actualización.")
    except gspread.exceptions.WorksheetNotFound:
        pass
    
    worksheet = sh.add_worksheet(title=nombre_hoja, rows=str(len(df)+1), cols=str(len(df.columns)))

    # Escribir los datos
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print(f"Vista '{vista}' exportada a hoja '{nombre_hoja}'.")

# Cerrar conexión a la base de datos
conn.close()
print("Conexión cerrada.")