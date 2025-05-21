import pandas as pd
from utilidades.constantes import MAPEO_COLUMNAS_IMPORTACION
import streamlit as st
from pesos import obtener_pesos_recomendados

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

def crear_snapshot_pesos(pesos_usuario, modo_pesos):
    """Crea un snapshot de los pesos utilizados de manera consistente.
    
    Args:
        pesos_usuario (dict): Los pesos utilizados en el cálculo (ya normalizados)
        modo_pesos (str): El modo de pesos utilizado ("Pesos Recomendados", "Ajuste Manual", "Calcular nuevos pesos")
    
    Returns:
        dict: El snapshot de pesos con el formato consistente
    """
    # Asegurar que pesos_usuario sea un diccionario válido
    if not isinstance(pesos_usuario, dict):
        try:
            pesos_usuario = to_dict_flat(pesos_usuario)
        except Exception:
            pesos_usuario = {}
    
    # Limpiar y normalizar los pesos
    pesos_limpios = {}
    for k, v in pesos_usuario.items():
        try:
            if isinstance(v, dict):
                v = list(v.values())[0]
            pesos_limpios[k] = float(v)
        except (ValueError, TypeError):
            continue
    
    nombre_config = "Pesos Recomendados"
    
    if modo_pesos == "Calcular nuevos pesos":
        if 'pesos_ahp' in st.session_state:
            for nombre_config_ahp, config in st.session_state.configuraciones_ahp.items():
                if to_dict_flat(config['pesos']) == to_dict_flat(pesos_limpios):
                    nombre_config = f"Configuración Calculada: {nombre_config_ahp}"
                    break
            if nombre_config == "Pesos Recomendados":
                nombre_config = "Pesos Calculados"
    elif modo_pesos == "Ajuste Manual":
        pesos_recomendados = obtener_pesos_recomendados()
        if to_dict_flat(pesos_limpios) == to_dict_flat(pesos_recomendados):
            nombre_config = "Pesos Recomendados"
        else:
            nombre_config = "Pesos Manuales Personalizados"
            for nombre_config_manual, config in st.session_state.pesos_guardados.items():
                try:
                    # Normalizar los pesos de la configuración guardada para comparar
                    config_normalizada = {k: float(v) for k, v in config.items()}
                    suma = sum(config_normalizada.values())
                    if suma != 1.0:
                        config_normalizada = {k: v/suma for k, v in config_normalizada.items()}
                    if to_dict_flat(config_normalizada) == to_dict_flat(pesos_limpios):
                        nombre_config = f"Configuración Manual: {nombre_config_manual}"
                        break
                except Exception:
                    continue
    
    return {
        "modo": modo_pesos,
        "nombre_configuracion": nombre_config,
        "pesos_manuales": pesos_limpios,  # Guardar los pesos normalizados
        "pesos_ahp": st.session_state.get("pesos_ahp", {})
    } 