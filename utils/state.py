import streamlit as st
import numpy as np
from utils.constants import METRIC_NAMES
from weights import get_recommended_weights

def initialize_manual_weights():
    """Initializes manual weights with recommended values."""
    if 'manual_weights' not in st.session_state or st.session_state.manual_weights == {}:
        recommended_weights = get_recommended_weights()
        st.session_state.manual_weights = recommended_weights.copy()
    for id in METRIC_NAMES:
        if f"manual_weight_{id}" not in st.session_state:
            st.session_state[f"manual_weight_{id}"] = float(recommended_weights[id])

def initialize_state():
    """Initializes application state variables."""
    if 'devices' not in st.session_state:
        st.session_state.devices = []
    if 'selected_devices' not in st.session_state:
        st.session_state.selected_devices = {}
    if 'weight_mode_radio' not in st.session_state:
        st.session_state.weight_mode_radio = "Pesos Recomendados"
    if 'ahp_weights' not in st.session_state:
        st.session_state.ahp_weights = None
    if 'manual_weights' not in st.session_state:
        st.session_state.manual_weights = {}
    if 'ahp_matrix_open' not in st.session_state:
        st.session_state.ahp_matrix_open = False
    if 'ahp_configurations' not in st.session_state:
        st.session_state.ahp_configurations = {}
    if 'saved_weights' not in st.session_state:
        st.session_state.saved_weights = {}
    if 'show_import' not in st.session_state:
        st.session_state.show_import = False
    if 'imported_devices' not in st.session_state:
        st.session_state.imported_devices = []
    if 'import_message' not in st.session_state:
        st.session_state.import_message = None
    if 'restore_manual_weights' not in st.session_state:
        st.session_state.restore_manual_weights = False
    if 'individual_manual_weights' not in st.session_state:
        st.session_state.individual_manual_weights = {}
    if 'global_result' not in st.session_state:
        st.session_state.global_result = None
    if 'global_calculation_date' not in st.session_state:
        st.session_state.global_calculation_date = None

    if 'manual_weights' not in st.session_state:
        initialize_manual_weights()
    
    if 'comparison_matrix' not in st.session_state:
        metrics = list(METRIC_NAMES.keys())
        n = len(metrics)
        st.session_state.comparison_matrix = np.ones((n, n))

    # Initialize weight_mode_radio if not in edit mode
    if 'weight_mode_radio' not in st.session_state and not st.session_state.get('edit_mode', False):
        st.session_state.weight_mode_radio = "Pesos Recomendados"

def reset_state():
    """Resets all state variables to their initial values."""
    st.session_state.devices = []
    st.session_state.selected_devices = {}
    st.session_state.weight_mode_radio = "Pesos Recomendados"
    st.session_state.ahp_weights = None
    st.session_state.manual_weights = {}
    st.session_state.ahp_matrix_open = False
    st.session_state.ahp_configurations = {}
    st.session_state.saved_weights = {}
    st.session_state.show_import = False
    st.session_state.imported_devices = []
    st.session_state.import_message = None
    st.session_state.restore_manual_weights = False
    st.session_state.individual_manual_weights = {}
    st.session_state.global_result = None
    st.session_state.global_calculation_date = None
    initialize_manual_weights()
    metrics = list(METRIC_NAMES.keys())
    n = len(metrics)
    st.session_state.comparison_matrix = np.ones((n, n))
    st.session_state.weight_mode_radio = "Pesos Recomendados"
    # Remove additional variables
    for var in [
        'saved_weight_mode', 'global_result', 'ahp_weights', 'ahp_results',
        'show_ahp_weights_table', 'edit_mode', 'editing_device', 'edit_load_completed'
    ]:
        if var in st.session_state:
            del st.session_state[var] 