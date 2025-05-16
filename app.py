# Librerías estándar
import uuid
from datetime import datetime

# Librerías de terceros
import streamlit as st

# Módulos locales
from utilidades.constantes import NOMBRES_METRICAS, FORM_KEYS, GUIA_USO_DASHBOARD
from utilidades.auxiliares import to_dict_flat, extraer_valor_peso
from utilidades.estado import inicializar_estado, reiniciar_estado
from componentes.dispositivos import mostrar_dispositivo, mostrar_resultados_globales
from componentes.formularios import inicializar_formulario
from componentes.pesos_ui import mostrar_interfaz_pesos
from servicios.ahp_servicio import mostrar_matriz_ahp
from servicios.exportacion import exportar_resultados_excel
from servicios.importacion import generar_plantilla_excel, leer_archivo_dispositivos, generar_plantilla_json
from pesos import obtener_pesos_recomendados, validar_pesos_manuales
from modelo import SostenibilidadIoT

# --- INICIALIZACIÓN DE LA APLICACIÓN ---
st.set_page_config(page_title="Dashboard Sostenibilidad IoT", layout="wide")

# Inicializar estado
inicializar_estado()
inicializar_formulario()

# --- CONTROL DE NAVEGACIÓN ---
if st.session_state.matriz_ahp_abierta:
    mostrar_matriz_ahp()
    st.stop()

# --- INTERFAZ PRINCIPAL ---
st.title("Dashboard de Evaluación de Sostenibilidad - Dispositivos IoT")

# Botón para reiniciar
if st.button("Reiniciar"):
    reiniciar_estado()
    if 'dispositivos_importados' in st.session_state:
        del st.session_state['dispositivos_importados']
    if 'importar_csv' in st.session_state:
        del st.session_state['importar_csv']
    if 'mostrar_importar' in st.session_state:
        st.session_state['mostrar_importar'] = False
    st.rerun()

st.markdown("## Descripción de Métricas y Guía de Uso")
with st.expander("Ver detalles y guía de uso"):
    st.markdown(GUIA_USO_DASHBOARD)

# --- SECCIÓN DE IMPORTACIÓN DE DISPOSITIVOS ---
st.markdown("## Importar lista de dispositivos")
import_container = st.container()
with import_container:
    if 'mostrar_importar' not in st.session_state:
        st.session_state.mostrar_importar = False
    
    # --- Restaurar pesos manuales si es necesario antes de crear los widgets ---
    if 'restaurar_pesos_manuales' in st.session_state and st.session_state['restaurar_pesos_manuales']:
        modo_pesos_actual = st.session_state.get('modo_pesos_radio')
        pesos_ahp_actual = st.session_state.get('pesos_ahp')
        pesos_manuales_actual = st.session_state.get('pesos_manuales', {})
        pesos_manuales_individuales = st.session_state.get('pesos_manuales_individuales', {})
        st.session_state.modo_pesos_radio = modo_pesos_actual
        if pesos_ahp_actual:
            st.session_state.pesos_ahp = pesos_ahp_actual
        if pesos_manuales_actual:
            st.session_state.pesos_manuales = pesos_manuales_actual
        if modo_pesos_actual == "Ajuste Manual":
            for k, v in pesos_manuales_individuales.items():
                st.session_state[f"peso_manual_{k}"] = v
        st.session_state['restaurar_pesos_manuales'] = False
    
    if st.button("Importar lista de dispositivos"):
        # Guardar el estado actual de los pesos antes de cambiar mostrar_importar
        modo_pesos_actual = st.session_state.get('modo_pesos_radio')
        pesos_ahp_actual = st.session_state.get('pesos_ahp')
        pesos_manuales_actual = st.session_state.get('pesos_manuales', {})
        pesos_manuales_individuales = {}
        if modo_pesos_actual == "Ajuste Manual":
            for k in NOMBRES_METRICAS:
                pesos_manuales_individuales[k] = st.session_state.get(f"peso_manual_{k}")
        st.session_state['mostrar_importar'] = True
        # Guardar para restaurar en el próximo ciclo
        st.session_state['restaurar_pesos_manuales'] = True
        st.session_state['pesos_manuales_individuales'] = pesos_manuales_individuales
        st.session_state['modo_pesos_radio'] = modo_pesos_actual
        st.session_state['pesos_ahp'] = pesos_ahp_actual
        st.session_state['pesos_manuales'] = pesos_manuales_actual
        st.rerun()
    
    buffer = generar_plantilla_excel()
    st.download_button(
        label="Descargar plantilla Excel (.xlsx)",
        data=buffer,
        file_name="plantilla_dispositivos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    # Botón para descargar plantilla JSON
    buffer_json = generar_plantilla_json()
    st.download_button(
        label="Descargar plantilla JSON",
        data=buffer_json,
        file_name="plantilla_dispositivos.json",
        mime="application/json"
    )
    st.caption("Recuerda: no cambies los nombres de las columnas (Excel) o claves (JSON) en las plantillas. Deben coincidir exactamente para que la importación funcione.")

    # Mostrar uploader solo si mostrar_importar es True
    if st.session_state.mostrar_importar:
        st.info("Sube un archivo CSV, Excel o JSON con la lista de dispositivos a importar. Descarga la plantilla para ver el formato requerido.")
        if st.button("Cancelar importación", key="cancelar_importacion"):
            # Guardar el estado actual de los pesos antes de cancelar
            modo_pesos_actual = st.session_state.get('modo_pesos_radio')
            pesos_ahp_actual = st.session_state.get('pesos_ahp')
            pesos_manuales_actual = st.session_state.get('pesos_manuales', {})
            pesos_manuales_individuales = {}
            if modo_pesos_actual == "Ajuste Manual":
                for k in NOMBRES_METRICAS:
                    pesos_manuales_individuales[k] = st.session_state.get(f"peso_manual_{k}")
            # Guardar para restaurar en el próximo ciclo
            st.session_state['restaurar_pesos_manuales'] = True
            st.session_state['pesos_manuales_individuales'] = pesos_manuales_individuales
            st.session_state['modo_pesos_radio'] = modo_pesos_actual
            st.session_state['pesos_ahp'] = pesos_ahp_actual
            st.session_state['pesos_manuales'] = pesos_manuales_actual
            st.session_state.mostrar_importar = False
            st.session_state['dispositivos_importados'] = []
            if 'mensaje_importacion' in st.session_state:
                del st.session_state['mensaje_importacion']
            st.rerun()
        archivo_import = st.file_uploader("Selecciona el archivo", type=["csv", "xlsx", "json"], key="importar_csv")
        if archivo_import is not None:
            try:
                df_import = leer_archivo_dispositivos(archivo_import)
                if len(df_import) > 0:
                    importados = df_import.to_dict(orient='records')
                    for d in importados:
                        d['_import_hash'] = str(uuid.uuid4())
                    st.session_state['dispositivos_importados'] = importados
                    if 'importar_csv' in st.session_state:
                        del st.session_state['importar_csv']
                    st.session_state['mostrar_importar'] = False
                    st.session_state['mensaje_importacion'] = f"✅ Archivo '{archivo_import.name}' leído correctamente. Se encontraron {len(df_import)} dispositivos.\n\nAhora puedes añadirlos individualmente o todos al sistema usando los botones correspondientes."

                    # --- GUARDAR Y RESTAURAR ESTADO DE PESOS ---
                    modo_pesos_actual = st.session_state.get('modo_pesos_radio')
                    pesos_ahp_actual = st.session_state.get('pesos_ahp')
                    pesos_manuales_actual = st.session_state.get('pesos_manuales', {})
                    pesos_manuales_individuales = {}
                    if modo_pesos_actual == "Ajuste Manual":
                        for k in NOMBRES_METRICAS:
                            pesos_manuales_individuales[k] = st.session_state.get(f"peso_manual_{k}")
                    # Restaurar
                    st.session_state.modo_pesos_radio = modo_pesos_actual
                    if pesos_ahp_actual:
                        st.session_state.pesos_ahp = pesos_ahp_actual
                    if pesos_manuales_actual:
                        st.session_state.pesos_manuales = pesos_manuales_actual
                    if modo_pesos_actual == "Ajuste Manual":
                        for k, v in pesos_manuales_individuales.items():
                            st.session_state[f"peso_manual_{k}"] = v
                    # --- FIN RESTAURAR ESTADO DE PESOS ---

                    st.rerun()
                else:
                    st.session_state['dispositivos_importados'] = []
                    st.warning("⚠️ El archivo está vacío. No se encontraron dispositivos para importar.")
            except Exception as e:
                st.session_state['dispositivos_importados'] = []
                print(f"Error al leer el archivo: {str(e)}")
                st.error(f"❌ Error al leer el archivo: {str(e)}")

    # Mostrar la lista de dispositivos importados aunque mostrar_importar sea False
    if 'dispositivos_importados' in st.session_state and st.session_state['dispositivos_importados']:
        # Mostrar mensaje de éxito de importación si existe
        if 'mensaje_importacion' in st.session_state:
            st.success(st.session_state['mensaje_importacion'])
        st.markdown("""
        ### Dispositivos importados pendientes de añadir
        Revisa los datos principales de cada dispositivo. Puedes ver los detalles completos haciendo clic en \"Ver detalles\". Selecciona los pesos antes de añadir cada dispositivo al sistema.
        """)
        for idx, disp in enumerate(st.session_state['dispositivos_importados']):
            with st.container():
                col1, col2 = st.columns([5, 1])
                nombre = disp.get('nombre', 'Sin nombre')
                potencia = disp.get('potencia', 'N/A')
                vida = disp.get('vida', 'N/A')
                col1.markdown(f"**{nombre}** | Potencia: {potencia} W | Vida útil: {vida} años")
                key_exp = f"expandir_importado_{idx}"
                if key_exp not in st.session_state:
                    st.session_state[key_exp] = False
                if col2.button("Ver detalles" if not st.session_state[key_exp] else "Ocultar detalles", key=f"btn_det_import_{idx}"):
                    st.session_state[key_exp] = not st.session_state[key_exp]
                    st.rerun()
                if st.session_state[key_exp]:
                    st.write(disp)
                if st.button("Añadir dispositivo al sistema", key=f"btn_add_import_{idx}"):
                    # Guardar el estado actual de los pesos
                    modo_pesos_actual = st.session_state.modo_pesos_radio
                    pesos_ahp_actual = st.session_state.get('pesos_ahp', None)
                    pesos_manuales_actual = st.session_state.get('pesos_manuales', {})
                    
                    # Guardar los valores individuales de los pesos manuales
                    pesos_manuales_individuales = {}
                    if modo_pesos_actual == "Ajuste Manual":
                        for k in NOMBRES_METRICAS:
                            pesos_manuales_individuales[k] = st.session_state.get(f"peso_manual_{k}")
                    
                    # Obtener pesos activos
                    if modo_pesos_actual == "Calcular nuevos pesos":
                        if pesos_ahp_actual:
                            pesos_usuario = pesos_ahp_actual
                            nombre_config_pesos = "Pesos Calculados"
                            for nombre_config_ahp, config in st.session_state.configuraciones_ahp.items():
                                if to_dict_flat(config['pesos']) == to_dict_flat(pesos_usuario):
                                    nombre_config_pesos = f"Configuración Calculada: {nombre_config_ahp}"
                                    break
                        else:
                            pesos_usuario = obtener_pesos_recomendados()
                            nombre_config_pesos = "Pesos Recomendados"
                    elif modo_pesos_actual == "Ajuste Manual":
                        pesos_manuales = {k: st.session_state[f"peso_manual_{k}"] for k in NOMBRES_METRICAS}
                        pesos_usuario, _ = validar_pesos_manuales(pesos_manuales)
                        nombre_config_pesos = "Pesos Manuales Personalizados"
                        for nombre_config_manual, config in st.session_state.pesos_guardados.items():
                            if to_dict_flat(config) == to_dict_flat(pesos_usuario):
                                nombre_config_pesos = f"Configuración Manual: {nombre_config_manual}"
                                break
                    else:
                        pesos_usuario = obtener_pesos_recomendados()
                        nombre_config_pesos = "Pesos Recomendados"

                    sensor = SostenibilidadIoT(nombre)
                    sensor.pesos = {k: float(extraer_valor_peso(v)) for k, v in pesos_usuario.items()}
                    sensor.calcular_consumo_energia(
                        float(disp.get('potencia', 0)),
                        float(disp.get('horas', 0)),
                        float(disp.get('dias', 0))
                    )
                    sensor.calcular_huella_carbono()
                    sensor.calcular_ewaste(
                        float(disp.get('peso', 0)),
                        float(disp.get('vida', 0))
                    )
                    sensor.calcular_energia_renovable(float(disp.get('energia_renovable', 0)))
                    sensor.calcular_eficiencia_energetica(float(disp.get('funcionalidad', 0)))
                    sensor.calcular_durabilidad(float(disp.get('vida', 0)))
                    sensor.calcular_reciclabilidad(float(disp.get('reciclabilidad', 0)))
                    sensor.calcular_indice_mantenimiento(
                        int(disp.get('B', 0)),
                        float(disp.get('Wb', 0)),
                        int(disp.get('M', 0)),
                        int(disp.get('C', 0)),
                        float(disp.get('Wc', 0)),
                        float(disp.get('W0', 0)),
                        float(disp.get('W', 0))
                    )
                    resultado = sensor.calcular_sostenibilidad()
                    dispositivo_data = disp.copy()
                    dispositivo_data.update({
                        "id": str(uuid.uuid4()),
                        "calculo_realizado": True,
                        "pesos_utilizados": pesos_usuario,
                        "resultado": resultado,
                        "snapshot_form": disp.copy(),
                        "snapshot_pesos": {
                            "modo": modo_pesos_actual,
                            "nombre_configuracion": nombre_config_pesos,
                            "pesos_manuales": pesos_manuales_actual,
                            "pesos_ahp": pesos_ahp_actual
                        }
                    })
                    st.session_state.dispositivos.append(dispositivo_data)
                    st.session_state['dispositivos_importados'] = [d for d in st.session_state['dispositivos_importados'] if d.get('_import_hash') != disp.get('_import_hash')]
                    for var in ["resultado_global", "fecha_calculo_global"]:
                        if var in st.session_state:
                            del st.session_state[var]
                    if 'mensaje_importacion' in st.session_state:
                        del st.session_state['mensaje_importacion']
                    
                    # Restaurar el estado de los pesos
                    st.session_state.modo_pesos_radio = modo_pesos_actual
                    if pesos_ahp_actual:
                        st.session_state.pesos_ahp = pesos_ahp_actual
                    if pesos_manuales_actual:
                        st.session_state.pesos_manuales = pesos_manuales_actual
                    
                    # Restaurar los valores individuales de los pesos manuales
                    if modo_pesos_actual == "Ajuste Manual":
                        for k, v in pesos_manuales_individuales.items():
                            st.session_state[f"peso_manual_{k}"] = v
                    
                    st.success(f"Dispositivo '{nombre}' añadido correctamente al sistema.")
                    st.rerun()
        st.info("Cuando estés listo, podrás añadir los dispositivos individualmente o todos juntos al sistema. Recuerda seleccionar los pesos antes de añadirlos.")

        # Botón para añadir todos los dispositivos importados
        if st.session_state['dispositivos_importados']:
            if st.button("Añadir todos los dispositivos importados al sistema", key="btn_add_all_importados"):
                # Guardar el estado actual de los pesos
                modo_pesos_actual = st.session_state.modo_pesos_radio
                pesos_ahp_actual = st.session_state.get('pesos_ahp', None)
                pesos_manuales_actual = st.session_state.get('pesos_manuales', {})
                pesos_manuales_individuales = {}
                if modo_pesos_actual == "Ajuste Manual":
                    for k in NOMBRES_METRICAS:
                        pesos_manuales_individuales[k] = st.session_state.get(f"peso_manual_{k}")
                nuevos_dispositivos = []
                for disp in st.session_state['dispositivos_importados']:
                    nombre = disp.get('nombre', 'Sin nombre')
                    # Obtener pesos activos
                    if modo_pesos_actual == "Calcular nuevos pesos":
                        if pesos_ahp_actual:
                            pesos_usuario = pesos_ahp_actual
                            nombre_config_pesos = "Pesos Calculados"
                            for nombre_config_ahp, config in st.session_state.configuraciones_ahp.items():
                                if to_dict_flat(config['pesos']) == to_dict_flat(pesos_usuario):
                                    nombre_config_pesos = f"Configuración Calculada: {nombre_config_ahp}"
                                    break
                        else:
                            pesos_usuario = obtener_pesos_recomendados()
                            nombre_config_pesos = "Pesos Recomendados"
                    elif modo_pesos_actual == "Ajuste Manual":
                        pesos_manuales = {k: st.session_state[f"peso_manual_{k}"] for k in NOMBRES_METRICAS}
                        pesos_usuario, _ = validar_pesos_manuales(pesos_manuales)
                        nombre_config_pesos = "Pesos Manuales Personalizados"
                        for nombre_config_manual, config in st.session_state.pesos_guardados.items():
                            if to_dict_flat(config) == to_dict_flat(pesos_usuario):
                                nombre_config_pesos = f"Configuración Manual: {nombre_config_manual}"
                                break
                    else:
                        pesos_usuario = obtener_pesos_recomendados()
                        nombre_config_pesos = "Pesos Recomendados"

                    sensor = SostenibilidadIoT(nombre)
                    sensor.pesos = {k: float(extraer_valor_peso(v)) for k, v in pesos_usuario.items()}
                    sensor.calcular_consumo_energia(
                        float(disp.get('potencia', 0)),
                        float(disp.get('horas', 0)),
                        float(disp.get('dias', 0))
                    )
                    sensor.calcular_huella_carbono()
                    sensor.calcular_ewaste(
                        float(disp.get('peso', 0)),
                        float(disp.get('vida', 0))
                    )
                    sensor.calcular_energia_renovable(float(disp.get('energia_renovable', 0)))
                    sensor.calcular_eficiencia_energetica(float(disp.get('funcionalidad', 0)))
                    sensor.calcular_durabilidad(float(disp.get('vida', 0)))
                    sensor.calcular_reciclabilidad(float(disp.get('reciclabilidad', 0)))
                    sensor.calcular_indice_mantenimiento(
                        int(disp.get('B', 0)),
                        float(disp.get('Wb', 0)),
                        int(disp.get('M', 0)),
                        int(disp.get('C', 0)),
                        float(disp.get('Wc', 0)),
                        float(disp.get('W0', 0)),
                        float(disp.get('W', 0))
                    )
                    resultado = sensor.calcular_sostenibilidad()
                    dispositivo_data = disp.copy()
                    dispositivo_data.update({
                        "id": str(uuid.uuid4()),
                        "calculo_realizado": True,
                        "pesos_utilizados": pesos_usuario,
                        "resultado": resultado,
                        "snapshot_form": disp.copy(),
                        "snapshot_pesos": {
                            "modo": modo_pesos_actual,
                            "nombre_configuracion": nombre_config_pesos,
                            "pesos_manuales": pesos_manuales_actual,
                            "pesos_ahp": pesos_ahp_actual
                        }
                    })
                    nuevos_dispositivos.append(dispositivo_data)
                st.session_state.dispositivos.extend(nuevos_dispositivos)
                st.session_state['dispositivos_importados'] = []
                if 'mensaje_importacion' in st.session_state:
                    del st.session_state['mensaje_importacion']
                for var in ["resultado_global", "fecha_calculo_global"]:
                    if var in st.session_state:
                        del st.session_state[var]
                # Restaurar el estado de los pesos
                st.session_state.modo_pesos_radio = modo_pesos_actual
                if pesos_ahp_actual:
                    st.session_state.pesos_ahp = pesos_ahp_actual
                if pesos_manuales_actual:
                    st.session_state.pesos_manuales = pesos_manuales_actual
                if modo_pesos_actual == "Ajuste Manual":
                    for k, v in pesos_manuales_individuales.items():
                        st.session_state[f"peso_manual_{k}"] = v
                st.success("Todos los dispositivos importados han sido añadidos correctamente al sistema.")
                st.rerun()

# Inicializar en session_state si no existen
for k, (default, _) in FORM_KEYS.items():
    if f"form_{k}" not in st.session_state:
        st.session_state[f"form_{k}"] = default

col1, col2 = st.columns([2, 1])

with col1:
    submitted = False  # Inicializar para evitar NameError
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
    pesos_usuario = mostrar_interfaz_pesos()

if submitted:
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
    sensor = SostenibilidadIoT(nombre)
    pesos_limpios = {}
    for k, v in pesos_usuario.items():
        if isinstance(v, dict):
            v = list(v.values())[0]
        try:
            pesos_limpios[k] = float(v)
        except Exception:
            continue
    sensor.pesos = pesos_limpios
    sensor.calcular_consumo_energia(potencia, horas, dias)
    sensor.calcular_huella_carbono()
    sensor.calcular_ewaste(peso, vida)
    sensor.calcular_energia_renovable(energia_renovable)
    sensor.calcular_eficiencia_energetica(funcionalidad)
    sensor.calcular_durabilidad(vida)
    sensor.calcular_reciclabilidad(reciclabilidad)
    sensor.calcular_indice_mantenimiento(B, Wb, M, C, Wc, W0, W)
    resultado = sensor.calcular_sostenibilidad()

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

    st.success(f"Dispositivo '{nombre}' añadido correctamente. Presiona 'Calcular Índice de Sostenibilidad Total' para ver los resultados.")
    st.rerun()

# --- BOTÓN DE REFRESH ---
if 'modo_edicion' in st.session_state and st.session_state.modo_edicion:
    st.warning("Termina de editar o cancelar la edición de un dispositivo antes de calcular el índice global.")
    st.button("Calcular Indice de Sostenibilidad", disabled=True)
else:
    if st.button("Calcular Indice de Sostenibilidad"):
        if not st.session_state.dispositivos:
            st.warning("No hay dispositivos añadidos.")
        else:
            total_indices = []
            metricas_totales = []

            for idx, dispositivo in enumerate(st.session_state.dispositivos):
                # Si no existe resultado, recalcularlo usando los pesos guardados
                if "resultado" not in dispositivo or not dispositivo["calculo_realizado"]:
                    sensor = SostenibilidadIoT(dispositivo["nombre"])
                    sensor.pesos = {k: float(extraer_valor_peso(v)) for k, v in dispositivo["pesos_utilizados"].items()}
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

# --- MOSTRAR RESULTADOS INDIVIDUALES ---
if st.session_state.dispositivos:
    st.markdown("---")
    st.subheader("Resultados por Dispositivo")

    dispositivos = st.session_state.dispositivos
    num_dispositivos = len(dispositivos)

    # Mostrar resultados individuales de todos los dispositivos
    for idx, disp in enumerate(dispositivos):
        # Si no existe resultado, recalcularlo usando los pesos guardados
        if "resultado" not in disp or not disp["calculo_realizado"]:
            sensor = SostenibilidadIoT(disp["nombre"])
            sensor.pesos = {k: float(extraer_valor_peso(v)) for k, v in disp["pesos_utilizados"].items()}
            sensor.calcular_consumo_energia(disp["potencia"], disp["horas"], disp["dias"])
            sensor.calcular_huella_carbono()
            sensor.calcular_ewaste(disp["peso"], disp["vida"])
            sensor.calcular_energia_renovable(disp["energia_renovable"])
            sensor.calcular_eficiencia_energetica(disp["funcionalidad"])
            sensor.calcular_durabilidad(disp["vida"])
            sensor.calcular_reciclabilidad(disp["reciclabilidad"])
            sensor.calcular_indice_mantenimiento(
                disp["B"], disp["Wb"], disp["M"], disp["C"], disp["Wc"], disp["W0"], disp["W"]
            )
            resultado = sensor.calcular_sostenibilidad()
            disp["resultado"] = resultado
            disp["calculo_realizado"] = True
        # Mostrar resumen y botón de expandir/ocultar detalles
        with st.container():
            col_res, col_btn_det = st.columns([5, 1])
            col_res.markdown(f"**{disp['nombre']}** — Índice: {disp['resultado']['indice_sostenibilidad']:.2f}/10")
            key_exp = f"expandir_disp_{disp['id']}"
            if key_exp not in st.session_state:
                st.session_state[key_exp] = False
            if col_btn_det.button("Mostrar detalles" if not st.session_state[key_exp] else "Ocultar detalles", key=f"btn_toggle_{disp['id']}"):
                st.session_state[key_exp] = not st.session_state[key_exp]
                st.rerun()
            if st.session_state[key_exp]:
                mostrar_dispositivo(disp, disp['id'])

# --- MOSTRAR RESULTADOS GLOBALES ---
mostrar_resultados_globales()

    # Botón de descarga directo
if "resultado_global" in st.session_state:
    excel_file = exportar_resultados_excel()
    st.download_button(
        label="Descargar Resultados Completos",
        data=excel_file,
        file_name=f"sostenibilidad_iot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
