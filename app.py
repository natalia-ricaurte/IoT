import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from modelo import SostenibilidadIoT

st.set_page_config(page_title="Dashboard Sostenibilidad IoT", layout="wide")
st.title("Dashboard de Evaluación de Sostenibilidad - Dispositivos IoT")


if "dispositivos" not in st.session_state:
    st.session_state.dispositivos = []

# Botón para reiniciar la lista de dispositivos
if st.button("Reiniciar"):
    st.session_state.dispositivos = []

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
            nombre = st.text_input("Nombre del dispositivo", "Sensor de temperatura", help="Nombre descriptivo del dispositivo IoT.")
            potencia = st.number_input("Potencia (W)", value=2.0, help="Potencia eléctrica en vatios (W) del dispositivo cuando está en funcionamiento.")
            horas = st.number_input("Horas uso diario", value=24.0, help="Cantidad de horas al día que el dispositivo está en uso.")
            dias = st.number_input("Días uso/año", value=365, help="Número de días al año que el dispositivo opera.")
            peso = st.number_input("Peso dispositivo (kg)", value=0.1, help="Peso total del dispositivo en kilogramos.")
            vida = st.number_input("Vida útil (años)", value=5, help="Duración esperada del dispositivo antes de desecharse o reemplazarse.")

        with colB:
            energia_renovable = st.slider("Energía renovable (%)", 0, 100, 30, help="Porcentaje de energía que proviene de fuentes renovables.")
            funcionalidad = st.slider("Funcionalidad (1-10)", 1, 10, 8, help="Nivel de funcionalidad y utilidad que ofrece el dispositivo.")
            reciclabilidad = st.slider("Reciclabilidad (%)", 0, 100, 65, help="Porcentaje del dispositivo que puede reciclarse al finalizar su vida útil.")

        with st.expander("Datos de mantenimiento"):
            colM1, colM2 = st.columns(2)
            with colM1:
                B = st.number_input("Baterías vida útil", value=2, help="Cantidad de baterías necesarias durante toda la vida útil del dispositivo.")
                Wb = st.number_input("Peso batería (g)", value=50, help="Peso de cada batería en gramos.")
                M = st.number_input("Mantenimientos", value=1, help="Número de veces que el dispositivo requiere mantenimiento.")
                C = st.number_input("Componentes reemplazados", value=2, help="Número de componentes reemplazados en mantenimientos.")

            with colM2:
                Wc = st.number_input("Peso componente (g)", value=20, help="Peso promedio de cada componente reemplazado en gramos.")
                W0 = st.number_input("Peso nuevo (g)", value=200, help="Peso total del dispositivo cuando es nuevo.")
                W = st.number_input("Peso final (g)", value=180, help="Peso final del dispositivo después del uso.")


        submitted = st.form_submit_button("Añadir dispositivo")

with col2:
    st.subheader("Ajuste de Peso Relativo por Métrica del Dispositivo")
    pesos_usuario = {
        'CE': st.slider("Peso CE", 0.0, 1.0, 0.22),
        'HC': st.slider("Peso HC", 0.0, 1.0, 0.18),
        'EW': st.slider("Peso EW", 0.0, 1.0, 0.12),
        'ER': st.slider("Peso ER", 0.0, 1.0, 0.18),
        'EE': st.slider("Peso EE", 0.0, 1.0, 0.14),
        'DP': st.slider("Peso DP", 0.0, 1.0, 0.08),
        'RC': st.slider("Peso RC", 0.0, 1.0, 0.05),
        'IM': st.slider("Peso IM", 0.0, 1.0, 0.03)
    }

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
    st.session_state.dispositivos.append((nombre, resultado))

if st.session_state.dispositivos:
    st.markdown("---")
    st.subheader("Resultados por Dispositivo")
    for nombre, resultado in st.session_state.dispositivos:
        st.markdown(f"### {nombre}")
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

            radar_chart(resultado["metricas_normalizadas"], f"Métricas Normalizadas - {nombre}")

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
                
# Botón para calcular el índice de sostenibilidad total y mostrar el gráfico de araña
if st.button("Calcular Índice de Sostenibilidad Total"):
    total_indices = [resultado['indice_sostenibilidad'] for _, resultado in st.session_state.dispositivos]
    promedio_total = sum(total_indices) / len(total_indices)

    # Calcular los promedios de las métricas normalizadas
    metricas_totales = [resultado["metricas_normalizadas"] for _, resultado in st.session_state.dispositivos]
    promedio_metricas = {key: sum(d[key] for d in metricas_totales) / len(metricas_totales) for key in metricas_totales[0]}

    # Mostrar el índice total
    st.success(f"El Índice de Sostenibilidad Total es: {promedio_total:.2f}/10")

    # Mostrar el gráfico de araña para los promedios
    st.subheader("Gráfico de Araña - Promedio de Métricas")
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

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.plot(angles, valores, color='teal', linewidth=2)
        ax.fill(angles, valores, color='skyblue', alpha=0.4)
        ax.set_yticks([2, 4, 6, 8, 10])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_title(titulo, y=1.1)
        st.pyplot(fig)

    radar_chart(promedio_metricas, "Promedio de Métricas Normalizadas")