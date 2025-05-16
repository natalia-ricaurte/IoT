import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from componentes.graficos import radar_chart
from utilidades.constantes import NOMBRES_METRICAS
from utilidades.auxiliares import to_dict_flat
from pesos import obtener_pesos_recomendados, validar_pesos_manuales

def mostrar_dispositivo(dispositivo, idx):
    """Muestra el gráfico, recomendaciones y detalles completos del dispositivo."""
    if dispositivo.get("calculo_realizado", False) and "resultado" in dispositivo:
        resultado = dispositivo["resultado"]
        nombre = dispositivo["nombre"]

        # Crear columnas para organizar la disposición
        col1, col2 = st.columns([2, 1])

        # Gráfico a la izquierda
        with col1:
            st.markdown(f"### {nombre}")
            radar_chart(
                resultado["metricas_normalizadas"], 
                f"Métricas Normalizadas - {nombre}",
                key=f"radar_{idx}"
            )

        # Recomendaciones a la derecha
        with col2:
            st.metric("Índice de Sostenibilidad", f"{resultado['indice_sostenibilidad']:.2f}/10")
            st.markdown("### Recomendaciones")
            recomendaciones = []

            if resultado['metricas_normalizadas']['ER'] < 5:
                recomendaciones.append("Aumentar uso de energía renovable.")
            if resultado['metricas_normalizadas']['DP'] < 5:
                recomendaciones.append("Incrementar durabilidad del hardware.")
            if resultado['metricas_normalizadas']['IM'] < 5:
                recomendaciones.append("Reducir impacto de mantenimiento.")
            if resultado['metricas_normalizadas']['EE'] < 5:
                recomendaciones.append("Mejorar eficiencia energética.")
            if resultado['indice_sostenibilidad'] < 6:
                recomendaciones.append("Revisar métricas críticas para mejorar el índice global.")

            for rec_idx, rec in enumerate(recomendaciones):
                st.button(rec, disabled=True, key=f"rec_{idx}_{rec_idx}")

        # --- Secciones de detalles ---
        st.markdown("#### Detalles completos del dispositivo")
        with st.expander("Datos de entrada del dispositivo"):
            nombres_campos = {
                'nombre': 'Nombre del dispositivo',
                'potencia': 'Potencia (W)',
                'horas': 'Horas de uso diario',
                'dias': 'Días de uso al año',
                'peso': 'Peso del dispositivo (kg)',
                'vida': 'Vida útil (años)',
                'energia_renovable': 'Energía renovable (%)',
                'funcionalidad': 'Funcionalidad (1-10)',
                'reciclabilidad': 'Reciclabilidad (%)',
                'B': 'Baterías vida útil',
                'Wb': 'Peso batería (g)',
                'M': 'Mantenimientos',
                'C': 'Componentes reemplazados',
                'Wc': 'Peso componente (g)',
                'W0': 'Peso nuevo (g)',
                'W': 'Peso final (g)'
            }
            datos = {nombres_campos[k]: v for k, v in dispositivo.items() if k in nombres_campos}
            # Convertir todos los valores a float para asegurar consistencia
            datos = {k: float(v) if isinstance(v, (int, float)) else v for k, v in datos.items()}
            df_datos = pd.DataFrame(datos, index=[0]).T
            df_datos.columns = ['Valor']
            st.dataframe(df_datos, use_container_width=True)

        with st.expander("Pesos utilizados"):
            pesos = dispositivo.get('pesos_utilizados', {})
            # Limpiar y asegurar que todos los valores sean floats
            pesos_limpios = {}
            for k, v in pesos.items():
                if isinstance(v, dict):
                    v = list(v.values())[0]
                try:
                    pesos_limpios[k] = float(v)
                except Exception:
                    continue
            if pesos_limpios:
                # Mostrar el nombre de la configuración guardado explícitamente
                nombre_config = dispositivo.get('snapshot_pesos', {}).get('nombre_configuracion', 'Desconocido')
                st.markdown(f"**Configuración de pesos:** {nombre_config}")
                df_pesos = pd.DataFrame.from_dict(pesos_limpios, orient='index', columns=['Peso'])
                df_pesos.index = df_pesos.index.map(NOMBRES_METRICAS)
                df_pesos = df_pesos.rename_axis('Métrica').reset_index()
                st.dataframe(df_pesos.style.format({'Peso': '{:.3f}'}), use_container_width=True)
            else:
                st.info('No se registraron pesos para este dispositivo.')

        # Checkbox y confirmación para eliminar
        eliminar_key = f'eliminar_{dispositivo["id"]}'
        if st.checkbox('Eliminar dispositivo', key=eliminar_key):
            st.warning('¿Estás seguro de que deseas eliminar este dispositivo? Esta acción no se puede deshacer.')
            if st.button('Confirmar eliminación', key=f'confirmar_{dispositivo["id"]}'):
                st.session_state.dispositivos = [d for d in st.session_state.dispositivos if d["id"] != dispositivo["id"]]
                # Eliminar resultados globales y relacionados siempre que se elimina un dispositivo
                for var in ["resultado_global", "fecha_calculo_global", "mostrar_tabla_pesos_ahp", "pesos_ahp", "ahp_resultados"]:
                    if var in st.session_state:
                        del st.session_state[var]
                st.success(f"Dispositivo '{nombre}' eliminado correctamente.")
                st.rerun()

def mostrar_resultados_globales():
    """Muestra los resultados globales del sistema."""
    if "resultado_global" not in st.session_state:
        return

    st.markdown("---")
    resultado_global = st.session_state.resultado_global
    promedio_total = resultado_global["promedio_total"]
    promedio_metricas = resultado_global["promedio_metricas"]

    # Gráfico del promedio a la izquierda
    col1, col2 = st.columns([2, 1])
    with col1:
        radar_chart(promedio_metricas, "Promedio de Métricas Normalizadas", key="radar_total")
    # Recomendaciones globales a la derecha
    with col2:
        st.metric("Índice de Sostenibilidad Global", f"{promedio_total:.2f}/10")
        st.markdown("### Recomendaciones Globales")
        recomendaciones_globales = []
        if promedio_metricas["ER"] < 5:
            recomendaciones_globales.append("Aumentar uso de energía renovable.")
        if promedio_metricas["DP"] < 5:
            recomendaciones_globales.append("Incrementar durabilidad del hardware.")
        if promedio_metricas["IM"] < 5:
            recomendaciones_globales.append("Reducir impacto de mantenimiento.")
        if promedio_metricas["EE"] < 5:
            recomendaciones_globales.append("Mejorar eficiencia energética.")
        if promedio_total < 6:
            recomendaciones_globales.append("Revisar métricas críticas para mejorar el índice global.")
        for rec_idx, rec in enumerate(recomendaciones_globales):
            st.button(rec, disabled=True, key=f"global_rec_{rec_idx}")

    # --- Detalles del sistema ---
    with st.expander("Detalles del sistema"):
        dispositivos = st.session_state.dispositivos
        st.markdown(f"**Cantidad total de dispositivos evaluados:** {len(dispositivos)}")
        indices = [d['resultado']['indice_sostenibilidad'] for d in dispositivos if 'resultado' in d]
        if len(indices) > 1:
            std = np.std(indices)
            st.markdown(f"**Desviación estándar de los índices individuales:** {std:.2f}")
        else:
            st.markdown("**Desviación estándar de los índices individuales:** N/A")
        if 'fecha_calculo_global' not in st.session_state:
            st.session_state.fecha_calculo_global = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        st.markdown(f"**Fecha y hora del cálculo global:** {st.session_state.fecha_calculo_global}")
        pesos_usados = [str(d.get('pesos_utilizados', {})) for d in dispositivos]
        if len(set(pesos_usados)) > 1:
            st.warning("Atención: los dispositivos fueron evaluados con diferentes configuraciones de pesos. Los índices individuales pueden no ser directamente comparables.")
        st.markdown("**Pesos utilizados para el cálculo global**")
        if "pesos_ahp" in st.session_state and st.session_state.modo_pesos_radio == "Calcular nuevos pesos":
            pesos_global = st.session_state.pesos_ahp
            nombre_config = "Pesos Calculados"
            for nombre_config, config in st.session_state.configuraciones_ahp.items():
                if to_dict_flat(config['pesos']) == to_dict_flat(pesos_global):
                    nombre_config = f"Configuración Calculada: {nombre_config}"
                    break
        elif st.session_state.modo_pesos_radio == "Ajuste Manual":
            pesos_manuales = {k: st.session_state[f"peso_manual_{k}"] for k in NOMBRES_METRICAS}
            pesos_global, _ = validar_pesos_manuales(pesos_manuales)
            nombre_config = "Pesos Manuales Personalizados"
            for nombre_config, config in st.session_state.pesos_guardados.items():
                if to_dict_flat(config) == to_dict_flat(pesos_global):
                    nombre_config = f"Configuración Manual: {nombre_config}"
                    break
        else:
            pesos_global = obtener_pesos_recomendados()
            nombre_config = "Pesos Recomendados"
        st.markdown(f"**Configuración de pesos:** {nombre_config}")
        pesos_limpios = {}
        for k, v in pesos_global.items():
            if isinstance(v, dict):
                v = list(v.values())[0]
            try:
                pesos_limpios[k] = float(v)
            except Exception:
                continue
        df_pesos = pd.DataFrame.from_dict(pesos_limpios, orient='index', columns=['Peso'])
        df_pesos.index = df_pesos.index.map(NOMBRES_METRICAS)
        df_pesos = df_pesos.rename_axis('Métrica').reset_index()
        st.dataframe(df_pesos.style.format({'Peso': '{:.3f}'}), use_container_width=True)
        st.markdown("**Dispositivos incluidos en el cálculo global**")
        if dispositivos:
            data_disp = {
                'Nombre': [d['nombre'] for d in dispositivos],
                'Índice de Sostenibilidad': [float(d['resultado']['indice_sostenibilidad']) if 'resultado' in d else None for d in dispositivos]
            }
            df_disp = pd.DataFrame(data_disp)
            st.dataframe(df_disp.style.format({'Índice de Sostenibilidad': '{:.2f}'}), use_container_width=True)
        else:
            st.info('No hay dispositivos incluidos actualmente.') 