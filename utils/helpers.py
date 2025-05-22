import pandas as pd
import streamlit as st
from utils.constants import RECOMMENDED_WEIGHTS

def to_dict_flat(d):
    """
    Converts different types of data to a flat dictionary.
    
    Args:
        d: Can be an object with to_dict() method, a pandas Series, a dictionary or an iterable object.
    
    Returns:
        dict: A flat dictionary with the data.
    """
    if hasattr(d, 'to_dict'):
        return d.to_dict()
    if isinstance(d, pd.Series):
        return d.to_dict()
    if isinstance(d, dict):
        return d
    return dict(d)

def extract_weight_value(v):
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

def create_weights_snapshot(user_weights, weights_mode):
    """Creates a consistent snapshot of the weights used.
    
    Args:
        user_weights (dict): The weights used in the calculation (already normalized)
        weights_mode (str): The weights mode used ("Pesos Recomendados", "Ajuste Manual", "Calcular nuevos pesos")
    
    Returns:
        dict: The weights snapshot with consistent format
    """
    # Ensure user_weights is a valid dictionary
    if not isinstance(user_weights, dict):
        try:
            user_weights = to_dict_flat(user_weights)
        except Exception:
            user_weights = {}
    
    # Clean and normalize weights
    clean_weights = {}
    for k, v in user_weights.items():
        try:
            if isinstance(v, dict):
                v = list(v.values())[0]
            clean_weights[k] = float(v)
        except (ValueError, TypeError):
            continue
    
    config_name = "Pesos Recomendados"
    
    if weights_mode == "Calcular nuevos pesos":
        config_name = "Pesos Calculados"
        if 'ahp_weights' in st.session_state:
            for ahp_config_name, config in st.session_state.ahp_configurations.items():
                if to_dict_flat(config['weights']) == to_dict_flat(clean_weights):
                    config_name = f"Configuración Calculada: {ahp_config_name}"
                    break
    elif weights_mode == "Ajuste Manual":
        recommended_weights = RECOMMENDED_WEIGHTS
        if to_dict_flat(clean_weights) == to_dict_flat(recommended_weights):
            config_name = "Pesos Recomendados"
        else:
            config_name = "Pesos Manuales Personalizados"
            for manual_config_name, config in st.session_state.saved_weights.items():
                try:
                    # Normalize saved configuration weights for comparison
                    normalized_config = {k: float(v) for k, v in config.items()}
                    total = sum(normalized_config.values())
                    if total != 1.0:
                        normalized_config = {k: v/total for k, v in normalized_config.items()}
                    if to_dict_flat(normalized_config) == to_dict_flat(clean_weights):
                        config_name = f"Configuración Manual: {manual_config_name}"
                        break
                except Exception:
                    continue
    
    return {
        "mode": weights_mode,
        "config_name": config_name,
        "manual_weights": clean_weights,  # Save normalized weights
        "ahp_weights": st.session_state.get("ahp_weights", {})
    } 