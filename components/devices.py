import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from components.charts import radar_chart
from utils.constants import METRIC_NAMES_ES

def show_device(device, idx):
    """Shows the chart, recommendations and complete details of the device."""
    if device.get("calculation_done", False) and "result" in device:
        result = device["result"]
        name = device["name"]

        # Create columns to organize the layout
        col1, col2 = st.columns([2, 1])

        # Chart on the left
        with col1:
            st.markdown(f"### {name}")
            radar_chart(
                result["normalized_metrics"], 
                f"Métricas Normalizadas - {name}",
                key=f"radar_{idx}"
            )

        # Recommendations on the right
        with col2:
            st.metric("Índice de Sostenibilidad", f"{result['sustainability_index']:.2f}/10")
            st.markdown("### Recomendaciones")
            recommendations = []

            if result['normalized_metrics']['RE'] < 5:
                recommendations.append("Aumentar uso de energía renovable.")
            if result['normalized_metrics']['PD'] < 5:
                recommendations.append("Incrementar durabilidad del hardware.")
            if result['normalized_metrics']['MT'] < 5:
                recommendations.append("Reducir impacto de mantenimiento.")
            if result['normalized_metrics']['EE'] < 5:
                recommendations.append("Mejorar eficiencia energética.")
            if result['sustainability_index'] < 6:
                recommendations.append("Revisar métricas críticas para mejorar el índice global.")

            for rec_idx, rec in enumerate(recommendations):
                st.button(rec, disabled=True, key=f"rec_{idx}_{rec_idx}")

        # --- Detail sections ---
        st.markdown("#### Detalles completos del dispositivo")
        with st.expander("Datos de entrada del dispositivo"):
            field_names = {
                'name': 'Nombre del dispositivo',
                'power': 'Potencia (W)',
                'hours': 'Horas de uso diario',
                'days': 'Días de uso al año',
                'weight': 'Peso del dispositivo (kg)',
                'life': 'Vida útil (años)',
                'renewable_energy': 'Energía renovable (%)',
                'functionality': 'Funcionalidad (1-10)',
                'recyclability': 'Reciclabilidad (%)',
                'B': 'Baterías vida útil',
                'Wb': 'Peso batería (g)',
                'M': 'Mantenimientos',
                'C': 'Componentes reemplazados',
                'Wc': 'Peso componente (g)',
                'W0': 'Peso nuevo (g)',
                'W': 'Peso final (g)'
            }
            data = {field_names[k]: v for k, v in device.items() if k in field_names}
            # Convert all values to float to ensure consistency
            data = {k: float(v) if isinstance(v, (int, float)) else v for k, v in data.items()}
            df_data = pd.DataFrame(data, index=[0]).T
            df_data.columns = ['Valor']
            st.dataframe(df_data, use_container_width=True)

        with st.expander("Pesos utilizados"):
            # Get weights from snapshot if available
            weights_snapshot = device.get('weights_snapshot', {})
            weights = weights_snapshot.get('manual_weights', {})
            
            # If no weights in snapshot, try to get them from used_weights
            if not weights:
                weights = device.get('used_weights', {})
                if not isinstance(weights, dict):
                    try:
                        if isinstance(weights, str):
                            import json
                            weights = json.loads(weights)
                        elif isinstance(weights, (list, tuple)):
                            weights = dict(weights)
                        else:
                            weights = {}
                    except Exception:
                        weights = {}
            
            # Clean and ensure all values are floats
            clean_weights = {}
            for k, v in weights.items():
                try:
                    if isinstance(v, dict):
                        v = list(v.values())[0]
                    clean_weights[k] = float(v)
                except Exception:
                    continue
            
            if clean_weights:
                # Show the explicitly saved configuration name
                config_name = weights_snapshot.get('config_name', 'Desconocido')
                st.markdown(f"**Configuración de pesos:** {config_name}")
                df_weights = pd.DataFrame.from_dict(clean_weights, orient='index', columns=['Peso'])
                df_weights.index = df_weights.index.map(METRIC_NAMES_ES)
                df_weights = df_weights.rename_axis('Métrica').reset_index()
                st.dataframe(df_weights.style.format({'Peso': '{:.3f}'}), use_container_width=True)
            else:
                st.info('No se registraron pesos para este dispositivo.')

        # Checkbox and confirmation for deletion
        delete_key = f'eliminar_{device["id"]}'
        if st.checkbox('Eliminar dispositivo', key=delete_key):
            st.warning('¿Estás seguro de que deseas eliminar este dispositivo? Esta acción no se puede deshacer.')
            if st.button('Confirmar eliminación', key=f'confirmar_{device["id"]}'):
                st.session_state.devices = [d for d in st.session_state.devices if d["id"] != device["id"]]
                # Delete global results and related variables whenever a device is deleted
                for var in ["global_result", "global_calculation_date", "show_ahp_weights_table", "ahp_weights", "ahp_results"]:
                    if var in st.session_state:
                        del st.session_state[var]
                st.success(f"Dispositivo '{name}' eliminado correctamente.")
                st.rerun()

def show_global_results():
    """Shows the global results of the system."""
    if "global_result" not in st.session_state or st.session_state["global_result"] is None:
        return

    st.markdown("---")
    global_result = st.session_state.global_result
    total_average = global_result["total_average"]
    metrics_average = global_result["metrics_average"]

    # Average chart on the left
    col1, col2 = st.columns([2, 1])
    with col1:
        radar_chart(metrics_average, "Promedio de Métricas Normalizadas", key="average_metrics_radar")
    # Global recommendations on the right
    with col2:
        st.metric("Índice de Sostenibilidad Global", f"{total_average:.2f}/10")
        st.markdown("### Recomendaciones Globales")
        global_recommendations = []
        if metrics_average['RE'] < 5:
            global_recommendations.append("Aumentar uso de energía renovable.")
        if metrics_average['PD'] < 5:
            global_recommendations.append("Incrementar durabilidad del hardware.")
        if metrics_average['MT'] < 5:
            global_recommendations.append("Reducir impacto de mantenimiento.")
        if metrics_average['EE'] < 5:
            global_recommendations.append("Mejorar eficiencia energética.")
        if total_average < 6:
            global_recommendations.append("Revisar métricas críticas para mejorar el índice global.")
        for rec_idx, rec in enumerate(global_recommendations):
            st.button(rec, disabled=True, key=f"global_rec_{rec_idx}")

    # --- System details ---
    with st.expander("Detalles del sistema"):
        devices = st.session_state.devices
        included_devices = [d for d in devices if st.session_state.selected_devices.get(d['id'], True)]
        
        st.markdown(f"**Cantidad total de dispositivos evaluados:** {len(included_devices)}")
        if len(devices) != len(included_devices):
            st.info(f"⚠️ Nota: {len(devices) - len(included_devices)} dispositivos fueron excluidos del cálculo.")
            
        indices = [d['result']['sustainability_index'] for d in included_devices if 'result' in d]
        if len(indices) > 1:
            std = np.std(indices)
            st.markdown(f"**Desviación estándar de los índices individuales:** {std:.2f}")
        else:
            st.markdown("**Desviación estándar de los índices individuales:** N/A")
            
        if 'global_calculation_date' not in st.session_state or st.session_state.global_calculation_date is None:
            st.session_state.global_calculation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.markdown(f"**Fecha y hora del cálculo global:** {st.session_state.global_calculation_date}")
        
        used_weights = [str(d.get('used_weights', {})) for d in included_devices]
        if len(set(used_weights)) > 1:
            st.warning("Atención: los dispositivos fueron evaluados con diferentes configuraciones de pesos. Los índices individuales pueden no ser directamente comparables.")
        
        # Añadir tabla de métricas globales
        st.markdown("**Promedios Globales por Métrica de Sostenibilidad**")
        
        # Guía de interpretación
        st.info("""
        📊 **Guía de interpretación:**
        - Valores cercanos a 10 indican alto desempeño ambiental
        - Valores bajos indican áreas con potencial de mejora
        """)
        
        # Crear DataFrame con métricas y valores
        metrics_df = pd.DataFrame({
            'Métrica': list(METRIC_NAMES_ES.values()),
            'Valor Normalizado': [metrics_average[k] for k in METRIC_NAMES_ES.keys()]
        })
        
        # Ordenar por valor normalizado descendente
        metrics_df = metrics_df.sort_values('Valor Normalizado', ascending=False)
        
        # Añadir columna de Desempeño
        metrics_df['Desempeño'] = metrics_df['Valor Normalizado'].apply(
            lambda x: '🟢 Alto' if x >= 8 else '🟡 Moderado' if x >= 5 else '🔴 Bajo'
        )
        
        # Crear barras de progreso HTML
        def create_progress_bar(value):
            percentage = (value / 10) * 100
            # Definir color según el valor
            if value >= 8:
                color = '#5fba7d'  # Verde para alto desempeño
            elif value >= 5:
                color = '#ffd700'  # Amarillo para desempeño moderado
            else:
                color = '#ff6b6b'  # Rojo para bajo desempeño
                
            return f'<div style="width: 100px; height: 8px; background-color: #e9ecef; border-radius: 4px;">' \
                   f'<div style="width: {percentage}%; height: 100%; background-color: {color}; border-radius: 4px;"></div>' \
                   f'</div>'
        
        # Aplicar barras de progreso
        metrics_df['Valor Normalizado'] = metrics_df['Valor Normalizado'].apply(
            lambda x: f"{create_progress_bar(x)} {x:.2f}"
        )
        
        # Reordenar columnas
        metrics_df = metrics_df[['Métrica', 'Valor Normalizado', 'Desempeño']]
        
        # Mostrar la tabla con formato HTML
        st.markdown(metrics_df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        # Mostrar las métricas más altas y más bajas
        st.markdown(f"""
        **Métricas más destacadas:**
        - 🏆 Mejor desempeño: {metrics_df.iloc[0]['Métrica']} ({metrics_average[list(METRIC_NAMES_ES.keys())[0]]:.2f})
        - ⚠️ Necesita atención: {metrics_df.iloc[-1]['Métrica']} ({metrics_average[list(METRIC_NAMES_ES.keys())[-1]]:.2f})
        """)
            
        st.markdown("**Dispositivos incluidos en el cálculo global**")
        if included_devices:
            device_data = {
                'Nombre': [d['name'] for d in included_devices],
                'Índice de Sostenibilidad': [float(d['result']['sustainability_index']) if 'result' in d else None for d in included_devices]
            }
            df_devices = pd.DataFrame(device_data)
            st.dataframe(df_devices.style.format({'Índice de Sostenibilidad': '{:.2f}'}), use_container_width=True)
        else:
            st.info('No hay dispositivos incluidos actualmente.') 