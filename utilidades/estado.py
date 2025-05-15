import streamlit as st
import numpy as np
from utilidades.constantes import NOMBRES_METRICAS
from pesos import obtener_pesos_recomendados

def inicializar_pesos_manuales():
    """Inicializa los pesos manuales con los valores recomendados."""
    if 'pesos_manuales' not in st.session_state:
        pesos_recomendados = obtener_pesos_recomendados()
        st.session_state.pesos_manuales = pesos_recomendados.copy()
    for id in NOMBRES_METRICAS:
        if f"peso_manual_{id}" not in st.session_state:
            st.session_state[f"peso_manual_{id}"] = float(pesos_recomendados[id])

def inicializar_estado():
    """Inicializa todas las variables de estado necesarias."""
    if "dispositivos" not in st.session_state:
        st.session_state.dispositivos = []
    
    if 'matriz_ahp_abierta' not in st.session_state:
        st.session_state.matriz_ahp_abierta = False

    if 'pesos_manuales' not in st.session_state:
        inicializar_pesos_manuales()
    
    if 'pesos_guardados' not in st.session_state:
        st.session_state.pesos_guardados = {}
    
    if 'matriz_comparacion' not in st.session_state:
        metricas = list(NOMBRES_METRICAS.keys())
        n = len(metricas)
        st.session_state.matriz_comparacion = np.ones((n, n))

    # Inicializar modo_pesos_radio si no está en modo edición
    if 'modo_pesos_radio' not in st.session_state and not st.session_state.get('modo_edicion', False):
        st.session_state.modo_pesos_radio = "Pesos Recomendados"

    if 'configuraciones_ahp' not in st.session_state:
        st.session_state.configuraciones_ahp = {}

def reiniciar_estado():
    """Reinicia el estado de la aplicación a sus valores iniciales."""
    st.session_state.dispositivos = []
    st.session_state.matriz_ahp_abierta = False
    inicializar_pesos_manuales()
    st.session_state.pesos_guardados = {}
    metricas = list(NOMBRES_METRICAS.keys())
    n = len(metricas)
    st.session_state.matriz_comparacion = np.ones((n, n))
    st.session_state.modo_pesos_radio = "Pesos Recomendados"
    # Eliminar variables adicionales
    for var in [
        'modo_pesos_guardado', 'resultado_global', 'pesos_ahp', 'ahp_resultados',
        'mostrar_tabla_pesos_ahp', 'modo_edicion', 'dispositivo_editando', 'carga_edicion_realizada'
    ]:
        if var in st.session_state:
            del st.session_state[var] 