import streamlit as st
import uuid
from utils.constants import FORM_KEYS, METRIC_NAMES
from model import IoTSustainability
from weights import get_recommended_weights, validate_manual_weights
from utils.helpers import to_dict_flat, create_weights_snapshot

def initialize_form():
    """Initializes form state variables."""
    for k, (default, _) in FORM_KEYS.items():
        if f"form_{k}" not in st.session_state:
            st.session_state[f"form_{k}"] = default

def show_device_form():
    """Shows the form for entering IoT device data."""
    submitted = False
    with st.form("formulario_datos"):
        st.subheader("Datos del dispositivo IoT")
        colA, colB = st.columns(2)
        
        # First form column
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

        # Second form column
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

        # Maintenance section
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

def process_form(form_data):
    """Processes form data and updates application state."""
    # Delete only global results and date, NOT AHP weights
    for var in ["global_result", "global_calculation_date"]:
        if var in st.session_state:
            del st.session_state[var]

    # Determine active weights and configuration name at this moment
    if st.session_state.weight_mode_radio == "Calcular nuevos pesos":
        if 'ahp_weights' in st.session_state:
            user_weights = st.session_state.ahp_weights
            # Find active calculated configuration name
            weights_config_name = "Pesos Calculados"
            for ahp_config_name, config in st.session_state.ahp_configurations.items():
                if to_dict_flat(config['weights']) == to_dict_flat(user_weights):
                    weights_config_name = f"Configuración Calculada: {ahp_config_name}"
                    break
        else:
            st.warning("No hay pesos AHP calculados. Se usarán los pesos recomendados.")
            user_weights = get_recommended_weights()
            weights_config_name = "Pesos Recomendados"
    elif st.session_state.weight_mode_radio == "Ajuste Manual":
        manual_weights = {k: st.session_state[f"manual_weight_{k}"] for k in METRIC_NAMES}
        user_weights, _ = validate_manual_weights(manual_weights)
        # Find active manual configuration name
        weights_config_name = "Pesos Manuales Personalizados"
        for manual_config_name, config in st.session_state.saved_weights.items():
            if to_dict_flat(config) == to_dict_flat(user_weights):
                weights_config_name = f"Configuración Manual: {manual_config_name}"
                break
    else:
        user_weights = get_recommended_weights()
        weights_config_name = "Pesos Recomendados"

    # Create device with form data
    device = {
        "nombre": form_data["nombre"],
        "potencia": form_data["potencia"],
        "horas": form_data["horas"],
        "dias": form_data["dias"],
        "peso": form_data["peso"],
        "vida": form_data["vida"],
        "energia_renovable": form_data["energia_renovable"],
        "funcionalidad": form_data["funcionalidad"],
        "reciclabilidad": form_data["reciclabilidad"],
        "B": form_data["B"],
        "Wb": form_data["Wb"],
        "M": form_data["M"],
        "C": form_data["C"],
        "Wc": form_data["Wc"],
        "W0": form_data["W0"],
        "W": form_data["W"],
        "used_weights": user_weights,
        "configuration_name": weights_config_name
    }

    # Add device to the list
    st.session_state.devices.append(device)

    # Clear form
    for key in FORM_KEYS:
        st.session_state[f"form_{key}"] = 0.0

    # Calculate sustainability index using these weights
    sensor = IoTSustainability(form_data['nombre'])
    clean_weights = {}
    for k, v in user_weights.items():
        if isinstance(v, dict):
            v = list(v.values())[0]
        try:
            clean_weights[k] = float(v)
        except Exception:
            continue
    sensor.pesos = clean_weights
    sensor.calculate_energy_consumption(form_data['potencia'], form_data['horas'], form_data['dias'])
    sensor.calculate_carbon_footprint()
    sensor.calculate_ewaste(form_data['peso'], form_data['vida'])
    sensor.calculate_renewable_energy(form_data['energia_renovable'])
    sensor.calculate_energy_efficiency(form_data['funcionalidad'])
    sensor.calculate_durability(form_data['vida'])
    sensor.calculate_recyclability(form_data['reciclabilidad'])
    sensor.calculate_maintenance_index(
        form_data['B'], form_data['Wb'], form_data['M'],
        form_data['C'], form_data['Wc'], form_data['W0'], form_data['W']
    )
    result = sensor.calculate_sustainability()

    device_data = {
        "id": str(uuid.uuid4()),
        **form_data,
        "calculo_realizado": True,
        "used_weights": user_weights,
        "resultado": result,
        # Save form and weights snapshot
        "snapshot_form": {k: st.session_state[f"form_{k}"] for k in FORM_KEYS},
        "weights_snapshot": create_weights_snapshot(user_weights, st.session_state.weight_mode_radio)
    }

    st.session_state.devices.append(device_data)
    st.success(f"Dispositivo '{form_data['nombre']}' añadido correctamente. Presiona 'Calcular Índice de Sostenibilidad Total' para ver los resultados.")
    st.rerun() 