import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from pesos import (
    obtener_pesos_recomendados,
    validar_pesos_manuales,
    texto_explicacion_pesos,
    NOMBRES_METRICAS
)
from modelo import SostenibilidadIoT

# --- BLOQUE DE MATRIZ AHP EN PANTALLA COMPLETA ---
if 'matriz_ahp_abierta' not in st.session_state:
    st.session_state.matriz_ahp_abierta = False
if 'pesos_ahp' not in st.session_state:
    st.session_state.pesos_ahp = None

if st.session_state.matriz_ahp_abierta:
    metricas = list(NOMBRES_METRICAS.keys())
    n = len(metricas)
    st.title("Matriz de Comparación por Pares (AHP)")
    st.info("Completa la matriz de comparación por pares usando la escala de Saaty. Solo debes llenar la mitad superior, el resto se calcula automáticamente.")
    st.markdown("""
    **Escala de Saaty:**
    - 1: Igual importancia
    - 3: Moderadamente más importante
    - 5: Fuertemente más importante
    - 7: Muy fuertemente más importante
    - 9: Extremadamente más importante
    - Valores intermedios (2,4,6,8) cuando sea necesario
    - Si la métrica de la fila es MENOS importante que la de la columna, usa el recíproco (por ejemplo, 1/3, 1/5, etc.)
    """)
    # Inicializar la matriz de comparación en session_state si no existe
    if 'matriz_comparacion' not in st.session_state:
        matriz = np.ones((n, n))
        st.session_state.matriz_comparacion = matriz
    # Mostrar la matriz editable
    st.write("### Matriz de Comparación por Pares")
    cols = st.columns(n+1)
    cols[0].write("")
    for j in range(n):
        cols[j+1].markdown(f"**{NOMBRES_METRICAS[metricas[j]]}**")
    for i in range(n):
        row = st.columns(n+1)
        row[0].markdown(f"**{NOMBRES_METRICAS[metricas[i]]}**")
        for j in range(n):
            if i == j:
                row[j+1].write("1.00")
                st.session_state.matriz_comparacion[i, j] = 1.0
            elif i < j:
                valor = row[j+1].number_input(
                    label=f"{metricas[i]} vs {metricas[j]}",
                    min_value=0.11,
                    max_value=9.0,
                    value=float(st.session_state.matriz_comparacion[i, j]) if st.session_state.matriz_comparacion[i, j] != 1.0 else 1.0,
                    step=0.01,
                    key=f"matriz_{i}_{j}"
                )
                st.session_state.matriz_comparacion[i, j] = valor
                st.session_state.matriz_comparacion[j, i] = 1/valor
            elif i > j:
                row[j+1].write(f"{st.session_state.matriz_comparacion[i, j]:.2f}")
    col_save, col_cancel = st.columns([1,1])
    with col_save:
        if st.button("Calcular y guardar pesos AHP"):
            df_criterios = pd.DataFrame(
                st.session_state.matriz_comparacion,
                index=metricas,
                columns=metricas
            )
            suma_columnas = np.array(df_criterios.sum(numeric_only=True))
            matriz_normalizada = df_criterios.div(suma_columnas, axis=1)
            pesos = pd.DataFrame(
                matriz_normalizada.mean(axis=1),
                index=df_criterios.index,
                columns=['peso']
            )
            matriz_aleatoria = {
                1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
                9: 1.45, 10: 1.49, 11: 1.51, 12: 1.48, 13: 1.56, 14: 1.57, 15: 1.59
            }
            df_temp = df_criterios.multiply(np.array(pesos['peso']), axis=1)
            df_temp['suma'] = df_temp.sum(axis=1)
            lambda_max = df_temp['suma'].div(np.array(pesos['peso'])).mean()
            ic = round((lambda_max - n) / (n - 1), 3)
            rc = round(ic / matriz_aleatoria[n], 3)
            st.session_state.pesos_ahp = pesos['peso'].to_dict()
            st.session_state.matriz_ahp_abierta = False
            st.success("Pesos calculados exitosamente")
            if rc < 0.1:
                st.success(f"Razón de Consistencia: {rc} (La matriz es consistente)")
            else:
                st.warning(f"Razón de Consistencia: {rc} (La matriz NO es consistente)")
    with col_cancel:
        if st.button("Cancelar y volver"):
            st.session_state.matriz_ahp_abierta = False
    st.stop()

st.set_page_config(page_title="Dashboard Sostenibilidad IoT", layout="wide")
st.title("Dashboard de Evaluación de Sostenibilidad - Dispositivos IoT")

st.markdown("## Descripción de Métricas")
with st.expander("Ver métricas clave del modelo"):
    st.markdown("""
    **Métricas de sostenibilidad evaluadas:**
    1. **CE - Consumo de Energía:** kWh anuales usados por el dispositivo.
    2. **HC - Huella de Carbono:** kg de CO₂eq emitidos.
    3. **EW - E-waste:** kg de residuos electrónicos generados por año.
    4. **ER - Energía Renovable:** Porcentaje de energía limpia usada.
    5. **EE - Eficiencia Energética:** Relación funcionalidad / consumo.
    6. **DP - Durabilidad del Producto:** Vida útil esperada.
    7. **RC - Reciclabilidad:** Porcentaje de materiales reciclables.
    8. **IM - Mantenimiento:** Impacto de baterías, reemplazos y desgaste.
    """)

col1, col2 = st.columns([2, 1])

with col1:
    with st.form("formulario_datos"):
        st.subheader("Datos del dispositivo IoT")
        colA, colB = st.columns(2)
        with colA:
            nombre = st.text_input("Nombre del dispositivo", "Sensor de temperatura")
            potencia = st.number_input("Potencia (W)", value=2.0)
            horas = st.number_input("Horas uso diario", value=24.0)
            dias = st.number_input("Días uso/año", value=365)
            peso = st.number_input("Peso dispositivo (kg)", value=0.1)
            vida = st.number_input("Vida útil (años)", value=5)
        with colB:
            energia_renovable = st.slider("Energía renovable (%)", 0, 100, 30)
            funcionalidad = st.slider("Funcionalidad (1-10)", 1, 10, 8)
            reciclabilidad = st.slider("Reciclabilidad (%)", 0, 100, 65)

        with st.expander("Datos de mantenimiento"):
            colM1, colM2 = st.columns(2)
            with colM1:
                B = st.number_input("Baterías vida útil", value=2)
                Wb = st.number_input("Peso batería (g)", value=50)
                M = st.number_input("Mantenimientos", value=1)
                C = st.number_input("Componentes reemplazados", value=2)
            with colM2:
                Wc = st.number_input("Peso componente (g)", value=20)
                W0 = st.number_input("Peso nuevo (g)", value=200)
                W = st.number_input("Peso final (g)", value=180)

        submitted = st.form_submit_button("Calcular")

with col2:
    st.subheader("Ajuste de Pesos por Métrica")

    if 'pesos_manuales' not in st.session_state:
        st.session_state.pesos_manuales = obtener_pesos_recomendados().copy()

    modo_pesos = st.radio(
        "Selecciona el modo de ajuste de pesos:",
        ("Usar pesos recomendados", "Ajustar pesos manualmente", "Calcular pesos con AHP")
    )

    if modo_pesos == "Usar pesos recomendados":
        pesos_usuario = obtener_pesos_recomendados()
        st.success("Se han cargado los pesos recomendados del modelo AHP+ODS.")

        df_pesos = pd.DataFrame.from_dict(pesos_usuario, orient='index', columns=['Peso'])
        df_pesos.index = df_pesos.index.map(NOMBRES_METRICAS)
        df_pesos = df_pesos.rename_axis('Métrica').reset_index()
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

    elif modo_pesos == "Ajustar pesos manualmente":
        st.info("Ingresa el peso de cada métrica (entre 0 y 1). La suma debe ser 1.")
        
        if 'pesos_guardados' not in st.session_state:
            st.session_state.pesos_guardados = {}

        with st.expander("Gestión de configuraciones personalizadas"):
            nuevo_nombre = st.text_input("Guardar configuración como", "")
            if st.button("Guardar configuración") and nuevo_nombre:
                config_actual = {k: st.session_state[f"peso_manual_{k}"] for k in NOMBRES_METRICAS}
                st.session_state.pesos_guardados[nuevo_nombre] = config_actual
                st.session_state.pesos_manuales = config_actual.copy()
                st.success(f"Configuración '{nuevo_nombre}' guardada y activada.")

            if st.session_state.pesos_guardados:
                seleccion = st.selectbox("Seleccionar configuración guardada", list(st.session_state.pesos_guardados.keys()))
                col_config = st.columns(2)
                if col_config[0].button("Aplicar configuración"):
                    st.session_state.pesos_manuales = st.session_state.pesos_guardados[seleccion].copy()
                    for k in NOMBRES_METRICAS:
                        st.session_state[f"peso_manual_{k}"] = st.session_state.pesos_manuales[k]
                    st.rerun()

                if col_config[1].button("Eliminar configuración"):
                    del st.session_state.pesos_guardados[seleccion]
                    st.success(f"Configuración '{seleccion}' eliminada.")
                    st.rerun()
            
            if st.button("Reiniciar configuracion"):
                st.session_state.pesos_manuales = obtener_pesos_recomendados().copy()
                for k in NOMBRES_METRICAS:
                    st.session_state[f"peso_manual_{k}"] = st.session_state.pesos_manuales[k]
                st.rerun()

        pesos_usuario = {}
        total_temporal = 0

        # Obtener los pesos recomendados para usar como valores por defecto
        pesos_recomendados = obtener_pesos_recomendados()

        for id, nombre_metrica in NOMBRES_METRICAS.items():
            # Inicializar el valor en session_state si no existe
            if f"peso_manual_{id}" not in st.session_state:
                st.session_state[f"peso_manual_{id}"] = pesos_recomendados[id]
            
            valor = st.number_input(
                f"{nombre_metrica}",
                min_value=0.0,
                max_value=1.0,
                step=0.01,
                format="%.3f",
                key=f"peso_manual_{id}"
            )
            pesos_usuario[id] = valor
            total_temporal += valor
            st.session_state.pesos_manuales[id] = valor

        st.metric("Suma total de pesos", f"{total_temporal:.3f}")

        pesos_usuario, es_valido = validar_pesos_manuales(pesos_usuario)
        if not es_valido:
            st.warning("Los pesos fueron normalizados automáticamente para que sumen 1.")
            with st.expander("Ver pesos normalizados"):
                st.write("Los siguientes pesos normalizados serán utilizados en el cálculo:")
                for id, valor in pesos_usuario.items():
                    st.write(f"{NOMBRES_METRICAS[id]}: {valor:.3f}")
                st.write(f"Suma total normalizada: {sum(pesos_usuario.values()):.3f}")

        pesos_usuario, es_valido = validar_pesos_manuales(pesos_usuario)
        if not es_valido:
            st.warning("Los pesos fueron normalizados automáticamente para que sumen 1.")


    elif modo_pesos == "Calcular pesos con AHP":
        # Estado para mostrar/ocultar la matriz en pantalla completa
        if 'matriz_ahp_abierta' not in st.session_state:
            st.session_state.matriz_ahp_abierta = False
        if 'pesos_ahp' not in st.session_state:
            st.session_state.pesos_ahp = None

        metricas = list(NOMBRES_METRICAS.keys())
        n = len(metricas)

        # Botón para abrir la matriz en pantalla completa
        if not st.session_state.matriz_ahp_abierta:
            if st.button("Editar matriz de comparación AHP en pantalla completa", key="abrir_ahp"):
                st.session_state.matriz_ahp_abierta = True
                st.rerun()
            # Si ya hay pesos calculados, mostrar resumen y opción de editar
            if st.session_state.pesos_ahp is not None:
                st.success("Pesos calculados con AHP:")
                df_pesos = pd.DataFrame.from_dict(st.session_state.pesos_ahp, orient='index', columns=['Peso'])
                df_pesos.index = df_pesos.index.map(NOMBRES_METRICAS)
                df_pesos = df_pesos.rename_axis('Métrica').reset_index()
                st.dataframe(df_pesos.style.format({'Peso': '{:.3f}'}), use_container_width=True)
        else:
            metricas = list(NOMBRES_METRICAS.keys())
            n = len(metricas)
            st.title("Matriz de Comparación por Pares (AHP)")
            st.info("Completa la matriz de comparación por pares usando la escala de Saaty. Solo debes llenar la mitad superior, el resto se calcula automáticamente.")
            st.markdown("""
            **Escala de Saaty:**
            - 1: Igual importancia
            - 3: Moderadamente más importante
            - 5: Fuertemente más importante
            - 7: Muy fuertemente más importante
            - 9: Extremadamente más importante
            - Valores intermedios (2,4,6,8) cuando sea necesario
            - Si la métrica de la fila es MENOS importante que la de la columna, usa el recíproco (por ejemplo, 1/3, 1/5, etc.)
            """)
            # Inicializar la matriz de comparación en session_state si no existe
            if 'matriz_comparacion' not in st.session_state:
                matriz = np.ones((n, n))
                st.session_state.matriz_comparacion = matriz
            # Mostrar la matriz editable
            st.write("### Matriz de Comparación por Pares")
            cols = st.columns(n+1)
            cols[0].write("")
            for j in range(n):
                cols[j+1].markdown(f"**{NOMBRES_METRICAS[metricas[j]]}**")
            for i in range(n):
                row = st.columns(n+1)
                row[0].markdown(f"**{NOMBRES_METRICAS[metricas[i]]}**")
                for j in range(n):
                    if i == j:
                        row[j+1].write("1.00")
                        st.session_state.matriz_comparacion[i, j] = 1.0
                    elif i < j:
                        valor = row[j+1].number_input(
                            label=f"{metricas[i]} vs {metricas[j]}",
                            min_value=0.11,
                            max_value=9.0,
                            value=float(st.session_state.matriz_comparacion[i, j]) if st.session_state.matriz_comparacion[i, j] != 1.0 else 1.0,
                            step=0.01,
                            key=f"matriz_{i}_{j}"
                        )
                        st.session_state.matriz_comparacion[i, j] = valor
                        st.session_state.matriz_comparacion[j, i] = 1/valor
                    elif i > j:
                        row[j+1].write(f"{st.session_state.matriz_comparacion[i, j]:.2f}")
            # Estado temporal para mostrar resultados sin cerrar
            if 'ahp_resultados' not in st.session_state:
                st.session_state.ahp_resultados = None
            col_calc, col_accept, col_cancel = st.columns([1,1,1])
            with col_calc:
                if st.button("Calcular pesos", key="calcular_ahp"):
                    df_criterios = pd.DataFrame(
                        st.session_state.matriz_comparacion,
                        index=metricas,
                        columns=metricas
                    )
                    suma_columnas = np.array(df_criterios.sum(numeric_only=True))
                    matriz_normalizada = df_criterios.div(suma_columnas, axis=1)
                    pesos = pd.DataFrame(
                        matriz_normalizada.mean(axis=1),
                        index=df_criterios.index,
                        columns=['peso']
                    )
                    matriz_aleatoria = {
                        1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
                        9: 1.45, 10: 1.49, 11: 1.51, 12: 1.48, 13: 1.56, 14: 1.57, 15: 1.59
                    }
                    df_temp = df_criterios.multiply(np.array(pesos['peso']), axis=1)
                    df_temp['suma'] = df_temp.sum(axis=1)
                    lambda_max = df_temp['suma'].div(np.array(pesos['peso'])).mean()
                    ic = round((lambda_max - n) / (n - 1), 3)
                    rc = round(ic / matriz_aleatoria[n], 3)
                    st.session_state.ahp_resultados = {
                        'pesos': pesos['peso'].to_dict(),
                        'ic': ic,
                        'rc': rc
                    }
            with col_accept:
                if st.session_state.ahp_resultados is not None:
                    if st.button("Aceptar y cerrar", key="aceptar_ahp"):
                        st.session_state.pesos_ahp = st.session_state.ahp_resultados['pesos']
                        st.session_state.matriz_ahp_abierta = False
                        st.session_state.ahp_resultados = None
                else:
                    st.button("Aceptar y cerrar", key="aceptar_ahp_disabled", disabled=True)
            with col_cancel:
                if st.button("Cancelar y volver", key="cancelar_ahp"):
                    st.session_state.matriz_ahp_abierta = False
                    st.session_state.ahp_resultados = None
            # Mostrar resultados si existen
            if st.session_state.ahp_resultados is not None:
                st.success("Pesos calculados (sin cerrar la matriz):")
                df_pesos = pd.DataFrame.from_dict(st.session_state.ahp_resultados['pesos'], orient='index', columns=['Peso'])
                df_pesos.index = df_pesos.index.map(NOMBRES_METRICAS)
                df_pesos = df_pesos.rename_axis('Métrica').reset_index()
                st.dataframe(df_pesos.style.format({'Peso': '{:.3f}'}), use_container_width=True)
                rc = st.session_state.ahp_resultados['rc']
                if rc < 0.1:
                    st.success(f"Razón de Consistencia: {rc} (La matriz es consistente)")
                else:
                    st.warning(f"Razón de Consistencia: {rc} (La matriz NO es consistente)")
            st.stop()

if submitted:
    sensor = SostenibilidadIoT(nombre)
    sensor.pesos = pesos_usuario
    sensor.calcular_consumo_energia(potencia, horas, dias)
    sensor.calcular_huella_carbono()
    sensor.calcular_ewaste(peso, vida)
    sensor.calcular_energia_renovable(energia_renovable)
    sensor.calcular_eficiencia_energetica(funcionalidad)
    sensor.calcular_durabilidad(vida)
    sensor.calcular_reciclabilidad(reciclabilidad)
    sensor.calcular_indice_mantenimiento(B, Wb, M, C, Wc, W0, W)
    resultado = sensor.calcular_sostenibilidad()

    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Gráfico de Araña")
        def radar_chart(metricas, titulo):
            etiquetas = {
                'CE': 'Cons. Energía', 'HC': 'Huella CO₂', 'EW': 'E-waste',
                'ER': 'Energía Renov.', 'EE': 'Eficiencia', 'DP': 'Durabilidad',
                'RC': 'Reciclabilidad', 'IM': 'Mantenimiento'
            }
            labels = [etiquetas[m] for m in metricas]
            valores = list(metricas.values())
            valores += valores[:1]
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
            ax.plot(angles, valores, color='teal', linewidth=2)
            ax.fill(angles, valores, color='skyblue', alpha=0.4)
            ax.set_yticks([2, 4, 6, 8, 10])
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels)
            ax.set_title(titulo, y=1.1)
            st.pyplot(fig)

        radar_chart(resultado["metricas_normalizadas"], "Métricas Normalizadas")

    with col4:
        st.subheader("Resultados y Recomendaciones")
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
            recomendaciones.append("Índice global bajo: revisar métricas críticas.")

        for r in recomendaciones:
            st.info(r)
