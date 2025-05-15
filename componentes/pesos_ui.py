import streamlit as st
import pandas as pd
from utilidades.constantes import NOMBRES_METRICAS
from pesos import obtener_pesos_recomendados, validar_pesos_manuales
from utilidades.manejo_datos import to_dict_flat

def inicializar_pesos_manuales():
    """Inicializa los pesos manuales con los valores recomendados."""
    pesos_recomendados = obtener_pesos_recomendados()
    for k, v in pesos_recomendados.items():
        st.session_state[f"peso_manual_{k}"] = float(v)

def mostrar_pesos_recomendados():
    """Muestra la interfaz para los pesos recomendados."""
    pesos_usuario = obtener_pesos_recomendados()
    st.success("Se han cargado los pesos recomendados del modelo AHP+ODS.")

    df_pesos = pd.DataFrame.from_dict(pesos_usuario, orient='index', columns=['Peso'])
    df_pesos.index = df_pesos.index.map(NOMBRES_METRICAS)
    df_pesos = df_pesos.rename_axis('Métrica').reset_index()
    
    # Agregar columna de importancia relativa
    df_pesos['Importancia'] = df_pesos['Peso'].apply(
        lambda x: '🔴 Alta' if x >= 0.20 else '🟡 Media' if 0.10 < x < 0.20 else '🟢 Baja'
    )
    
    st.dataframe(df_pesos.style.format({'Peso': '{:.3f}'}), use_container_width=True)

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

def mostrar_ajuste_manual():
    """Muestra la interfaz para el ajuste manual de pesos."""
    st.info("""
    **Instrucciones para el Ajuste Manual:**
    - Asigne un peso entre 0 y 1 a cada métrica
    - La suma total debe ser 1.0
    - Los pesos más altos indican mayor importancia
    - El sistema normalizará automáticamente si la suma no es 1.0
    """)

    with st.expander("Gestión de configuraciones personalizadas"):
        nuevo_nombre = st.text_input("Guardar configuración como", "")
        guardar = st.button("Guardar configuración")
        if guardar and nuevo_nombre:
            config_actual = {k: float(st.session_state[f"peso_manual_{k}"]) for k in NOMBRES_METRICAS}
            if 'pesos_guardados' not in st.session_state:
                st.session_state.pesos_guardados = {}
            st.session_state.pesos_guardados[nuevo_nombre] = config_actual
            st.success(f"Configuración '{nuevo_nombre}' guardada correctamente.")
            st.rerun()
        # Mostrar selectbox y botones para aplicar/eliminar si hay configuraciones guardadas
        if st.session_state.get('pesos_guardados'):
            seleccion = st.selectbox("Seleccionar configuración guardada", list(st.session_state.pesos_guardados.keys()))
            col_config = st.columns(2)
            if col_config[0].button("Aplicar configuración"):
                st.session_state.pesos_manuales = st.session_state.pesos_guardados[seleccion].copy()
                for k in NOMBRES_METRICAS:
                    st.session_state[f"peso_manual_{k}"] = st.session_state.pesos_manuales[k]
                st.success(f"Configuración '{seleccion}' aplicada correctamente.")
                st.rerun()
            if col_config[1].button("Eliminar configuración"):
                del st.session_state.pesos_guardados[seleccion]
                st.success(f"Configuración '{seleccion}' eliminada correctamente.")
                st.rerun()
        if st.button("Reiniciar configuración"):
            inicializar_pesos_manuales()
            st.rerun()

    # Mensaje de configuración activa antes de los inputs manuales
    pesos_actuales = {k: st.session_state.get(f"peso_manual_{k}", 0) for k in NOMBRES_METRICAS}
    pesos_recomendados = obtener_pesos_recomendados()
    if to_dict_flat(pesos_actuales) == to_dict_flat(pesos_recomendados):
        st.success("**Configuración activa: Pesos Recomendados**")
    else:
        st.success("**Configuración activa: Pesos Manuales Personalizados**")

    pesos_usuario = {}
    for id, nombre_metrica in NOMBRES_METRICAS.items():
        valor_default = float(st.session_state.get(f"peso_manual_{id}", obtener_pesos_recomendados()[id]))
        valor = st.number_input(
            f"{nombre_metrica}",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            format="%.3f",
            value=valor_default,
            key=f"peso_manual_{id}"
        )
        pesos_usuario[id] = float(valor)

    # Asegurar que todas las métricas están presentes
    for id in NOMBRES_METRICAS:
        if id not in pesos_usuario:
            pesos_usuario[id] = float(st.session_state.get(f"peso_manual_{id}", obtener_pesos_recomendados()[id]))

    total_temporal = sum(pesos_usuario.values())
    st.metric("Suma total de pesos", f"{total_temporal:.3f}")

    pesos_usuario, es_valido = validar_pesos_manuales(pesos_usuario)
    if not es_valido:
        st.warning("Los pesos fueron normalizados automáticamente para que sumen 1.")
        with st.expander("Ver pesos normalizados"):
            st.write("Los siguientes pesos normalizados serán utilizados en el cálculo:")
            for id, valor in pesos_usuario.items():
                st.write(f"{NOMBRES_METRICAS[id]}: {valor:.3f}")
            st.write(f"Suma total normalizada: {sum(pesos_usuario.values()):.3f}")

    return pesos_usuario

def mostrar_pesos_calculados():
    """Muestra la interfaz para los pesos calculados mediante AHP."""
    st.info("""
    **Matriz de Comparación por Pares:**
    - Este método le permite comparar la importancia relativa de cada par de métricas
    - Se utiliza la escala de Saaty para las comparaciones
    - El sistema verificará la consistencia de sus comparaciones
    - Se recomienda comenzar comparando las métricas más importantes entre sí
    - En caso de que no se realice el cálculo, se usarán los pesos recomendados.
    """)
    
    # Mostrar configuración activa si hay pesos calculados
    if 'pesos_ahp' in st.session_state and st.session_state.pesos_ahp is not None:
        nombre_config = "Pesos Calculados"  # valor por defecto
        for nombre_config, config in st.session_state.configuraciones_ahp.items():
            if to_dict_flat(config['pesos']) == to_dict_flat(st.session_state.pesos_ahp):
                nombre_config = f"Configuración Calculada: {nombre_config}"
                break
        st.success(f"**Configuración activa:** {nombre_config}")
    
    if st.button("Editar matriz de comparación por pares"):
        st.session_state.modo_pesos_guardado = st.session_state.modo_pesos_radio
        st.session_state.matriz_ahp_abierta = True
        st.rerun()
    
    # Mostrar la tabla resumen de pesos calculados si existen
    if 'pesos_ahp' in st.session_state and st.session_state.pesos_ahp is not None:
        # Mostrar solo la tabla de pesos sin el mensaje
        pesos = st.session_state.pesos_ahp
        pesos_limpios = {}
        for k, v in pesos.items():
            if isinstance(v, dict):
                val = list(v.values())[0]
            elif isinstance(v, pd.Series):
                val = v.iloc[0]
            else:
                val = v
            pesos_limpios[k] = float(val)
        
        # Crear DataFrame con los pesos
        metricas_list = list(pesos_limpios.keys())
        pesos_list = [pesos_limpios[k] for k in metricas_list]
        nombres_list = [NOMBRES_METRICAS[k] for k in metricas_list]
        df_pesos = pd.DataFrame({
            'Métrica': nombres_list,
            'Peso': pesos_list
        })
        
        # Agregar columna de importancia relativa con criterios equilibrados
        df_pesos['Importancia'] = df_pesos['Peso'].apply(
            lambda x: '🔴 Alta' if x >= 0.20 else '🟡 Media' if 0.10 < x < 0.20 else '🟢 Baja'
        )
        st.dataframe(df_pesos.style.format({'Peso': '{:.3f}'}), use_container_width=True)
        
        # Añadir expander de gestión de configuraciones de pesos calculados
        with st.expander("Gestión de configuraciones de pesos calculados"):
            if 'configuraciones_ahp' not in st.session_state:
                st.session_state.configuraciones_ahp = {}
            nuevo_nombre = st.text_input("Guardar configuración como", "")
            if st.button("Guardar configuración") and nuevo_nombre:
                config_actual = {
                    'pesos': st.session_state.pesos_ahp,
                    'rc': st.session_state.ahp_resultados['rc'] if 'ahp_resultados' in st.session_state else None,
                    'matriz': st.session_state.matriz_comparacion.copy()
                }
                st.session_state.configuraciones_ahp[nuevo_nombre] = config_actual
                st.success(f"Configuración '{nuevo_nombre}' guardada correctamente.")
                st.rerun()
            if st.session_state.configuraciones_ahp:
                seleccion = st.selectbox("Seleccionar configuración guardada", list(st.session_state.configuraciones_ahp.keys()))
                col_config = st.columns(2)
                if col_config[0].button("Aplicar configuración"):
                    config = st.session_state.configuraciones_ahp[seleccion]
                    st.session_state.pesos_ahp = config['pesos']
                    st.session_state.matriz_comparacion = config['matriz']
                    if 'ahp_resultados' not in st.session_state:
                        st.session_state.ahp_resultados = {}
                    st.session_state.ahp_resultados['pesos'] = config['pesos']
                    st.session_state.ahp_resultados['rc'] = config['rc']
                    st.success(f"Configuración '{seleccion}' aplicada correctamente.")
                    st.rerun()
                if col_config[1].button("Eliminar configuración"):
                    del st.session_state.configuraciones_ahp[seleccion]
                    st.success(f"Configuración '{seleccion}' eliminada correctamente.")
                    st.rerun()

def mostrar_interfaz_pesos():
    """Muestra la interfaz principal para la gestión de pesos."""
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

    modo_pesos = st.radio(
        "Selecciona el método de asignación de pesos:",
        ("Pesos Recomendados", "Ajuste Manual", "Calcular nuevos pesos"),
        key="modo_pesos_radio"
    )

    if modo_pesos == "Pesos Recomendados":
        mostrar_pesos_recomendados()
        return obtener_pesos_recomendados()
    elif modo_pesos == "Ajuste Manual":
        return mostrar_ajuste_manual()
    else:  # Calcular nuevos pesos
        mostrar_pesos_calculados()
        if 'pesos_ahp' in st.session_state and st.session_state.pesos_ahp is not None:
            return st.session_state.pesos_ahp
        return obtener_pesos_recomendados() 