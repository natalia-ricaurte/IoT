# Standard libraries
import uuid
from datetime import datetime

# Third-party libraries
import streamlit as st

# Local modules
from utils.constants import METRIC_NAMES, FORM_KEYS, DASHBOARD_GUIDE
from utils.helpers import create_weights_snapshot, to_dict_flat, extract_weight_value
from utils.state import initialize_state, reset_state
from components.devices import show_device, show_global_results
from components.forms import initialize_form
from components.weights_ui import show_weights_interface
from services.ahp_service import show_ahp_matrix
from services.export import export_results_excel, export_devices_list
from services.import_service import generate_excel_template, read_devices_file, generate_json_template
from weights import get_recommended_weights, validate_manual_weights
from model import IoTSustainability

# --- APPLICATION INITIALIZATION ---
st.set_page_config(page_title="Dashboard Sostenibilidad IoT", page_icon="🌱", layout="wide")

# Initialize state
initialize_state()
initialize_form()

# Initialize device selection state
if 'selected_devices' not in st.session_state:
    st.session_state.selected_devices = {}

def update_device_selection():
    """Updates the device selection state."""
    if 'selected_devices' not in st.session_state:
        st.session_state.selected_devices = {}
    
    # Keep only selections for devices that still exist
    current_devices = {device['id']: device for device in st.session_state.devices}
    st.session_state.selected_devices = {
        id: selected 
        for id, selected in st.session_state.selected_devices.items()
        if id in current_devices
    }
    
    # Add new devices as selected by default
    for id in current_devices:
        if id not in st.session_state.selected_devices:
            st.session_state.selected_devices[id] = True
    
    # Remove global results if they exist
    if 'global_result' in st.session_state:
        del st.session_state.global_result

def get_selected_devices():
    """Returns the list of currently selected devices."""
    return [
        d for d in st.session_state.devices
        if st.session_state.selected_devices.get(d['id'], True)
    ]

# --- NAVIGATION CONTROL ---
if st.session_state.ahp_matrix_open:
    show_ahp_matrix()
    st.stop()

# --- MAIN INTERFACE ---
st.title("Dashboard de Evaluación de Sostenibilidad - Dispositivos IoT")

# Reset button
if st.button("Reiniciar"):
    reset_state()
    if 'imported_devices' in st.session_state:
        del st.session_state['imported_devices']
    if 'import_csv' in st.session_state:
        del st.session_state['import_csv']
    if 'show_import' in st.session_state:
        st.session_state['show_import'] = False
    if 'selected_devices' in st.session_state:
        del st.session_state['selected_devices']
    st.rerun()

st.markdown("## Descripción de Métricas y Guía de Uso")
with st.expander("Ver detalles y guía de uso"):
    st.markdown(DASHBOARD_GUIDE)

st.markdown('---')

# --- DEVICE IMPORT SECTION ---
st.markdown("## Importar lista de dispositivos")
import_container = st.container()
with import_container:
    if 'show_import' not in st.session_state:
        st.session_state.show_import = False
    
    # --- Restore manual weights if needed before creating widgets ---
    if 'restore_manual_weights' in st.session_state and st.session_state['restore_manual_weights']:
        current_weight_mode = st.session_state.get('weight_mode_radio')
        current_ahp_weights = st.session_state.get('ahp_weights')
        current_manual_weights = st.session_state.get('manual_weights', {})
        individual_manual_weights = st.session_state.get('individual_manual_weights', {})
        st.session_state.weight_mode_radio = current_weight_mode
        if current_ahp_weights:
            st.session_state.ahp_weights = current_ahp_weights
        if current_manual_weights:
            st.session_state.manual_weights = current_manual_weights
        if current_weight_mode == "Ajuste Manual":
            for k, v in individual_manual_weights.items():
                st.session_state[f"manual_weight_{k}"] = v
        st.session_state['restore_manual_weights'] = False
    
    if st.button("Importar lista de dispositivos"):
        # Save current weight state before changing show_import
        current_weight_mode = st.session_state.get('weight_mode_radio')
        current_ahp_weights = st.session_state.get('ahp_weights')
        current_manual_weights = st.session_state.get('manual_weights', {})
        individual_manual_weights = {}
        if current_weight_mode == "Ajuste Manual":
            for k in METRIC_NAMES:
                individual_manual_weights[k] = st.session_state.get(f"manual_weight_{k}")
        st.session_state['show_import'] = True
        # Save to restore in next cycle
        st.session_state['restore_manual_weights'] = True
        st.session_state['individual_manual_weights'] = individual_manual_weights
        st.session_state['weight_mode_radio'] = current_weight_mode
        st.session_state['ahp_weights'] = current_ahp_weights
        st.session_state['manual_weights'] = current_manual_weights
        st.rerun()
    
    # --- Template download buttons in an expander ---
    with st.expander("Descargar plantillas de importación"):
        buffer = generate_excel_template()
        st.download_button(
            label="Descargar plantilla Excel (.xlsx)",
            data=buffer,
            file_name="plantilla_dispositivos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        buffer_json = generate_json_template()
        st.download_button(
            label="Descargar plantilla JSON",
            data=buffer_json,
            file_name="plantilla_dispositivos.json",
            mime="application/json"
        )
    st.caption("Recuerda: no cambies los nombres de las columnas (Excel) o claves (JSON) en las plantillas. Deben coincidir exactamente para que la importación funcione.")

    # Show uploader only if show_import is True
    if st.session_state.show_import:
        st.info("Sube un archivo CSV, Excel o JSON con la lista de dispositivos a importar. Descarga la plantilla para ver el formato requerido.")
        if st.button("Cancelar importación", key="cancel_import"):
            # Save current weight state before canceling
            current_weight_mode = st.session_state.get('weight_mode_radio')
            current_ahp_weights = st.session_state.get('ahp_weights')
            current_manual_weights = st.session_state.get('manual_weights', {})
            individual_manual_weights = {}
            if current_weight_mode == "Ajuste Manual":
                for k in METRIC_NAMES:
                    individual_manual_weights[k] = st.session_state.get(f"manual_weight_{k}")
            # Save to restore in next cycle
            st.session_state['restore_manual_weights'] = True
            st.session_state['individual_manual_weights'] = individual_manual_weights
            st.session_state['weight_mode_radio'] = current_weight_mode
            st.session_state['ahp_weights'] = current_ahp_weights
            st.session_state['manual_weights'] = current_manual_weights
            st.session_state.show_import = False
            st.session_state['imported_devices'] = []
            if 'import_message' in st.session_state:
                del st.session_state['import_message']
            st.rerun()
        import_file = st.file_uploader("Selecciona el archivo", type=["csv", "xlsx", "json"], key="import_csv")
        if import_file is not None:
            try:
                import_df = read_devices_file(import_file)
                if len(import_df) > 0:
                    imported = import_df.to_dict(orient='records')
                    for d in imported:
                        d['_import_hash'] = str(uuid.uuid4())
                    st.session_state['imported_devices'] = imported
                    if 'import_csv' in st.session_state:
                        del st.session_state['import_csv']
                    st.session_state['show_import'] = False
                    st.session_state['import_message'] = f"✅ Archivo '{import_file.name}' leído correctamente. Se encontraron {len(import_df)} dispositivos.\n\nAhora puedes añadirlos individualmente o todos al sistema usando los botones correspondientes."

                    # --- SAVE AND RESTORE WEIGHT STATE ---
                    current_weight_mode = st.session_state.get('weight_mode_radio')
                    current_ahp_weights = st.session_state.get('ahp_weights')
                    current_manual_weights = st.session_state.get('manual_weights', {})
                    individual_manual_weights = {}
                    if current_weight_mode == "Ajuste Manual":
                        for k in METRIC_NAMES:
                            individual_manual_weights[k] = st.session_state.get(f"manual_weight_{k}")
                    # Restore
                    st.session_state.weight_mode_radio = current_weight_mode
                    if current_ahp_weights:
                        st.session_state.ahp_weights = current_ahp_weights
                    if current_manual_weights:
                        st.session_state.manual_weights = current_manual_weights
                    if current_weight_mode == "Ajuste Manual":
                        for k, v in individual_manual_weights.items():
                            st.session_state[f"manual_weight_{k}"] = v
                    # --- END RESTORE WEIGHT STATE ---

                    st.rerun()
                else:
                    st.session_state['imported_devices'] = []
                    st.warning("⚠️ El archivo está vacío. No se encontraron dispositivos para importar.")
            except Exception as e:
                st.session_state['imported_devices'] = []
                print(f"Error al leer el archivo: {str(e)}")
                st.error(f"❌ Error al leer el archivo: {str(e)}")

    # Show imported devices list even if show_import is False
    if 'imported_devices' in st.session_state and st.session_state['imported_devices']:
        st.markdown('---')
        # Show import success message if it exists
        if 'import_message' in st.session_state:
            st.success(st.session_state['import_message'])
        st.markdown("""
        ### Dispositivos importados pendientes de añadir
        Revisa los datos principales de cada dispositivo. Puedes ver los detalles completos haciendo clic en \"Ver detalles\". Selecciona los pesos antes de añadir cada dispositivo al sistema.
        """)
        for idx, device in enumerate(st.session_state['imported_devices']):
            with st.container():
                col1, col2, col3 = st.columns([5, 1, 1])
                name = device.get('nombre', 'Sin nombre')
                power = device.get('potencia', 'N/A')
                life = device.get('vida', 'N/A')
                col1.markdown(f"**{name}** | Potencia: {power} W | Vida útil: {life} años")
                key_exp = f"expand_imported_{idx}"
                if key_exp not in st.session_state:
                    st.session_state[key_exp] = False
                if col2.button("Ver detalles" if not st.session_state[key_exp] else "Ocultar detalles", key=f"btn_details_import_{idx}"):
                    st.session_state[key_exp] = not st.session_state[key_exp]
                    st.rerun()
                if col3.button("Añadir dispositivo al sistema", key=f"btn_add_import_{idx}"):
                    # Save current weight state
                    current_weight_mode = st.session_state.weight_mode_radio
                    current_ahp_weights = st.session_state.get('ahp_weights', None)
                    current_manual_weights = st.session_state.get('manual_weights', {})
                    # Save individual manual weight values
                    individual_manual_weights = {}
                    if current_weight_mode == "Ajuste Manual":
                        for k in METRIC_NAMES:
                            individual_manual_weights[k] = st.session_state.get(f"manual_weight_{k}")
                    # Get active weights
                    if current_weight_mode == "Calcular nuevos pesos":
                        if current_ahp_weights:
                            user_weights = current_ahp_weights
                            weights_config_name = "Pesos Calculados"
                            for ahp_config_name, config in st.session_state.ahp_configurations.items():
                                if to_dict_flat(config['weights']) == to_dict_flat(current_ahp_weights):
                                    weights_config_name = f"Configuración Calculada: {ahp_config_name}"
                                    break
                        else:
                            user_weights = get_recommended_weights()
                            weights_config_name = "Pesos Recomendados"
                    elif current_weight_mode == "Ajuste Manual":
                        manual_weights = {k: st.session_state[f"manual_weight_{k}"] for k in METRIC_NAMES}
                        user_weights, _ = validate_manual_weights(manual_weights)
                        weights_config_name = "Pesos Manuales Personalizados"
                        for manual_config_name, config in st.session_state.saved_weights.items():
                            normalized_config = {k: float(v) for k, v in config.items()}
                            total = sum(normalized_config.values())
                            if total != 1.0:
                                normalized_config = {k: v/total for k, v in normalized_config.items()}
                            if to_dict_flat(normalized_config) == to_dict_flat(user_weights):
                                weights_config_name = f"Configuración Manual: {manual_config_name}"
                                break
                    else:  # Pesos Recomendados
                        user_weights = get_recommended_weights()
                        weights_config_name = "Pesos Recomendados"                    
                    sensor = IoTSustainability(device.get('nombre', 'Sin nombre'))
                    sensor.weights = {k: float(extract_weight_value(v)) for k, v in user_weights.items()}
                    sensor.calculate_energy_consumption(
                        float(device.get('potencia', 0)),
                        float(device.get('horas', 0)),
                        float(device.get('dias', 0))
                    )
                    sensor.calculate_carbon_footprint()
                    sensor.calculate_ewaste(
                        float(device.get('peso', 0)),
                        float(device.get('vida', 0))
                    )
                    sensor.calculate_renewable_energy(float(device.get('energia_renovable', 0)))
                    sensor.calculate_energy_efficiency(float(device.get('funcionalidad', 0)))
                    sensor.calculate_durability(float(device.get('vida', 0)))
                    sensor.calculate_recyclability(float(device.get('reciclabilidad', 0)))
                    sensor.calculate_maintenance_index(
                        int(device.get('B', 0)),
                        float(device.get('Wb', 0)),
                        int(device.get('M', 0)),
                        int(device.get('C', 0)),
                        float(device.get('Wc', 0)),
                        float(device.get('W0', 0)),
                        float(device.get('W', 0))
                    )
                    result = sensor.calculate_sustainability()
                    device_data = device.copy()
                    device_data.update({
                        "id": str(uuid.uuid4()),
                        "calculation_done": True,
                        "used_weights": user_weights,
                        "result": result,
                        "snapshot_form": device.copy(),
                        "snapshot_weights": create_weights_snapshot(user_weights, current_weight_mode)
                    })
                    st.session_state.devices.append(device_data)
                    update_device_selection()  # Update selection when adding device
                    st.session_state['imported_devices'] = [d for d in st.session_state['imported_devices'] if d.get('_import_hash') != device.get('_import_hash')]
                    for var in ["global_result", "global_calculation_date"]:
                        if var in st.session_state:
                            del st.session_state[var]
                    if 'import_message' in st.session_state:
                        del st.session_state['import_message']
                    # Restore weight state
                    st.session_state.weight_mode_radio = current_weight_mode
                    if current_ahp_weights:
                        st.session_state.ahp_weights = current_ahp_weights
                    if current_manual_weights:
                        st.session_state.manual_weights = current_manual_weights
                    # Restore individual manual weight values
                    if current_weight_mode == "Ajuste Manual":
                        for k, v in individual_manual_weights.items():
                            st.session_state[f"manual_weight_{k}"] = v
                    st.success(f"Dispositivo '{device.get('nombre', 'Sin nombre')}' añadido correctamente al sistema.")
                    st.rerun()
                if st.session_state[key_exp]:
                    st.write(device)
        st.info("Cuando estés listo, podrás añadir los dispositivos individualmente o todos juntos al sistema. Recuerda seleccionar los pesos antes de añadirlos.")

        # Button to add all imported devices to the system
        if st.session_state['imported_devices']:
            if st.button("Añadir todos los dispositivos importados al sistema", key="btn_add_all_importados"):
                # Save current weight state
                current_weight_mode = st.session_state.weight_mode_radio
                current_ahp_weights = st.session_state.get('ahp_weights', None)
                current_manual_weights = st.session_state.get('manual_weights', {})
                individual_manual_weights = {}
                if current_weight_mode == "Ajuste Manual":
                    for k in METRIC_NAMES:
                        individual_manual_weights[k] = st.session_state.get(f"manual_weight_{k}")
                new_devices = []
                for device in st.session_state['imported_devices']:
                    name = device.get('nombre', 'Sin nombre')
                    # Get active weights
                    if current_weight_mode == "Calcular nuevos pesos":
                        if current_ahp_weights:
                            user_weights = current_ahp_weights
                            weights_config_name = "Pesos Calculados"
                            for ahp_config_name, config in st.session_state.ahp_configurations.items():
                                if to_dict_flat(config['weights']) == to_dict_flat(user_weights):
                                    weights_config_name = f"Configuración Calculada: {ahp_config_name}"
                                    break
                        else:
                            user_weights = get_recommended_weights()
                            weights_config_name = "Pesos Recomendados"
                    elif current_weight_mode == "Ajuste Manual":
                        manual_weights = {k: st.session_state[f"manual_weight_{k}"] for k in METRIC_NAMES}
                        user_weights, _ = validate_manual_weights(manual_weights)
                        weights_config_name = "Pesos Manuales Personalizados"
                        for manual_config_name, config in st.session_state.saved_weights.items():
                            # Normalize saved configuration before comparing
                            normalized_config = {k: float(v) for k, v in config.items()}
                            total = sum(normalized_config.values())
                            if total != 1.0:
                                normalized_config = {k: v/total for k, v in normalized_config.items()}
                            if to_dict_flat(normalized_config) == to_dict_flat(user_weights):
                                weights_config_name = f"Configuración Manual: {manual_config_name}"
                                break
                    else:
                        user_weights = get_recommended_weights()
                        weights_config_name = "Pesos Recomendados"

                    sensor = IoTSustainability(name)
                    sensor.weights = {k: float(extract_weight_value(v)) for k, v in user_weights.items()}
                    sensor.calculate_energy_consumption(
                        float(device.get('potencia', 0)),
                        float(device.get('horas', 0)),
                        float(device.get('dias', 0))
                    )
                    sensor.calculate_carbon_footprint()
                    sensor.calculate_ewaste(
                        float(device.get('peso', 0)),
                        float(device.get('vida', 0))
                    )
                    sensor.calculate_renewable_energy(float(device.get('energia_renovable', 0)))
                    sensor.calculate_energy_efficiency(float(device.get('funcionalidad', 0)))
                    sensor.calculate_durability(float(device.get('vida', 0)))
                    sensor.calculate_recyclability(float(device.get('reciclabilidad', 0)))
                    sensor.calculate_maintenance_index(
                        int(device.get('B', 0)),
                        float(device.get('Wb', 0)),
                        int(device.get('M', 0)),
                        int(device.get('C', 0)),
                        float(device.get('Wc', 0)),
                        float(device.get('W0', 0)),
                        float(device.get('W', 0))
                    )
                    result = sensor.calculate_sustainability()
                    device_data = device.copy()
                    device_data.update({
                        "id": str(uuid.uuid4()),
                        "calculation_done": True,
                        "used_weights": user_weights,
                        "result": result,
                        "snapshot_form": device.copy(),
                        "snapshot_weights": create_weights_snapshot(user_weights, current_weight_mode)
                    })
                    new_devices.append(device_data)
                st.session_state.devices.extend(new_devices)
                update_device_selection()  # Update selection when adding devices
                st.session_state['imported_devices'] = []
                if 'import_message' in st.session_state:
                    del st.session_state['import_message']
                for var in ["global_result", "global_calculation_date"]:
                    if var in st.session_state:
                        del st.session_state[var]
                # Restore weight state
                st.session_state.weight_mode_radio = current_weight_mode
                if current_ahp_weights:
                    st.session_state.ahp_weights = current_ahp_weights
                if current_manual_weights:
                    st.session_state.manual_weights = current_manual_weights
                if current_weight_mode == "Ajuste Manual":
                    for k, v in individual_manual_weights.items():
                        st.session_state[f"manual_weight_{k}"] = v
                st.success("Todos los dispositivos importados han sido añadidos correctamente al sistema.")
                st.rerun()

        # Button to clean imported devices list
        if st.button("Limpiar lista de dispositivos importados", key="btn_limpiar_importados"):
            st.session_state['imported_devices'] = []
            if 'import_message' in st.session_state:
                del st.session_state['import_message']
                st.rerun()

# Initialize in session_state if they don't exist
for k, (default, _) in FORM_KEYS.items():
    if f"form_{k}" not in st.session_state:
        st.session_state[f"form_{k}"] = default

col1, col2 = st.columns([2, 1])

with col1:
    submitted = False  # Initialize to avoid NameError
    with st.form("formulario_datos"):
        st.subheader("Datos del dispositivo IoT")
        colA, colB = st.columns(2)
        with colA:
            nombre = st.text_input("Nombre del dispositivo", value=st.session_state["form_nombre"], help="Nombre descriptivo del dispositivo IoT.")
            potencia = st.number_input("Potencia (W)", value=st.session_state["form_potencia"], help="Potencia eléctrica en vatios (W) del dispositivo cuando está en funcionamiento.")
            horas = st.number_input("Horas uso diario", value=st.session_state["form_horas"], help="Cantidad de horas al día que el dispositivo está en uso.")
            dias = st.number_input("Días uso/año", value=st.session_state["form_dias"], help="Número de días al año que el dispositivo opera.")
            peso = st.number_input("Peso dispositivo (kg)", value=st.session_state["form_peso"], help="Peso total del dispositivo en kilogramos.")
            vida = st.number_input("Vida útil (años)", value=st.session_state["form_vida"], help="Duración esperada del dispositivo antes de desecharse o reemplazarse.")

        with colB:
            energia_renovable = st.slider("Energía renovable (%)", 0, 100, st.session_state["form_energia_renovable"], help="Porcentaje de energía que proviene de fuentes renovables.")
            funcionalidad = st.slider("Funcionalidad (1-10)", 1, 10, st.session_state["form_funcionalidad"], help="Nivel de funcionalidad y utilidad que ofrece el dispositivo.")
            reciclabilidad = st.slider("Reciclabilidad (%)", 0, 100, st.session_state["form_reciclabilidad"], help="Porcentaje del dispositivo que puede reciclarse al finalizar su vida útil.")

        with st.expander("Datos de mantenimiento"):
            colM1, colM2 = st.columns(2)
            with colM1:
                B = st.number_input("Baterías vida útil", value=st.session_state["form_B"], help="Cantidad de baterías necesarias durante toda la vida útil del dispositivo.")
                Wb = st.number_input("Peso batería (g)", value=st.session_state["form_Wb"], help="Peso de cada batería en gramos.")
                M = st.number_input("Mantenimientos", value=st.session_state["form_M"], help="Número de veces que el dispositivo requiere mantenimiento.")
                C = st.number_input("Componentes reemplazados", value=st.session_state["form_C"], help="Número de componentes reemplazados en mantenimientos.")

            with colM2:
                Wc = st.number_input("Peso componente (g)", value=st.session_state["form_Wc"], help="Peso promedio de cada componente reemplazado en gramos.")
                W0 = st.number_input("Peso nuevo (g)", value=st.session_state["form_W0"], help="Peso total del dispositivo cuando es nuevo.")
                W = st.number_input("Peso final (g)", value=st.session_state["form_W"], help="Peso final del dispositivo después del uso.")

        submitted = st.form_submit_button("Añadir dispositivo")

with col2:
    pesos_usuario = show_weights_interface()

if submitted:
    # Eliminate only global results and date, NOT AHP weights
    for var in ["global_result", "global_calculation_date"]:
        if var in st.session_state:
            del st.session_state[var]

    # Determine active weights and configuration name at this moment
    if st.session_state.weight_mode_radio == "Calcular nuevos pesos":
        if 'ahp_weights' in st.session_state:
            pesos_usuario = st.session_state.ahp_weights
            # Search for active calculated configuration name
            nombre_config_pesos = "Pesos Calculados"
            for nombre_config_ahp, config in st.session_state.ahp_configurations.items():
                if to_dict_flat(config['weights']) == to_dict_flat(pesos_usuario):
                    nombre_config_pesos = f"Configuración Calculada: {nombre_config_ahp}"
                    break
        else:
            st.warning("No hay pesos AHP calculados. Se usarán los pesos recomendados.")
            pesos_usuario = get_recommended_weights()
            nombre_config_pesos = "Pesos Recomendados"
    elif st.session_state.weight_mode_radio == "Ajuste Manual":
        pesos_manuales = {k: st.session_state[f"manual_weight_{k}"] for k in METRIC_NAMES}
        pesos_usuario, _ = validate_manual_weights(pesos_manuales)
        # Search for active manual configuration name
        nombre_config_pesos = "Pesos Manuales Personalizados"
        for nombre_config_manual, config in st.session_state.saved_weights.items():
            # Normalize saved configuration before comparing
            config_normalizada = {k: float(v) for k, v in config.items()}
            suma = sum(config_normalizada.values())
            if suma != 1.0:
                config_normalizada = {k: v/suma for k, v in config_normalizada.items()}
            if to_dict_flat(config_normalizada) == to_dict_flat(pesos_usuario):
                nombre_config_pesos = f"Configuración Manual: {nombre_config_manual}"
                break
    else:
        pesos_usuario = get_recommended_weights()
        nombre_config_pesos = "Pesos Recomendados"

    # Calculate sustainability index using these weights
    sensor = IoTSustainability(nombre)
    pesos_limpios = {}
    for k, v in pesos_usuario.items():
        if isinstance(v, dict):
            v = list(v.values())[0]
        try:
            pesos_limpios[k] = float(v)
        except Exception:
            continue
    sensor.weights = pesos_limpios
    sensor.calculate_energy_consumption(potencia, horas, dias)
    sensor.calculate_carbon_footprint()
    sensor.calculate_ewaste(peso, vida)
    sensor.calculate_renewable_energy(energia_renovable)
    sensor.calculate_energy_efficiency(funcionalidad)
    sensor.calculate_durability(vida)
    sensor.calculate_recyclability(reciclabilidad)
    sensor.calculate_maintenance_index(B, Wb, M, C, Wc, W0, W)
    resultado = sensor.calculate_sustainability()

    dispositivo_data = {
        "id": str(uuid.uuid4()),
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
        "calculation_done": True,
        "used_weights": pesos_usuario,
        "result": resultado,
        # Save snapshot of form and weights
        "snapshot_form": {k: st.session_state[f"form_{k}"] for k in FORM_KEYS},
        "snapshot_weights": create_weights_snapshot(pesos_usuario, st.session_state.weight_mode_radio)
    }

    st.session_state.devices.append(dispositivo_data)
    update_device_selection()  # Update selection when adding device

    st.success(f"Dispositivo '{nombre}' añadido correctamente. Presiona 'Calcular Índice de Sostenibilidad Total' para ver los resultados.")
    st.rerun()

# --- SHOW INDIVIDUAL RESULTS ---
if st.session_state.devices:
    st.markdown("---")
    st.subheader("Resultados por Dispositivo")

    # Mass selection controls
    col_sel1, col_sel2, col_sel3 = st.columns([1, 1, 2])
    with col_sel1:
        if st.button("Select All"):
            st.session_state.selected_devices = {
                d['id']: True for d in st.session_state.devices
            }
            st.rerun()
    with col_sel2:
        if st.button("Deseleccionar Todos"):
            st.session_state.selected_devices = {
                d['id']: False for d in st.session_state.devices
            }
            st.rerun()
    with col_sel3:
        num_seleccionados = sum(st.session_state.selected_devices.values())
        st.markdown(f"**Dispositivos seleccionados para el cálculo global:** {num_seleccionados}/{len(st.session_state.devices)}")

    # Show individual results for all devices
    for idx, device in enumerate(st.session_state.devices):
        # If no result exists, recalculate using saved weights
        if "result" not in device or not device["calculation_done"]:
            sensor = IoTSustainability(device["nombre"])
            sensor.weights = {k: float(extract_weight_value(v)) for k, v in device["used_weights"].items()}
            sensor.calculate_energy_consumption(device["potencia"], device["horas"], device["dias"])
            sensor.calculate_carbon_footprint()
            sensor.calculate_ewaste(device["peso"], device["vida"])
            sensor.calculate_renewable_energy(device["energia_renovable"])
            sensor.calculate_energy_efficiency(device["funcionalidad"])
            sensor.calculate_durability(device["vida"])
            sensor.calculate_recyclability(device["reciclabilidad"])
            sensor.calculate_maintenance_index(
                device["B"], device["Wb"], device["M"], device["C"], device["Wc"], device["W0"], device["W"]
            )
            resultado = sensor.calculate_sustainability()
            device["result"] = resultado
            device["calculation_done"] = True
        
        # Show summary and control buttons
        with st.container():
            col_res, col_sel, col_btn_det = st.columns([4, 1, 1])
            
            # Checkbox for selection
            if col_sel.checkbox(
                "Include in calculation",
                value=st.session_state.selected_devices.get(device['id'], True),
                key=f"sel_{device['id']}"
            ):
                if not st.session_state.selected_devices.get(device['id'], False):
                    st.session_state.selected_devices[device['id']] = True
                    if 'global_result' in st.session_state:
                        del st.session_state.global_result
                    st.rerun()
            else:
                if st.session_state.selected_devices.get(device['id'], True):
                    st.session_state.selected_devices[device['id']] = False
                    if 'global_result' in st.session_state:
                        del st.session_state.global_result
                    st.rerun()
            
            # Device summary
            col_res.markdown(f"**{device['nombre']}** — Índice: {device['result']['sustainability_index']:.2f}/10")
            
            # Details button
            key_exp = f"expand_device_{device['id']}"
            if key_exp not in st.session_state:
                st.session_state[key_exp] = False
            if col_btn_det.button("Mostrar detalles" if not st.session_state[key_exp] else "Ocultar detalles", key=f"btn_toggle_{device['id']}"):
                st.session_state[key_exp] = not st.session_state[key_exp]
                st.rerun()
            
            if st.session_state[key_exp]:
                show_device(device, device['id'])

    # Space before button
    st.markdown("---")
    st.markdown("&nbsp;", unsafe_allow_html=True)

    # Standard Streamlit button aligned to the left, with emoji
    if 'modo_edicion' in st.session_state and st.session_state.modo_edicion:
        st.warning("Termina de editar o cancelar la edición de un dispositivo antes de calcular el índice global.")
        st.button("🌍 Calcular Índice Global de Sostenibilidad", disabled=True)
    else:
        if st.button("🌍 Calcular Índice Global de Sostenibilidad"):
            selected_devices = get_selected_devices()
            if not selected_devices:
                st.warning("No hay dispositivos seleccionados para el cálculo global.")
            else:
                total_indices = []
                total_metrics = []

                for device in selected_devices:
                    if "result" not in device or not device["calculation_done"]:
                        sensor = IoTSustainability(device["nombre"])
                        sensor.weights = {k: float(extract_weight_value(v)) for k, v in device["used_weights"].items()}
                        sensor.calculate_energy_consumption(device["potencia"], device["horas"], device["dias"])
                        sensor.calculate_carbon_footprint()
                        sensor.calculate_ewaste(device["peso"], device["vida"])
                        sensor.calculate_renewable_energy(device["energia_renovable"])
                        sensor.calculate_energy_efficiency(device["funcionalidad"])
                        sensor.calculate_durability(device["vida"])
                        sensor.calculate_recyclability(device["reciclabilidad"])
                        sensor.calculate_maintenance_index(
                            device["B"], device["Wb"], device["M"], 
                            device["C"], device["Wc"], device["W0"], device["W"]
                        )
                        result = sensor.calculate_sustainability()
                        device["result"] = result
                        device["calculation_done"] = True

                    total_indices.append(device["result"]["sustainability_index"])
                    total_metrics.append(device["result"]["normalized_metrics"])

                total_average = sum(total_indices) / len(total_indices)
                metrics_average = {
                    key: sum(m[key] for m in total_metrics) / len(total_metrics)
                    for key in total_metrics[0]
                }
                st.session_state.global_result = {
                    "total_average": total_average,
                    "metrics_average": metrics_average,
                    "included_devices": selected_devices
                }
                st.success("Resultados actualizados correctamente.")

    # Space after button
    st.markdown("&nbsp;", unsafe_allow_html=True)

# --- SHOW GLOBAL RESULTS ---
show_global_results()

# --- GLOBAL RESULTS EXPORT SECTION ---
if st.session_state.get('global_result'):
    st.markdown('---')
    buffer = export_results_excel()
    included_devices = len(st.session_state.global_result['included_devices'])
    st.download_button(
        label='⬇️ Descargar resultados globales (Excel)',
        data=buffer,
        file_name=f'resultados_globales_{st.session_state.global_result["total_average"]:.1f}_{included_devices}devices_{datetime.now().strftime("%Y%m%d")}.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# --- DOWNLOAD SECTION IN EXPANDER ---
if st.session_state.get('devices'):
    st.markdown('---')
    with st.expander('⬇️ Descargar lista de dispositivos añadidos'):
        solo_seleccionados = st.checkbox("Incluir solo dispositivos seleccionados para el cálculo global")
        formato = st.selectbox('Selecciona el formato de descarga:', ['Excel (.xlsx)', 'CSV (.csv)', 'JSON (.json)'], key='formato_descarga_devices')
        formatos_map = {
            'Excel (.xlsx)': 'excel',
            'CSV (.csv)': 'csv',
            'JSON (.json)': 'json'
        }
        formato_export = formatos_map[formato]
        devices_exportar = get_selected_devices() if solo_seleccionados else st.session_state.devices
        buffer = export_devices_list(devices_exportar, formato=formato_export)
        if formato_export == 'excel':
            st.download_button(
                label='Descargar lista de dispositivos añadidos (Excel)',
                data=buffer,
                file_name=f'devices_{len(devices_exportar)}_{datetime.now().strftime("%Y%m%d")}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        elif formato_export == 'csv':
            st.download_button(
                label='Descargar lista de dispositivos añadidos (CSV)',
                data=buffer,
                file_name=f'devices_{len(devices_exportar)}_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv'
            )
        elif formato_export == 'json':
            st.download_button(
                label='Descargar lista de dispositivos añadidos (JSON)',
                data=buffer,
                file_name=f'devices_{len(devices_exportar)}_{datetime.now().strftime("%Y%m%d")}.json',
                mime='application/json'
            )

# --- FOOTER SECTION ---
st.markdown(
    """
    <hr>
    <div style='text-align: center;'>
        <a href='https://github.com/natalia-ricaurte/IoT' target='_blank' style='margin-right:30px;'>
            <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' width='40' style='vertical-align:middle; margin-right:10px;'/>
            <span style='font-size:18px; vertical-align:middle;'>Repositorio en GitHub</span>
        </a>
        <a href='https://sistemas.uniandes.edu.co/es/' target='_blank' style='margin-left:30px;'>
            <img src='https://upload.wikimedia.org/wikipedia/commons/4/47/University_of_Los_Andes_logo.svg' width='40' style='vertical-align:middle; margin-right:10px;'/>
            <span style='font-size:18px; vertical-align:middle;'>Universidad de los Andes</span>
        </a>
        <br>
        <span style='font-size:12px; color:gray;'>© 2024 Juan Camilo Pacheco, Natalia Andrea Ricaurte, Laura Valentina Lara</span>
    </div>
    """,
    unsafe_allow_html=True
) 