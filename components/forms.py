import streamlit as st
import uuid
from utils.constants import FORM_KEYS, METRIC_NAMES, RECOMMENDED_WEIGHTS
from model import IoTSustainability
from weights import validate_manual_weights
from utils.helpers import to_dict_flat, create_weights_snapshot

def initialize_form():
    """Initializes form state variables."""
    for k, (default, _) in FORM_KEYS.items():
        if f"form_{k}" not in st.session_state:
            st.session_state[f"form_{k}"] = default

def show_device_form():
    """Shows the form for entering IoT device data."""
    submitted = False
    with st.form("form_data"):
        st.subheader("Datos del dispositivo IoT")
        colA, colB = st.columns(2)
        
        # First form column
        with colA:
            name = st.text_input(
                "Nombre del dispositivo", 
                value=st.session_state["form_name"], 
                help="Nombre descriptivo del dispositivo IoT."
            )
            power = st.number_input(
                "Potencia (W)", 
                value=st.session_state["form_power"], 
                help="Potencia eléctrica en vatios (W) del dispositivo cuando está en funcionamiento."
            )
            hours = st.number_input(
                "Horas uso diario", 
                value=st.session_state["form_hours"], 
                help="Cantidad de horas al día que el dispositivo está en uso."
            )
            days = st.number_input(
                "Días uso/año", 
                value=st.session_state["form_days"], 
                help="Número de días al año que el dispositivo opera."
            )
            weight = st.number_input(
                "Peso dispositivo (kg)", 
                value=st.session_state["form_weight"], 
                help="Peso total del dispositivo en kilogramos."
            )
            life = st.number_input(
                "Vida útil (años)", 
                value=st.session_state["form_life"], 
                help="Duración esperada del dispositivo antes de desecharse o reemplazarse."
            )

        # Second form column
        with colB:
            renewable_energy = st.slider(
                "Energía renovable (%)", 
                0, 100, 
                st.session_state["form_renewable_energy"], 
                help="Porcentaje de energía que proviene de fuentes renovables."
            )
            functionality = st.slider(
                "Funcionalidad (1-10)", 
                1, 10, 
                st.session_state["form_functionality"], 
                help="Nivel de funcionalidad y utilidad que ofrece el dispositivo."
            )
            recyclability = st.slider(
                "Reciclabilidad (%)", 
                0, 100, 
                st.session_state["form_recyclability"], 
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
    'name': name,
    'power': power,
    'daily_hours': hours,
    'annual_days': days,
    'weight': weight,
    'lifespan': life,
    'renewable_energy': renewable_energy,
    'functionality': functionality,
    'recyclability': recyclability,
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
            for config in st.session_state.ahp_configurations.items():
                if to_dict_flat(config['weights']) == to_dict_flat(user_weights):
                    break
        else:
            st.warning("No hay pesos AHP calculados. Se usarán los pesos recomendados.")
            user_weights = RECOMMENDED_WEIGHTS

    elif st.session_state.weight_mode_radio == "Ajuste Manual":
        manual_weights = {k: st.session_state[f"manual_weight_{k}"] for k in METRIC_NAMES}
        user_weights, _ = validate_manual_weights(manual_weights)
        # Find active manual configuration name
        for config in st.session_state.saved_weights.items():
            if to_dict_flat(config) == to_dict_flat(user_weights):
                break
    else:
        user_weights = RECOMMENDED_WEIGHTS

    # Calculate sustainability index using these weights
    sensor = IoTSustainability(form_data['name'])
    clean_weights = {}
    for k, v in user_weights.items():
        if isinstance(v, dict):
            v = list(v.values())[0]
        try:
            clean_weights[k] = float(v)
        except Exception:
            continue
    sensor.weights = clean_weights
    sensor.calculate_energy_consumption(form_data['power'], form_data['hours'], form_data['days'])
    sensor.calculate_carbon_footprint()
    sensor.calculate_ewaste(form_data['weight'], form_data['life'])
    sensor.calculate_renewable_energy(form_data['renewable_energy'])
    sensor.calculate_energy_efficiency(form_data['functionality'])
    sensor.calculate_durability(form_data['life'])
    sensor.calculate_recyclability(form_data['recyclability'])
    sensor.calculate_maintenance_index(
        form_data['B'], form_data['Wb'], form_data['M'],
        form_data['C'], form_data['Wc'], form_data['W0'], form_data['W']
    )
    result = sensor.calculate_sustainability()

    device_data = {
        "id": str(uuid.uuid4()),
        **form_data,
        "calculation_done": True,
        "used_weights": user_weights,
        "result": result,
        # Save form and weights snapshot
        "snapshot_form": {k: st.session_state[f"form_{k}"] for k in FORM_KEYS},
        "weights_snapshot": create_weights_snapshot(user_weights, st.session_state.weight_mode_radio)
    }

    st.session_state.devices.append(device_data)
    st.success(f"Dispositivo '{form_data['name']}' añadido correctamente. Presiona 'Calcular Índice de Sostenibilidad Total' para ver los resultados.")
    st.rerun() 