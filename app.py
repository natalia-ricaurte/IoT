
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

st.markdown("## Criterios de Ajuste de Pesos")
with st.expander("Ver explicación del porqué de los pesos asignados"):
    st.markdown("""
    Las siguientes ponderaciones representan la importancia relativa de cada métrica en el índice de sostenibilidad. Estas ponderaciones pueden ser modificadas por el usuario según su enfoque institucional o particular.

- **Consumo de energía (0.22)**: 
  Mayor peso porque impacta directamente en la sostenibilidad del despliegue IoT. Está relacionado con el ODS 7 (Energía asequible y no contaminante). El consumo eléctrico de los dispositivos define su eficiencia operativa a gran escala.

- **Huella de carbono (0.18)**: 
  Se le asigna un peso alto porque mide el impacto ambiental total del dispositivo en términos de emisiones. Alineado con el ODS 13 (Acción por el clima), refleja el compromiso con la mitigación del cambio climático.

- **Uso de energía renovable (0.18)**: 
  Fundamental para reducir la dependencia de fuentes fósiles, lo que se traduce en una menor huella ambiental. Relevante para los ODS 7 y 12 (Consumo y producción responsables).

- **Eficiencia energética (0.14)**: 
  Relacionado con cómo se usa la energía en función de la cantidad de operaciones realizadas. Afecta la optimización de recursos y se conecta con el ODS 7, enfocado en eficiencia energética.

- **Generación de E-Waste (0.12)**: 
  Evalúa el impacto de los residuos electrónicos en la economía circular. Alineado con el ODS 12 (Producción y consumo responsables), promueve el diseño para desensamblaje y menor desecho.

- **Consumo de agua (0.08)**: 
  Se le asigna un peso menor porque no todos los dispositivos IoT impactan significativamente en el uso del agua. Sin embargo, es relevante para sectores específicos como agricultura o smart cities (ODS 6 - Agua limpia y saneamiento).

- **Reciclabilidad de materiales (0.05)**: 
  Tiene un menor peso en la evaluación individual del dispositivo, pero sigue siendo relevante para la economía circular (ODS 12). Dispositivos más reciclables reducen el impacto post-uso.

- **Mantenimiento (0.03)**: 
  Representa el impacto de acciones como reemplazo de baterías o componentes. Aunque de bajo peso, se considera para reflejar el impacto total durante la vida útil del dispositivo. 
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
            st.markdown(texto_explicacion_pesos())


    elif modo_pesos == "Ajustar pesos manualmente":
        st.info("Ingresa el peso de cada métrica (entre 0 y 1). La suma debe ser 1.")
        
        if 'config_activa' not in st.session_state:
            if st.session_state.pesos_manuales == obtener_pesos_recomendados():
                st.session_state.config_activa = "Recomendados"

        if 'pesos_guardados' not in st.session_state:
            st.session_state.pesos_guardados = {}

        with st.expander("Gestión de configuraciones personalizadas"):
            nuevo_nombre = st.text_input("Guardar configuración como", "")
            if st.button("Guardar configuración") and nuevo_nombre:
                st.session_state.pesos_guardados[nuevo_nombre] = st.session_state.pesos_manuales.copy()
                st.session_state.config_activa = nuevo_nombre
                st.success(f"Configuración '{nuevo_nombre}' guardada y activada.")
                st.rerun()

            if st.session_state.pesos_guardados:
                seleccion = st.selectbox("Seleccionar configuración guardada", list(st.session_state.pesos_guardados.keys()))
                col_config = st.columns(2)
                if col_config[0].button("Aplicar configuración"):
                    st.session_state.pesos_manuales = st.session_state.pesos_guardados[seleccion].copy()
                    st.session_state.config_activa = seleccion
                    st.rerun()
                if col_config[1].button("Eliminar configuración"):
                    del st.session_state.pesos_guardados[seleccion]
                    st.success(f"Configuración '{seleccion}' eliminada.")
                    st.rerun()
            
            if st.button("Reiniciar configuracion"):
                for k, v in obtener_pesos_recomendados().items():
                    st.session_state[f"peso_manual_{k}"] = v
                st.session_state.pesos_manuales = obtener_pesos_recomendados().copy()
                st.session_state.config_activa = "Recomendados"
                st.rerun()

        nombre = st.session_state.get('config_activa')
        if nombre and nombre != "Recomendados":
            st.success(f"Configuración activa: '{nombre}'")
        elif nombre == "Recomendados":
            st.info("Configuración activa: Recomendados")
        else:
            st.warning("Configuración activa: Personalizada")

        pesos_usuario = {}
        total_temporal = 0


        for id, nombre_metrica in NOMBRES_METRICAS.items():
            valor = st.number_input(
                f"{nombre_metrica}",
                min_value=0.0,
                max_value=1.0,
                step=0.01,
                format="%.3f",
                value=st.session_state.pesos_manuales.get(id, 0.1),
                key=f"peso_manual_{id}"
            )
            pesos_usuario[id] = valor
            total_temporal += valor

        st.metric("Suma total de pesos", f"{total_temporal:.3f}")

        for k in NOMBRES_METRICAS:
            actual = st.session_state.get(f"peso_manual_{k}", 0)
            original = st.session_state.pesos_manuales.get(k, 0)
            if abs(actual - original) > 1e-6:
                st.session_state.config_activa = None
                break


        pesos_usuario, es_valido = validar_pesos_manuales(pesos_usuario)
        if not es_valido:
            st.warning("Los pesos fueron normalizados automáticamente para que sumen 1.")


    elif modo_pesos == "Calcular pesos con AHP":
        st.warning("Esta funcionalidad está en desarrollo. Pronto podrás comparar métricas usando la escala de Saaty.")
        pesos_usuario = obtener_pesos_recomendados()  # fallback temporal

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
