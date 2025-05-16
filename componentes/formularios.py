import streamlit as st
import uuid
from utilidades.constantes import FORM_KEYS, NOMBRES_METRICAS
from modelo import SostenibilidadIoT
from pesos import obtener_pesos_recomendados, validar_pesos_manuales
from utilidades.auxiliares import to_dict_flat

def inicializar_formulario():
    """Inicializa los valores del formulario en el session_state si no existen."""
    for k, (default, _) in FORM_KEYS.items():
        if f"form_{k}" not in st.session_state:
            st.session_state[f"form_{k}"] = default

def mostrar_formulario_dispositivo():
    """Muestra el formulario para ingresar datos de un dispositivo IoT."""
    submitted = False
    with st.form("formulario_datos"):
        st.subheader("Datos del dispositivo IoT")
        colA, colB = st.columns(2)
        
        # Primera columna del formulario
        with colA:
            nombre = st.text_input(
                "Nombre del dispositivo", 
                value=st.session_state["form_nombre"], 
                help="Nombre descriptivo del dispositivo IoT."
            )
            potencia = st.number_input(
                "Potencia (W)", 
                value=st.session_state["form_potencia"], 
                help="Potencia eléctrica en vatios (W) del dispositivo cuando está en funcionamiento."
            )
            horas = st.number_input(
                "Horas uso diario", 
                value=st.session_state["form_horas"], 
                help="Cantidad de horas al día que el dispositivo está en uso."
            )
            dias = st.number_input(
                "Días uso/año", 
                value=st.session_state["form_dias"], 
                help="Número de días al año que el dispositivo opera."
            )
            peso = st.number_input(
                "Peso dispositivo (kg)", 
                value=st.session_state["form_peso"], 
                help="Peso total del dispositivo en kilogramos."
            )
            vida = st.number_input(
                "Vida útil (años)", 
                value=st.session_state["form_vida"], 
                help="Duración esperada del dispositivo antes de desecharse o reemplazarse."
            )

        # Segunda columna del formulario
        with colB:
            energia_renovable = st.slider(
                "Energía renovable (%)", 
                0, 100, 
                st.session_state["form_energia_renovable"], 
                help="Porcentaje de energía que proviene de fuentes renovables."
            )
            funcionalidad = st.slider(
                "Funcionalidad (1-10)", 
                1, 10, 
                st.session_state["form_funcionalidad"], 
                help="Nivel de funcionalidad y utilidad que ofrece el dispositivo."
            )
            reciclabilidad = st.slider(
                "Reciclabilidad (%)", 
                0, 100, 
                st.session_state["form_reciclabilidad"], 
                help="Porcentaje del dispositivo que puede reciclarse al finalizar su vida útil."
            )

        # Sección de mantenimiento
        with st.expander("Datos de mantenimiento"):
            colM1, colM2 = st.columns(2)
            with colM1:
                B = st.number_input(
                    "Baterías vida útil", 
                    value=st.session_state["form_B"], 
                    help="Cantidad de baterías necesarias durante toda la vida útil del dispositivo."
                )
                Wb = st.number_input(
                    "Peso batería (g)", 
                    value=st.session_state["form_Wb"], 
                    help="Peso de cada batería en gramos."
                )
                M = st.number_input(
                    "Mantenimientos", 
                    value=st.session_state["form_M"], 
                    help="Número de veces que el dispositivo requiere mantenimiento."
                )
                C = st.number_input(
                    "Componentes reemplazados", 
                    value=st.session_state["form_C"], 
                    help="Número de componentes reemplazados en mantenimientos."
                )

            with colM2:
                Wc = st.number_input(
                    "Peso componente (g)", 
                    value=st.session_state["form_Wc"], 
                    help="Peso promedio de cada componente reemplazado en gramos."
                )
                W0 = st.number_input(
                    "Peso nuevo (g)", 
                    value=st.session_state["form_W0"], 
                    help="Peso total del dispositivo cuando es nuevo."
                )
                W = st.number_input(
                    "Peso final (g)", 
                    value=st.session_state["form_W"], 
                    help="Peso final del dispositivo después del uso."
                )

        submitted = st.form_submit_button("Añadir dispositivo")

    return submitted, {
        'nombre': nombre,
        'potencia': potencia,
        'horas': horas,
        'dias': dias,
        'peso': peso,
        'vida': vida,
        'energia_renovable': energia_renovable,
        'funcionalidad': funcionalidad,
        'reciclabilidad': reciclabilidad,
        'B': B,
        'Wb': Wb,
        'M': M,
        'C': C,
        'Wc': Wc,
        'W0': W0,
        'W': W
    }

def procesar_formulario(datos_formulario):
    """Procesa los datos del formulario y actualiza el estado de la aplicación."""
    # Eliminar solo los resultados globales y la fecha, NO los pesos AHP
    for var in ["resultado_global", "fecha_calculo_global"]:
        if var in st.session_state:
            del st.session_state[var]

    # Determinar los pesos activos y el nombre de la configuración en este momento
    if st.session_state.modo_pesos_radio == "Calcular nuevos pesos":
        if 'pesos_ahp' in st.session_state:
            pesos_usuario = st.session_state.pesos_ahp
            # Buscar nombre de la configuración calculada activa
            nombre_config_pesos = "Pesos Calculados"
            for nombre_config_ahp, config in st.session_state.configuraciones_ahp.items():
                if to_dict_flat(config['pesos']) == to_dict_flat(pesos_usuario):
                    nombre_config_pesos = f"Configuración Calculada: {nombre_config_ahp}"
                    break
        else:
            st.warning("No hay pesos AHP calculados. Se usarán los pesos recomendados.")
            pesos_usuario = obtener_pesos_recomendados()
            nombre_config_pesos = "Pesos Recomendados"
    elif st.session_state.modo_pesos_radio == "Ajuste Manual":
        pesos_manuales = {k: st.session_state[f"peso_manual_{k}"] for k in NOMBRES_METRICAS}
        pesos_usuario, _ = validar_pesos_manuales(pesos_manuales)
        # Buscar nombre de la configuración manual activa
        nombre_config_pesos = "Pesos Manuales Personalizados"
        for nombre_config_manual, config in st.session_state.pesos_guardados.items():
            if to_dict_flat(config) == to_dict_flat(pesos_usuario):
                nombre_config_pesos = f"Configuración Manual: {nombre_config_manual}"
                break
    else:
        pesos_usuario = obtener_pesos_recomendados()
        nombre_config_pesos = "Pesos Recomendados"

    # Calcular el índice de sostenibilidad usando estos pesos
    sensor = SostenibilidadIoT(datos_formulario['nombre'])
    pesos_limpios = {}
    for k, v in pesos_usuario.items():
        if isinstance(v, dict):
            v = list(v.values())[0]
        try:
            pesos_limpios[k] = float(v)
        except Exception:
            continue
    sensor.pesos = pesos_limpios
    sensor.calcular_consumo_energia(datos_formulario['potencia'], datos_formulario['horas'], datos_formulario['dias'])
    sensor.calcular_huella_carbono()
    sensor.calcular_ewaste(datos_formulario['peso'], datos_formulario['vida'])
    sensor.calcular_energia_renovable(datos_formulario['energia_renovable'])
    sensor.calcular_eficiencia_energetica(datos_formulario['funcionalidad'])
    sensor.calcular_durabilidad(datos_formulario['vida'])
    sensor.calcular_reciclabilidad(datos_formulario['reciclabilidad'])
    sensor.calcular_indice_mantenimiento(
        datos_formulario['B'], datos_formulario['Wb'], datos_formulario['M'],
        datos_formulario['C'], datos_formulario['Wc'], datos_formulario['W0'], datos_formulario['W']
    )
    resultado = sensor.calcular_sostenibilidad()

    dispositivo_data = {
        "id": str(uuid.uuid4()),
        **datos_formulario,
        "calculo_realizado": True,
        "pesos_utilizados": pesos_usuario,
        "resultado": resultado,
        # Guardar snapshot del formulario y pesos
        "snapshot_form": {k: st.session_state[f"form_{k}"] for k in FORM_KEYS},
        "snapshot_pesos": {
            "modo": st.session_state.modo_pesos_radio,
            "nombre_configuracion": nombre_config_pesos,
            "pesos_manuales": st.session_state.get("pesos_manuales", {}),
            "pesos_ahp": st.session_state.get("pesos_ahp", {})
        }
    }

    st.session_state.dispositivos.append(dispositivo_data)
    st.success(f"Dispositivo '{datos_formulario['nombre']}' añadido correctamente. Presiona 'Calcular Índice de Sostenibilidad Total' para ver los resultados.")
    st.rerun() 