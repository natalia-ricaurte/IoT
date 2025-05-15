import streamlit as st
import pandas as pd
import numpy as np
from utilidades.constantes import NOMBRES_METRICAS
from pesos import ahp_attributes, razon_consistencia

def calcular_pesos_ahp(metricas):
    """Calcula los pesos usando el método AHP a partir de la matriz de comparación."""
    df_criterios = pd.DataFrame(
        st.session_state.matriz_comparacion,
        index=metricas,
        columns=metricas
    )
    pesos = ahp_attributes(df_criterios)
    ic, rc = razon_consistencia(pesos, df_criterios, verbose=False)
    return pesos, ic, rc

def mostrar_resultados_ahp(pesos, rc):
    """Muestra los resultados del cálculo de pesos por Matriz de Comparación por Pares."""
    st.success("Pesos calculados mediante la Matriz de Comparación por Pares:")
    # Convertir los pesos a un formato limpio
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
    # Mostrar razón de consistencia y advertencias
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

def mostrar_matriz_ahp():
    """Muestra la interfaz para la matriz de comparación por pares."""
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
    metricas = list(NOMBRES_METRICAS.keys())
    nombres = [NOMBRES_METRICAS[m] for m in metricas]
    n = len(metricas)
    if 'matriz_comparacion' not in st.session_state:
        st.session_state.matriz_comparacion = np.ones((n, n))
    # Encabezados de columna
    cols = st.columns(n+1)
    cols[0].write("")
    for j in range(n):
        cols[j+1].markdown(f"**{nombres[j]}**")
    # Filas de la matriz
    for i in range(n):
        row = st.columns(n+1)
        row[0].markdown(f"**{nombres[i]}**")
        for j in range(n):
            if i == j:
                row[j+1].markdown('<span style="font-weight:bold;">1.00</span>', unsafe_allow_html=True)
                st.session_state.matriz_comparacion[i, j] = 1.0
            elif i < j:
                valor = row[j+1].number_input(
                    f"Comparación {nombres[i]} vs {nombres[j]}",
                    min_value=0.11,
                    max_value=9.0,
                    value=float(st.session_state.matriz_comparacion[i, j]) if st.session_state.matriz_comparacion[i, j] != 1.0 else 1.0,
                    step=0.01,
                    key=f"matriz_{i}_{j}",
                    label_visibility="collapsed"
                )
                st.session_state.matriz_comparacion[i, j] = valor
                st.session_state.matriz_comparacion[j, i] = 1/valor
            else:
                row[j+1].write(f"{st.session_state.matriz_comparacion[i, j]:.2f}")
    st.markdown("---")
    # Botones de acción
    col_calc, col_save, col_space, col_cancel, col_reset = st.columns([1, 1, 2, 1, 1])
    with col_calc:
        if st.button("Calcular pesos"):
            df_criterios = pd.DataFrame(
                st.session_state.matriz_comparacion,
                index=metricas,
                columns=metricas
            )
            pesos = ahp_attributes(df_criterios)
            ic, rc = razon_consistencia(pesos, df_criterios, verbose=False)
            st.session_state.ahp_resultados = {
                'pesos': pesos,
                'ic': ic,
                'rc': rc
            }
            st.rerun()
    with col_save:
        if st.button("Guardar y salir"):
            if 'ahp_resultados' in st.session_state:
                pesos = st.session_state.ahp_resultados['pesos']
                if hasattr(pesos, 'to_dict'):
                    pesos = pesos.to_dict()
                st.session_state.pesos_ahp = pesos
                # Guardar los resultados para mostrar en la pantalla principal
                st.session_state.mostrar_tabla_pesos_ahp = {
                    'pesos': pesos,
                    'rc': st.session_state.ahp_resultados['rc']
                }
            st.session_state.matriz_ahp_abierta = False
            if 'modo_pesos_guardado' in st.session_state:
                st.session_state.modo_pesos_radio = st.session_state.modo_pesos_guardado
            st.rerun()
    with col_cancel:
        if st.button("Cancelar"):
            if 'ahp_resultados' in st.session_state:
                pesos = st.session_state.ahp_resultados['pesos']
                if hasattr(pesos, 'to_dict'):
                    pesos = pesos.to_dict()
                # Guardar los resultados para mostrar en la pantalla principal
                st.session_state.mostrar_tabla_pesos_ahp = {
                    'pesos': pesos,
                    'rc': st.session_state.ahp_resultados['rc']
                }
            st.session_state.matriz_ahp_abierta = False
            if 'modo_pesos_guardado' in st.session_state:
                st.session_state.modo_pesos_radio = st.session_state.modo_pesos_guardado
            st.rerun()
    with col_reset:
        if st.button("Reiniciar matriz", help="Reinicia la matriz de comparación a valores iniciales (identidad)", key="btn_reiniciar_matriz"):
            st.session_state.matriz_comparacion = np.ones((n, n))
            # Limpiar los pesos AHP y resultados anteriores
            if 'pesos_ahp' in st.session_state:
                del st.session_state.pesos_ahp
            if 'ahp_resultados' in st.session_state:
                del st.session_state.ahp_resultados
            if 'mostrar_tabla_pesos_ahp' in st.session_state:
                del st.session_state.mostrar_tabla_pesos_ahp
            st.warning("¡La matriz de comparación ha sido reiniciada a valores iniciales!")
            st.rerun()
    # Mostrar resultados si existen
    if st.session_state.get('ahp_resultados'):
        mostrar_resultados_ahp(st.session_state.ahp_resultados['pesos'], st.session_state.ahp_resultados['rc'])
    st.stop() 