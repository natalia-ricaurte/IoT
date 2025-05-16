import pandas as pd
from utilidades.constantes import MAPEO_COLUMNAS_IMPORTACION

def to_dict_flat(p):
    """
    Convierte diferentes tipos de datos a un diccionario plano.
    
    Args:
        p: Puede ser un objeto con método to_dict(), una Serie de pandas, un diccionario o un objeto iterable.
    
    Returns:
        dict: Un diccionario plano con los datos.
    """
    if hasattr(p, 'to_dict'):
        return p.to_dict()
    if isinstance(p, pd.Series):
        return p.to_dict()
    if isinstance(p, dict):
        return p
    return dict(p)

def obtener_valor_dispositivo(disp, nombre_interno):
    claves_posibles = [k for k, v in MAPEO_COLUMNAS_IMPORTACION.items() if v == nombre_interno]
    claves_posibles.append(nombre_interno)
    for clave in claves_posibles:
        if clave in disp:
            return disp[clave]
    return 'N/A'

def extraer_valor_peso(v):
    if isinstance(v, dict):
        for val in v.values():
            try:
                return float(val)
            except (ValueError, TypeError):
                continue
        raise ValueError("No se encontró valor numérico en el peso.")
    try:
        return float(v)
    except (ValueError, TypeError):
        raise ValueError(f"No se pudo convertir el valor {v} a número.") 