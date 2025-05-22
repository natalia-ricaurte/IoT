import streamlit as st
import pandas as pd
from utils.constants import METRIC_NAMES, RECOMMENDED_WEIGHTS
from utils.helpers import to_dict_flat
from weights import validate_manual_weights

def reset_manual_weights():
    """Resets manual weights to recommended values."""
    # reset manual weights dictionary
    st.session_state.manual_weights = RECOMMENDED_WEIGHTS
    # reset individual weights
    for k, v in RECOMMENDED_WEIGHTS.items():
        st.session_state[f"manual_weight_{k}"] = float(v)

def show_recommended_weights():
    """Shows the interface for recommended weights."""  
    user_weights = RECOMMENDED_WEIGHTS
    st.success("Se han cargado los pesos recomendados del modelo AHP+ODS.")

    weights_df = pd.DataFrame.from_dict(user_weights, orient='index', columns=['Peso'])
    weights_df.index = weights_df.index.map(METRIC_NAMES)
    weights_df = weights_df.rename_axis('Métrica').reset_index()
    
    # Add relative importance column
    weights_df['Importancia'] = weights_df['Peso'].apply(
        lambda x: '🔴 Alta' if x >= 0.20 else '🟡 Media' if 0.10 < x < 0.20 else '🟢 Baja'
    )
    
    st.dataframe(weights_df.style.format({'Peso': '{:.3f}'}), use_container_width=True)

    with st.expander("Ver explicación del modelo AHP+ODS"):
        st.markdown("""
        **Metodología de Cálculo de Pesos Recomendados**

        Los pesos recomendados se calcularon combinando dos enfoques complementarios:

        **1. Alineación con los Objetivos de Desarrollo Sostenible (ODS):**
        - Cada métrica fue evaluada según cuántos ODS relevantes aborda
        - Por ejemplo, el consumo de energía se alinea con el ODS 7 (energía asequible y no contaminante) y el ODS 13 (acción por el clima)

        **2. Evaluación cualitativa del impacto ambiental directo:**
        - Se asignó a cada métrica una puntuación de 1 a 5 según:
          - Magnitud del impacto
          - Frecuencia del impacto
          - Alcance del impacto
        - Por ejemplo, la huella de carbono y el consumo de energía obtienen una puntuación más alta que el mantenimiento

        **Cálculo del Score Total:**
        ```
        Score = 1 × ODS + 2 × Impacto
        ```
        Donde:
        - ODS: Número de ODS relevantes que aborda la métrica
        - Impacto: Puntuación cualitativa del impacto ambiental (1-5)

        **Aplicación del Método AHP:**
        - Con base en estos scores, se construyó una matriz de comparación por pares entre métricas
        - Se utilizó la escala de Saaty (1, 3, 5, 7, 9 y sus recíprocos)
        - Esta matriz refleja qué tan importante es una métrica en relación con otra

        **Resultado Final:**
        - Se calculó un vector de pesos normalizado
        - Todos los pesos suman 1
        - Representa la importancia relativa de cada métrica dentro del índice de sostenibilidad ambiental
        """)

def show_manual_adjustment():
    """Shows the interface for manual weight adjustment."""
    st.info("""
    **Instrucciones para el Ajuste Manual:**
    - Asigne un peso entre 0 y 1 a cada métrica
    - La suma total debe ser 1.0
    - Los pesos más altos indican mayor importancia
    - El sistema normalizará automáticamente si la suma no es 1.0
    """)

    with st.expander("Gestión de configuraciones personalizadas"):
        new_name = st.text_input("Guardar configuración como", "")
        save = st.button("Guardar configuración")
        if save and new_name:
            # Get current values from inputs
            current_config = {k: float(st.session_state[f"manual_weight_{k}"]) for k in METRIC_NAMES}
            if 'saved_weights' not in st.session_state:
                st.session_state.saved_weights = {}
            st.session_state.saved_weights[new_name] = current_config
            # Keep current values in state
            st.session_state.manual_weights = current_config.copy()
            st.success(f"Configuración '{new_name}' guardada correctamente.")
            # Don't rerun to maintain input values
        # Show selectbox and buttons for apply/delete if there are saved configurations
        if st.session_state.get('saved_weights'):
            selection = st.selectbox("Seleccionar configuración guardada", list(st.session_state.saved_weights.keys()))
            config_cols = st.columns(2)
            if config_cols[0].button("Aplicar configuración"):
                selected_config = st.session_state.saved_weights[selection]
                # Update manual weights dictionary
                st.session_state.manual_weights = selected_config.copy()
                # Update individual weights
                for k, v in selected_config.items():
                    st.session_state[f"manual_weight_{k}"] = float(v)
                # Force input updates
                st.session_state.update({f"manual_weight_{k}": float(v) for k, v in selected_config.items()})
                st.success(f"Configuración '{selection}' aplicada correctamente.")
                st.rerun()
            if config_cols[1].button("Eliminar configuración"):
                del st.session_state.saved_weights[selection]
                st.success(f"Configuración '{selection}' eliminada correctamente.")
                st.rerun()
        if st.button("Reiniciar configuración"):
            reset_manual_weights()
            st.rerun()

    # Active configuration message before manual inputs
    current_weights = {k: st.session_state.get(f"manual_weight_{k}", 0) for k in METRIC_NAMES}
    recommended_weights = RECOMMENDED_WEIGHTS
    if to_dict_flat(current_weights) == to_dict_flat(recommended_weights):
        st.success("**Configuración activa: Pesos Recomendados**")
    else:
        # Check if current weights match any saved configuration
        active_config_name = "Pesos Manuales Personalizados"
        for config_name, config in st.session_state.saved_weights.items():
            if to_dict_flat(config) == to_dict_flat(current_weights):
                active_config_name = f"Configuración Manual: {config_name}"
                break
        st.success(f"**Configuración activa: {active_config_name}**")

    user_weights = {}
    for id, metric_name in METRIC_NAMES.items():
        # Get current weight value
        current_value = st.session_state.get(f"manual_weight_{id}")
        if current_value is None:
            current_value = float(st.session_state.manual_weights.get(id, RECOMMENDED_WEIGHTS[id]))
            st.session_state[f"manual_weight_{id}"] = current_value
        
        value = st.number_input(
            f"{metric_name}",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            format="%.3f",
            value=current_value,
            key=f"manual_weight_{id}"
        )
        user_weights[id] = float(value)
        # Update manual weights dictionary
        st.session_state.manual_weights[id] = float(value)

    # Ensure all metrics are present
    for id in METRIC_NAMES:
        if id not in user_weights:
            user_weights[id] = float(st.session_state.get(f"manual_weight_{id}", RECOMMENDED_WEIGHTS[id]))

    temp_total = sum(user_weights.values())
    st.metric("Suma total de pesos", f"{temp_total:.3f}")

    user_weights, is_valid = validate_manual_weights(user_weights)
    if not is_valid:
        st.warning("Los pesos fueron normalizados automáticamente para que sumen 1.")
        with st.expander("Ver pesos normalizados"):
            st.write("Los siguientes pesos normalizados serán utilizados en el cálculo:")
            for id, value in user_weights.items():
                st.write(f"{METRIC_NAMES[id]}: {value:.3f}")
            st.write(f"Suma total normalizada: {sum(user_weights.values()):.3f}")

    return user_weights

def show_calculated_weights():
    """Shows the interface for AHP calculated weights."""
    st.info("""
    **Matriz de Comparación por Pares:**
    - Este método le permite comparar la importancia relativa de cada par de métricas
    - Se utiliza la escala de Saaty para las comparaciones
    - El sistema verificará la consistencia de sus comparaciones
    - Se recomienda comenzar comparando las métricas más importantes entre sí
    - En caso de que no se realice el cálculo, se usarán los pesos recomendados.
    """)
    
    # Show active configuration if there are calculated weights
    if 'ahp_weights' in st.session_state and st.session_state.ahp_weights is not None:
        config_name = "Pesos Calculados"  # default value
        for config_name, config in st.session_state.ahp_configurations.items():
            if to_dict_flat(config['weights']) == to_dict_flat(st.session_state.ahp_weights):
                config_name = f"Configuración Calculada: {config_name}"
                break
        st.success(f"**Configuración activa:** {config_name}")
    
    if st.button("Editar matriz de comparación por pares"):
        st.session_state.saved_weight_mode = st.session_state.weight_mode_radio
        st.session_state.ahp_matrix_open = True
        st.rerun()
    
    # Show calculated weights summary table if they exist
    if 'ahp_weights' in st.session_state and st.session_state.ahp_weights is not None:
        # Show only weights table without message
        weights = st.session_state.ahp_weights
        clean_weights = {}
        for k, v in weights.items():
            if isinstance(v, dict):
                val = list(v.values())[0]
            elif isinstance(v, pd.Series):
                val = v.iloc[0]
            else:
                val = v
            try:
                clean_weights[k] = float(val)
            except (ValueError, TypeError):
                continue
        
        # Create DataFrame with weights
        metrics_list = list(clean_weights.keys())
        weights_list = [float(clean_weights[k]) for k in metrics_list]
        names_list = [METRIC_NAMES[k] for k in metrics_list]
        weights_df = pd.DataFrame({
            'Métrica': names_list,
            'Peso': weights_list
        })
        
        # Add relative importance column with balanced criteria
        weights_df['Importancia'] = weights_df['Peso'].apply(
            lambda x: '🔴 Alta' if x >= 0.20 else '🟡 Media' if 0.10 < x < 0.20 else '🟢 Baja'
        )
        st.dataframe(weights_df.style.format({'Peso': '{:.3f}'}), use_container_width=True)
        
        # Add expander for calculated weights configuration management
        with st.expander("Gestión de configuraciones de pesos calculados"):
            if 'ahp_configurations' not in st.session_state:
                st.session_state.ahp_configurations = {}
            new_name = st.text_input("Guardar configuración como", "")
            if st.button("Guardar configuración") and new_name:
                current_config = {
                    'weights': st.session_state.ahp_weights,
                    'rc': st.session_state.ahp_results['rc'] if 'ahp_results' in st.session_state else None,
                    'matrix': st.session_state.comparison_matrix.copy()
                }
                st.session_state.ahp_configurations[new_name] = current_config
                st.success(f"Configuración '{new_name}' guardada correctamente.")
                st.rerun()
            if st.session_state.ahp_configurations:
                selection = st.selectbox("Seleccionar configuración guardada", list(st.session_state.ahp_configurations.keys()))
                config_cols = st.columns(2)
                if config_cols[0].button("Aplicar configuración"):
                    config = st.session_state.ahp_configurations[selection]
                    st.session_state.ahp_weights = config['weights']
                    st.session_state.comparison_matrix = config['matrix']
                    if 'ahp_results' not in st.session_state:
                        st.session_state.ahp_results = {}
                    st.session_state.ahp_results['weights'] = config['weights']
                    st.session_state.ahp_results['rc'] = config['rc']
                    st.success(f"Configuración '{selection}' aplicada correctamente.")
                    st.rerun()
                if config_cols[1].button("Eliminar configuración"):
                    del st.session_state.ahp_configurations[selection]
                    st.success(f"Configuración '{selection}' eliminada correctamente.")
                    st.rerun()

def show_weights_interface():
    """Shows the weights interface for weight gestion."""
    st.subheader("Ajuste de Pesos por Métrica")

    with st.expander("Información sobre los métodos de asignación de pesos"):
        st.markdown("""
        ### Método de Asignación de Pesos
        El sistema ofrece tres formas de asignar pesos a las métricas:

        1. **Pesos Recomendados**: 
           - Basados en análisis y alineación con ODS
           - Ideal para usuarios que buscan una evaluación estándar
           - No requiere configuración adicional

        2. **Ajuste Manual**:
           - Permite personalizar los pesos según necesidades específicas
           - Útil cuando se tiene conocimiento experto del dominio
           - Los pesos deben sumar 1.0

        3. **Calcular nuevos pesos**:
           - Utiliza la Matriz de Comparación por Pares
           - Requiere evaluar la importancia relativa entre métricas
           - Incluye verificación de consistencia
        """)
    
    weight_mode = st.radio(
        "Selecciona el método de asignación de pesos:",
        ("Pesos Recomendados", "Ajuste Manual", "Calcular nuevos pesos"),
        key="weight_mode_radio"
    )
    
    if weight_mode == "Pesos Recomendados":
        show_recommended_weights()
        return RECOMMENDED_WEIGHTS
    elif weight_mode == "Ajuste Manual":
        return show_manual_adjustment()
    else:  # Calcular nuevos pesos
        show_calculated_weights()
        if 'ahp_weights' in st.session_state and st.session_state.ahp_weights is not None:
            return st.session_state.ahp_weights
        return RECOMMENDED_WEIGHTS 