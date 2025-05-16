import pandas as pd
import io
from utilidades.constantes import MAPEO_COLUMNAS_IMPORTACION, DESCRIPCION_COLUMNAS_IMPORTACION, ADVERTENCIA_IMPORTACION
import json

# Esqueleto para la importación de dispositivos desde un archivo CSV, Excel o JSON

# Mapeo fijo: nombres de la plantilla -> nombres internos
MAPEO_COLUMNAS_PLANTILLA = {
    "nombre": "nombre",
    "potencia_w": "potencia",
    "horas_uso_diario": "horas",
    "dias_uso_anio": "dias",
    "peso_kg": "peso",
    "vida_util_anios": "vida",
    "energia_renovable_pct": "energia_renovable",
    "funcionalidad_1_10": "funcionalidad",
    "reciclabilidad_pct": "reciclabilidad",
    "baterias_vida_util": "B",
    "peso_bateria_g": "Wb",
    "mantenimientos": "M",
    "componentes_reemplazados": "C",
    "peso_componente_g": "Wc",
    "peso_nuevo_g": "W0",
    "peso_final_g": "W"
}

def leer_archivo_dispositivos(archivo):
    """
    Lee un archivo de dispositivos en formato CSV, Excel o JSON y devuelve un DataFrame.
    Renombra las columnas de la plantilla a los nombres internos estándar.
    """
    nombre = archivo.name.lower()
    if nombre.endswith('.csv'):
        df = pd.read_csv(archivo)
    elif nombre.endswith('.xlsx'):
        df = pd.read_excel(archivo)
    elif nombre.endswith('.json'):
        df = pd.read_json(archivo)
    else:
        raise ValueError("Formato de archivo no soportado. Usa CSV, Excel o JSON.")
    # Renombrar columnas usando el mapeo fijo
    columnas_mapeadas = {col: MAPEO_COLUMNAS_PLANTILLA[col] for col in df.columns if col in MAPEO_COLUMNAS_PLANTILLA}
    df = df.rename(columns=columnas_mapeadas)
    return df


def to_float(val):
    if isinstance(val, str):
        val = val.replace(',', '.')
    return float(val)


def validar_y_procesar_dispositivos(df):
    """
    Valida las columnas y tipos de datos del DataFrame de dispositivos.
    Devuelve una lista de diccionarios de dispositivos válidos y una lista de errores.
    """
    columnas_requeridas = [
        "nombre", "potencia", "horas", "dias", "peso", "vida",
        "energia_renovable", "funcionalidad", "reciclabilidad", "B",
        "Wb", "M", "C", "Wc", "W0", "W"
    ]
    errores = []
    dispositivos = []
    # Validar columnas
    for col in columnas_requeridas:
        if col not in df.columns:
            errores.append(f"Falta la columna requerida: {col}")
    if errores:
        return [], errores
    # Validar y procesar cada fila
    for idx, row in df.iterrows():
        dispositivo = {}
        try:
            dispositivo = {
                "nombre": str(row["nombre"]),
                "potencia": float(row["potencia"]),
                "horas": float(row["horas"]),
                "dias": int(row["dias"]),
                "peso": float(row["peso"]),
                "vida": float(row["vida"]),
                "energia_renovable": float(row["energia_renovable"]),
                "funcionalidad": float(row["funcionalidad"]),
                "reciclabilidad": float(row["reciclabilidad"]),
                "B": int(row["B"]),
                "Wb": float(row["Wb"]),
                "M": int(row["M"]),
                "C": int(row["C"]),
                "Wc": float(row["Wc"]),
                "W0": float(row["W0"]),
                "W": float(row["W"])
            }
            dispositivos.append(dispositivo)
        except Exception as e:
            errores.append(f"Error en la fila {idx+2}: {e}")
    return dispositivos, errores


def generar_plantilla_excel():
    """
    Genera y retorna un buffer con la plantilla de dispositivos en formato Excel (.xlsx).
    """
    columnas = [
        "nombre",
        "potencia_w",
        "horas_uso_diario",
        "dias_uso_anio",
        "peso_kg",
        "vida_util_anios",
        "energia_renovable_pct",
        "funcionalidad_1_10",
        "reciclabilidad_pct",
        "baterias_vida_util",
        "peso_bateria_g",
        "mantenimientos",
        "componentes_reemplazados",
        "peso_componente_g",
        "peso_nuevo_g",
        "peso_final_g"
    ]
    datos_ejemplo = [
        ["Sensor de temperatura", 2, 24, 365, 0.1, 5, 30, 8, 65, 2, 50, 1, 2, 20, 200, 180],
        ["Actuador de válvula", 5, 12, 300, 0.2, 7, 50, 9, 70, 3, 60, 2, 1, 25, 250, 230]
    ]
    df_plantilla = pd.DataFrame(datos_ejemplo, columns=columnas)
    # Crear hoja de ayuda
    ayuda = [
        [col, DESCRIPCION_COLUMNAS_IMPORTACION.get(col, "")] for col in columnas
    ]
    df_ayuda = pd.DataFrame(ayuda, columns=["Columna", "Descripción y unidad"])
    advertencia = ADVERTENCIA_IMPORTACION
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_plantilla.to_excel(writer, index=False, sheet_name="Plantilla")
        df_ayuda.to_excel(writer, index=False, sheet_name="Ayuda")
        # Escribir advertencia en la primera celda de la hoja de ayuda
        ws = writer.sheets["Ayuda"]
        ws.insert_rows(0)
        ws["A1"] = advertencia
    buffer.seek(0)
    return buffer

def generar_plantilla_json():
    ejemplo = [
        {
            "nombre": "Sensor de temperatura",
            "potencia_w": 2,
            "horas_uso_diario": 24,
            "dias_uso_anio": 365,
            "peso_kg": 0.1,
            "vida_util_anios": 5,
            "energia_renovable_pct": 50,
            "funcionalidad_1_10": 8,
            "reciclabilidad_pct": 80,
            "baterias_vida_util": 1,
            "peso_bateria_g": 50,
            "mantenimientos": 2,
            "componentes_reemplazados": 1,
            "peso_componente_g": 10,
            "peso_nuevo_g": 100,
            "peso_final_g": 90
        }
    ]
    return io.BytesIO(json.dumps(ejemplo, indent=2, ensure_ascii=False).encode('utf-8')) 