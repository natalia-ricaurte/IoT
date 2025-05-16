import pandas as pd
import io

# Esqueleto para la importación de dispositivos desde un archivo CSV, Excel o JSON

def leer_archivo_dispositivos(archivo):
    """
    Lee un archivo de dispositivos en formato CSV, Excel o JSON y devuelve un DataFrame.
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
        "nombre","potencia_watt","horas_uso_diario","dias_uso_anual","peso_kg","vida_util_anios",
        "energia_renovable_porcentaje","funcionalidad","reciclabilidad_porcentaje","baterias_vida_util",
        "peso_bateria_gramos","mantenimientos","componentes_reemplazados","peso_componente_gramos",
        "peso_nuevo_gramos","peso_final_gramos"
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
                "potencia": to_float(row["potencia_watt"]),
                "horas": to_float(row["horas_uso_diario"]),
                "dias": int(row["dias_uso_anual"]),
                "peso": to_float(row["peso_kg"]),
                "vida": to_float(row["vida_util_anios"]),
                "energia_renovable": to_float(row["energia_renovable_porcentaje"]),
                "funcionalidad": to_float(row["funcionalidad"]),
                "reciclabilidad": to_float(row["reciclabilidad_porcentaje"]),
                "B": int(row["baterias_vida_util"]),
                "Wb": to_float(row["peso_bateria_gramos"]),
                "M": int(row["mantenimientos"]),
                "C": int(row["componentes_reemplazados"]),
                "Wc": to_float(row["peso_componente_gramos"]),
                "W0": to_float(row["peso_nuevo_gramos"]),
                "W": to_float(row["peso_final_gramos"])
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
        "nombre","potencia_watt","horas_uso_diario","dias_uso_anual","peso_kg","vida_util_anios",
        "energia_renovable_porcentaje","funcionalidad","reciclabilidad_porcentaje","baterias_vida_util",
        "peso_bateria_gramos","mantenimientos","componentes_reemplazados","peso_componente_gramos",
        "peso_nuevo_gramos","peso_final_gramos"
    ]
    datos_ejemplo = [
        ["Sensor de temperatura",2,24,365,0.1,5,30,8,65,2,50,1,2,20,200,180],
        ["Actuador de válvula",5,12,300,0.2,7,50,9,70,3,60,2,1,25,250,230]
    ]
    df_plantilla = pd.DataFrame(datos_ejemplo, columns=columnas)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_plantilla.to_excel(writer, index=False, sheet_name="Plantilla")
    buffer.seek(0)
    return buffer 