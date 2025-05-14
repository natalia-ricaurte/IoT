import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from streamlit_echarts import st_echarts

from pesos import (
    obtener_pesos_recomendados,
    validar_pesos_manuales,
    NOMBRES_METRICAS,
    razon_consistencia,
    ahp_attributes
)
from modelo import SostenibilidadIoT

def inicializar_pesos_manuales():
    """Inicializa los pesos manuales con los valores recomendados."""
    pesos_recomendados = obtener_pesos_recomendados()
    for id in NOMBRES_METRICAS:
        st.session_state[f"peso_manual_{id}"] = float(pesos_recomendados[id])
    st.session_state.pesos_manuales = pesos_recomendados.copy()

def inicializar_estado():
    """Inicializa todas las variables de estado necesarias."""
    if "dispositivos" not in st.session_state:
        st.session_state.dispositivos = []
    
    if 'matriz_ahp_abierta' not in st.session_state:
        st.session_state.matriz_ahp_abierta = False

    if 'pesos_manuales' not in st.session_state:
        inicializar_pesos_manuales()
    
    if 'pesos_guardados' not in st.session_state:
        st.session_state.pesos_guardados = {}
    
    if 'matriz_comparacion' not in st.session_state:
        metricas = list(NOMBRES_METRICAS.keys())
        n = len(metricas)
        st.session_state.matriz_comparacion = np.ones((n, n))

def reiniciar_estado():
    """Reinicia el estado de la aplicación a sus valores iniciales."""
    st.session_state.dispositivos = []
    st.session_state.matriz_ahp_abierta = False
    inicializar_pesos_manuales()
    st.session_state.pesos_guardados = {}
    metricas = list(NOMBRES_METRICAS.keys())
    n = len(metricas)
    st.session_state.matriz_comparacion = np.ones((n, n))
    # Reiniciar el modo de pesos al estado inicial
    st.session_state.modo_pesos_radio = "Usar pesos recomendados"
    if 'modo_pesos_guardado' in st.session_state:
        del st.session_state.modo_pesos_guardado

from streamlit_echarts import st_echarts

from streamlit_echarts import st_echarts

def radar_chart(metricas, titulo, key):
    etiquetas = {
        'CE': 'Cons. Energía', 
        'HC': 'Huella CO₂', 
        'EW': 'E-waste',
        'ER': 'Energía Renov.', 
        'EE': 'Eficiencia', 
        'DP': 'Durabilidad',
        'RC': 'Reciclabilidad', 
        'IM': 'Mantenimiento'
    }
    
    labels = [etiquetas[m] for m in metricas.keys()]
    valores = list(metricas.values())

    options = {
        "backgroundColor": "#111111",
        "title": {
            "text": titulo,
            "left": "center",
            "top": "5%",
            "textStyle": {
                "color": "#ffffff",
                "fontSize": 20,
            },
        },
        "tooltip": {
            "trigger": "item"
        },
        "radar": {
            "indicator": [{"name": label, "max": 10} for label in labels],
            "radius": "60%",
            "center": ["50%", "55%"],
            "splitNumber": 5,
            "axisLine": {
                "lineStyle": {"color": "#3498db"}
            },
            "splitLine": {
                "lineStyle": {"color": "#444444"},
                "show": True
            },
            "splitArea": {
                "areaStyle": {"color": ["#2e2e3e", "#1e1e2f"]}
            }
        },
        "series": [
            {
                "name": titulo,
                "type": "radar",
                "data": [
                    {
                        "value": valores,
                        "name": titulo,
                        "itemStyle": {
                            "color": "#3498db"
                        },
                        "lineStyle": {
                            "color": "#3498db"
                        },
                        "areaStyle": {
                            "color": "#3498db",
                            "opacity": 0.3
                        }
                    }
                ]
            }
        ]
    }

    # Renderizar con ECharts usando el key único
    st_echarts(options=options, height="500px", key=key)


def calcular_pesos_ahp(metricas):
    df_criterios = pd.DataFrame(
        st.session_state.matriz_comparacion,
        index=metricas,
        columns=metricas
    )
    pesos = ahp_attributes(df_criterios)
    ic, rc = razon_consistencia(pesos, df_criterios, verbose=False)
    return pesos, ic, rc

def mostrar_resultados_ahp(pesos, rc):
    """Muestra los resultados del cálculo AHP."""
    st.success("Pesos calculados:")
    # Convertir los pesos a un formato limpio
    pesos_limpios = {}
    for k, v in pesos.items():
        if isinstance(v, dict):
            val = list(v.values())[0]
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
    st.dataframe(df_pesos.style.format({'Peso': '{:.3f}'}), use_container_width=True)
    
    if rc < 0.1:
        st.success(f"Razón de Consistencia: {rc:.3f} (La matriz es consistente)")
    else:
        st.warning(f"Razón de Consistencia: {rc:.3f} (La matriz NO es consistente)")

def mostrar_matriz_ahp():
    st.title("Matriz de Comparación por Pares (AHP)")
    st.info("Edita solo la mitad superior de la tabla. El resto se calcula automáticamente.")
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
            st.rerun()  # Forzar recarga para mostrar solo una vez
    with col_save:
        if st.button("Guardar y salir"):
            if 'ahp_resultados' in st.session_state:
                pesos = st.session_state.ahp_resultados['pesos']
                if hasattr(pesos, 'to_dict'):
                    pesos = pesos.to_dict()
                st.session_state.pesos_ahp = pesos
            st.session_state.matriz_ahp_abierta = False
            if 'modo_pesos_guardado' in st.session_state:
                st.session_state.modo_pesos_radio = st.session_state.modo_pesos_guardado
            st.rerun()
    with col_cancel:
        if st.button("Cancelar"):
            st.session_state.matriz_ahp_abierta = False
            if 'modo_pesos_guardado' in st.session_state:
                st.session_state.modo_pesos_radio = st.session_state.modo_pesos_guardado
            st.rerun()
    with col_reset:
        if st.button("Reiniciar matriz", help="Reinicia la matriz de comparación a valores iniciales (identidad)", key="btn_reiniciar_matriz"):
            st.session_state.matriz_comparacion = np.ones((n, n))
            st.warning("¡La matriz de comparación ha sido reiniciada a valores iniciales!")
            if 'ahp_resultados' in st.session_state:
                del st.session_state.ahp_resultados
            st.rerun()

    # Mostrar resultados si existen
    if st.session_state.get('ahp_resultados'):
        mostrar_resultados_ahp(st.session_state.ahp_resultados['pesos'], st.session_state.ahp_resultados['rc'])
    st.stop()

# --- INICIALIZACIÓN DE LA APLICACIÓN ---
st.set_page_config(page_title="Dashboard Sostenibilidad IoT", layout="wide")
inicializar_estado()

# --- CONTROL DE NAVEGACIÓN ---
if st.session_state.matriz_ahp_abierta:
    mostrar_matriz_ahp()
    st.stop()

# --- INTERFAZ PRINCIPAL ---
st.title("Dashboard de Evaluación de Sostenibilidad - Dispositivos IoT")

# Botón para reiniciar
if st.button("Reiniciar"):
    reiniciar_estado()
    st.rerun()

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
    st.subheader("Ajuste de Pesos por Métrica")

    modo_pesos = st.radio(
        "Selecciona el modo de ajuste de pesos:",
        ("Usar pesos recomendados", "Ajustar pesos manualmente", "Calcular nuevos pesos"),
        key="modo_pesos_radio"
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
                inicializar_pesos_manuales()
                st.rerun()

        pesos_usuario = {}
        total_temporal = 0

        for id, nombre_metrica in NOMBRES_METRICAS.items():
            valor = st.number_input(
                f"{nombre_metrica}",
                min_value=0.0,
                max_value=1.0,
                step=0.01,
                format="%.3f",
                value=float(st.session_state[f"peso_manual_{id}"]),
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

    elif modo_pesos == "Calcular nuevos pesos":
        if st.button("Editar matriz de comparación por pares"):
            st.session_state.modo_pesos_guardado = st.session_state.modo_pesos_radio
            st.session_state.matriz_ahp_abierta = True
            st.rerun()
        # Mostrar la tabla de pesos calculados si existen
        if 'pesos_ahp' in st.session_state and bool(st.session_state.pesos_ahp):
            st.success("Pesos calculados:")
            pesos_dict = st.session_state.pesos_ahp
            pesos_limpios = {}
            for k, v in pesos_dict.items():
                if isinstance(v, dict):
                    val = list(v.values())[0]
                else:
                    val = v
                pesos_limpios[k] = float(val)
            metricas_list = list(pesos_limpios.keys())
            pesos_list = [pesos_limpios[k] for k in metricas_list]
            nombres_list = [NOMBRES_METRICAS[k] for k in metricas_list]
            df_pesos = pd.DataFrame({
                'Métrica': nombres_list,
                'Peso': pesos_list
            })
            st.dataframe(df_pesos.style.format({'Peso': '{:.3f}'}), use_container_width=True)

if submitted:
    # Guardar los datos del dispositivo sin hacer cálculos ni mostrar gráficos
    dispositivo_data = {
        "nombre": nombre,
        "potencia": potencia,
        "horas": horas,
        "dias": dias,
        "peso": peso,
        "vida": vida,
        "energia_renovable": energia_renovable,
        "funcionalidad": funcionalidad,
        "reciclabilidad": reciclabilidad,
        "B": B,
        "Wb": Wb,
        "M": M,
        "C": C,
        "Wc": Wc,
        "W0": W0,
        "W": W,
        "calculo_realizado": False  # Control individual de cálculo
    }

    # Agregar el dispositivo sin mostrar resultados
    st.session_state.dispositivos.append(dispositivo_data)

    # Mostrar mensaje de confirmación sin resultados
    st.success(f"Dispositivo '{nombre}' añadido correctamente. Presiona 'Calcular Índice de Sostenibilidad Total' para ver los resultados.")

# --- BOTÓN DE REFRESH ---
if st.button("Calcular Indice de Sostenibilidad"):
    if not st.session_state.dispositivos:
        st.warning("No hay dispositivos añadidos.")
    else:
        total_indices = []
        metricas_totales = []

        for idx, dispositivo in enumerate(st.session_state.dispositivos):
            # Solo recalcular si no se ha calculado previamente
            if not dispositivo.get("calculo_realizado", False):
                sensor = SostenibilidadIoT(dispositivo["nombre"])

                # Obtener los pesos
                pesos_usuario = st.session_state.pesos_ahp if "pesos_ahp" in st.session_state else obtener_pesos_recomendados()
                sensor.pesos = {k: float(v) for k, v in pesos_usuario.items()}

                # Calcular métricas
                sensor.calcular_consumo_energia(dispositivo["potencia"], dispositivo["horas"], dispositivo["dias"])
                sensor.calcular_huella_carbono()
                sensor.calcular_ewaste(dispositivo["peso"], dispositivo["vida"])
                sensor.calcular_energia_renovable(dispositivo["energia_renovable"])
                sensor.calcular_eficiencia_energetica(dispositivo["funcionalidad"])
                sensor.calcular_durabilidad(dispositivo["vida"])
                sensor.calcular_reciclabilidad(dispositivo["reciclabilidad"])
                sensor.calcular_indice_mantenimiento(
                    dispositivo["B"], dispositivo["Wb"], dispositivo["M"], 
                    dispositivo["C"], dispositivo["Wc"], dispositivo["W0"], dispositivo["W"]
                )

                # Calcular el índice de sostenibilidad
                resultado = sensor.calcular_sostenibilidad()
                dispositivo["resultado"] = resultado
                dispositivo["calculo_realizado"] = True

            # Actualizar listas para el cálculo global
            total_indices.append(dispositivo["resultado"]["indice_sostenibilidad"])
            metricas_totales.append(dispositivo["resultado"]["metricas_normalizadas"])

        # Cálculo del índice global
        promedio_total = sum(total_indices) / len(total_indices)

        # Calcular promedio de métricas
        promedio_metricas = {
            key: sum(m[key] for m in metricas_totales) / len(metricas_totales)
            for key in metricas_totales[0]
        }

        # Guardar el resultado global
        st.session_state.resultado_global = {
            "promedio_total": promedio_total,
            "promedio_metricas": promedio_metricas
        }

        st.success("Resultados actualizados correctamente.")

# --- FUNCIÓN PARA MOSTRAR RESULTADOS DE UN DISPOSITIVO ---
def mostrar_dispositivo(dispositivo, idx):
    """Muestra el gráfico y las recomendaciones del dispositivo."""
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

# --- MOSTRAR RESULTADOS INDIVIDUALES ---
if st.session_state.dispositivos:
    st.markdown("---")
    st.subheader("Resultados por Dispositivo")

    dispositivos = st.session_state.dispositivos
    num_dispositivos = len(dispositivos)

    for i in range(0, num_dispositivos, 2):
        col1, col2 = st.columns(2)

        # Mostrar dispositivo en la primera columna
        with col1:
            mostrar_dispositivo(dispositivos[i], i)

        # Mostrar dispositivo en la segunda columna, si existe
        if i + 1 < num_dispositivos:
            with col2:
                mostrar_dispositivo(dispositivos[i + 1], i + 1)

# --- MOSTRAR RESULTADOS GLOBALES ---
if "resultado_global" in st.session_state:
    resultado_global = st.session_state.resultado_global
    promedio_total = resultado_global["promedio_total"]
    promedio_metricas = resultado_global["promedio_metricas"]

    st.markdown("---")
    st.success(f"Índice de Sostenibilidad Global: {promedio_total:.2f}/10")

    col1, col2 = st.columns([2, 1])

    # Gráfico del promedio a la izquierda
    with col1:
        radar_chart(promedio_metricas, "Promedio de Métricas Normalizadas", key="radar_total")

    # Recomendaciones globales a la derecha
    with col2:
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
