import streamlit as st
import pandas as pd
import numpy as np
from utils.constants import METRIC_NAMES
from weights import ahp_attributes, consistency_ratio

def calculate_ahp_weights(metrics):
    """Calculates weights using the AHP method from the comparison matrix."""
    df_criteria = pd.DataFrame(
        st.session_state.comparison_matrix,
        index=metrics,
        columns=metrics
    )
    weights = ahp_attributes(df_criteria)
    ic, rc = consistency_ratio(weights, df_criteria, verbose=False)
    return weights, ic, rc

def show_ahp_results(weights, rc):
    """Shows the results of the weight calculation by Pairwise Comparison Matrix."""
    st.success("Pesos calculados mediante la Matriz de Comparación por Pares:")
    # Convert weights to a clean format
    clean_weights = {}
    for k, v in weights.items():
        if isinstance(v, dict):
            val = list(v.values())[0]
        elif isinstance(v, pd.Series):
            val = v.iloc[0]
        else:
            val = v
        clean_weights[k] = float(val)
    # Create DataFrame with weights
    metrics_list = list(clean_weights.keys())
    weights_list = [clean_weights[k] for k in metrics_list]
    names_list = [METRIC_NAMES[k] for k in metrics_list]
    df_weights = pd.DataFrame({
        'Métrica': names_list,
        'Peso': weights_list
    })
    # Add relative importance column with balanced criteria
    df_weights['Importancia'] = df_weights['Peso'].apply(
        lambda x: '🔴 Alta' if x >= 0.20 else '🟡 Media' if 0.10 < x < 0.20 else '🟢 Baja'
    )
    st.dataframe(df_weights.style.format({'Peso': '{:.3f}'}), use_container_width=True)
    # Show consistency ratio and warnings
    if rc < 0.1:
        st.success(f"✅ Razón de Consistencia: {rc:.3f} (La matriz es consistente)")
    else:
        st.warning(f"⚠️ Razón de Consistencia: {rc:.3f} (La matriz NO es consistente)")
        st.info("""
        **Sugerencias para mejorar la consistencia:**
        1. Revise las comparaciones más extremas
        2. Asegúrese de que sus comparaciones sean transitivas
        3. Si A > B y B > C, entonces A debería ser más importante que C
        """)

def show_ahp_matrix():
    """Shows the interface for the pairwise comparison matrix."""
    st.title("Matriz de Comparación por Pares")
    with st.expander("ℹ️ Guía de la Matriz de Comparación por Pares"):
        st.markdown("""
        ### Guía de la Matriz de Comparación por Pares
        
        Esta matriz le permite comparar la importancia relativa de cada par de métricas utilizando la escala de Saaty.
        
        **Escala de Comparación:**
        - 1: Las métricas son igualmente importantes
        - 3: La métrica de la fila es moderadamente más importante
        - 5: La métrica de la fila es fuertemente más importante
        - 7: La métrica de la fila es muy fuertemente más importante
        - 9: La métrica de la fila es extremadamente más importante
        
        **Valores Decimales (Recíprocos):**
        Cuando una métrica es menos importante, use los siguientes valores decimales:
        | Comparación | Valor Decimal |
        |-------------|---------------|
        | 1/2         | 0.50         |
        | 1/3         | 0.33         |
        | 1/4         | 0.25         |
        | 1/5         | 0.20         |
        | 1/6         | 0.17         |
        | 1/7         | 0.14         |
        | 1/8         | 0.13         |
        | 1/9         | 0.11         |
        
        **Ejemplos:**
        - Si el Consumo de Energía es moderadamente más importante que la Huella de Carbono, ingrese 3
        - Si la Huella de Carbono es fuertemente más importante que el E-waste, ingrese 5
        - Si el E-waste es moderadamente menos importante que la Huella de Carbono, ingrese 0.33 (equivalente a 1/3)
        
        **Consejo:** Comience comparando las métricas más importantes entre sí.
        """)
    st.info("Edita solo la mitad superior de la tabla. El resto se calcula automáticamente.")
    metrics = list(METRIC_NAMES.keys())
    names = [METRIC_NAMES[m] for m in metrics]
    n = len(metrics)
    if 'comparison_matrix' not in st.session_state:
        st.session_state.comparison_matrix = np.ones((n, n))
    # Column headers
    cols = st.columns(n+1)
    cols[0].write("")
    for j in range(n):
        cols[j+1].markdown(f"**{names[j]}**")
    # Matrix rows
    for i in range(n):
        row = st.columns(n+1)
        row[0].markdown(f"**{names[i]}**")
        for j in range(n):
            if i == j:
                row[j+1].markdown('<span style="font-weight:bold;">1.00</span>', unsafe_allow_html=True)
                st.session_state.comparison_matrix[i, j] = 1.0
            elif i < j:
                value = row[j+1].number_input(
                    f"Comparación {names[i]} vs {names[j]}",
                    min_value=0.11,
                    max_value=9.0,
                    value=float(st.session_state.comparison_matrix[i, j]) if st.session_state.comparison_matrix[i, j] != 1.0 else 1.0,
                    step=0.01,
                    key=f"matrix_{i}_{j}",
                    label_visibility="collapsed"
                )
                st.session_state.comparison_matrix[i, j] = value
                st.session_state.comparison_matrix[j, i] = 1/value
            else:
                row[j+1].write(f"{st.session_state.comparison_matrix[i, j]:.2f}")
    st.markdown("---")
    # Action buttons
    col_calc, col_save, col_space, col_cancel, col_reset = st.columns([1, 1, 2, 1, 1])
    with col_calc:
        if st.button("Calcular pesos"):
            df_criteria = pd.DataFrame(
                st.session_state.comparison_matrix,
                index=metrics,
                columns=metrics
            )
            weights = ahp_attributes(df_criteria)
            ic, rc = consistency_ratio(weights, df_criteria, verbose=False)
            st.session_state.ahp_results = {
                'weights': weights,
                'ic': ic,
                'rc': rc
            }
            st.rerun()
    with col_save:
        if st.button("Guardar y salir"):
            if 'ahp_results' in st.session_state:
                weights = st.session_state.ahp_results['weights']
                if hasattr(weights, 'to_dict'):
                    weights = weights.to_dict()
                st.session_state.ahp_weights = weights
                # Save results to show in main screen
                st.session_state.show_ahp_weights_table = {
                    'weights': weights,
                    'rc': st.session_state.ahp_results['rc']
                }
            st.session_state.ahp_matrix_open = False
            if 'saved_weight_mode' in st.session_state:
                st.session_state.weight_mode_radio = st.session_state.saved_weight_mode
            st.rerun()
    with col_cancel:
        if st.button("Cancelar"):
            if 'ahp_results' in st.session_state:
                weights = st.session_state.ahp_results['weights']
                if hasattr(weights, 'to_dict'):
                    weights = weights.to_dict()
                # Save results to show in main screen
                st.session_state.show_ahp_weights_table = {
                    'weights': weights,
                    'rc': st.session_state.ahp_results['rc']
                }
            st.session_state.ahp_matrix_open = False
            if 'saved_weight_mode' in st.session_state:
                st.session_state.weight_mode_radio = st.session_state.saved_weight_mode
            st.rerun()
    with col_reset:
        if st.button("Reiniciar matriz", help="Reinicia la matriz de comparación a valores iniciales (identidad)", key="btn_reset_matrix"):
            st.session_state.comparison_matrix = np.ones((n, n))
            # Clear previous AHP weights and results
            if 'ahp_weights' in st.session_state:
                del st.session_state.ahp_weights
            if 'ahp_results' in st.session_state:
                del st.session_state.ahp_results
            if 'show_ahp_weights_table' in st.session_state:
                del st.session_state.show_ahp_weights_table
            st.warning("¡La matriz de comparación ha sido reiniciada a valores iniciales!")
            st.rerun()
    # Show results if they exist
    if st.session_state.get('ahp_results'):
        show_ahp_results(st.session_state.ahp_results['weights'], st.session_state.ahp_results['rc'])
    st.stop() 