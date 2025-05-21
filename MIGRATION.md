# Migración de Código a Inglés

## Reglas de Traducción

### Estructura de Carpetas
- `componentes/` → `components/`
- `utilidades/` → `utils/`
- `servicios/` → `services/`

### Archivos Principales
- `modelo.py` → `model.py`
- `pesos.py` → `weights.py`
- `app.py` → `app_new.py` ✅

### Convenciones de Nombres
- Funciones: `mostrar_dispositivo` → `show_device`
- Variables: `nombre_config` → `config_name`
- Clases: `CalculadoraPesos` → `WeightCalculator`

### Glosario de Términos Técnicos
- dispositivo → device
- peso → weight
- configuración → configuration
- métrica → metric
- índice → index
- cálculo → calculation
- resultado → result
- validación → validation
- importación → import
- exportación → export

### Códigos de Métricas
- `CE` → `EC` (Energy Consumption)
- `HC` → `CF` (Carbon Footprint)
- `EW` → `EW` (Electronic Waste)
- `ER` → `RE` (Renewable Energy Use)
- `EE` → `EE` (Energy Efficiency)
- `DP` → `PD` (Product Durability)
- `RC` → `RC` (Recyclability)
- `IM` → `MT` (Maintenance)

## Plan de Migración

### Fase 1: Archivos Base ✅
1. `modelo.py` → `model.py` ✅
   - Clase `SostenibilidadIoT` → `IoTSustainability`
   - Métodos y variables traducidos
   - Mensajes de error mantenidos en español
   - Lógica y funcionalidad preservada

2. `pesos.py` → `weights.py` ✅
   - Funciones traducidas:
     - `razon_consistencia` → `consistency_ratio`
     - `obtener_pesos_recomendados` → `get_recommended_weights`
     - `validar_pesos_manuales` → `validate_manual_weights`
   - Variables traducidas
   - Códigos de métricas actualizados según README
   - Mensajes de salida mantenidos en español

### Fase 2: Utilidades ✅
1. `utilidades/auxiliares.py` → `utils/helpers.py` ✅
2. `utilidades/constantes.py` → `utils/constants.py` ✅
3. `utilidades/estado.py` → `utils/state.py` ✅

### Fase 3: Componentes ✅
1. `componentes/dispositivos.py` → `components/devices.py` ✅
2. `componentes/formularios.py` → `components/forms.py` ✅
3. `componentes/pesos_ui.py` → `components/weights_ui.py` ✅

### Fase 4: Servicios ✅
1. `servicios/ahp_servicio.py` → `services/ahp_service.py` ✅
2. `servicios/exportacion.py` → `services/export.py` ✅
3. `servicios/importacion.py` → `services/import_service.py` ✅

### Fase 5: App Principal ✅
- `app.py` → `app_new.py` ✅
  - Traducción de variables de estado
  - Traducción de funciones internas
  - Mantenimiento de interfaz en español
  - Actualización de imports

## Notas Importantes
- NO se modificarán textos de la interfaz de usuario
- NO se modificarán mensajes al usuario
- NO se modificarán nombres de configuraciones visibles
- NO se modificarán descripciones y ayudas
- NO se modificarán nombres de archivos de datos (ej: plantillas)
- Las variables de estado de Streamlit (`st.session_state`) se mantendrán en español
  - Ejemplos: `dispositivos`, `modo_pesos_radio`, `resultado_global`, etc.

## Proceso de Validación
1. Verificar que todos los imports se actualizaron ✅
2. Probar que la aplicación sigue funcionando ✅
3. Verificar que la UI sigue en español ✅
4. Documentar cambios en este archivo ✅

## Estado de la Migración

### Fases Completadas ✅
- Fase 1: Archivos Base
- Fase 2: Utilidades
- Fase 3: Componentes
- Fase 4: Servicios
- Fase 5: App Principal

## Registro de Cambios
- Migrado `components/weights_ui.py` a `components/weights_ui.py`
- Migrado `servicios/ahp_servicio.py` a `services/ahp_service.py`
- Migrado `utilidades/estado.py` a `utils/state.py`
- Migrado `servicios/exportacion.py` a `services/export.py`
- Migrado `servicios/importacion.py` a `services/import_service.py`
- Migrado `componentes/formularios.py` a `components/forms.py`
- Migrado `componentes/graficos.py` a `components/charts.py`
- Migrado `componentes/dispositivos.py` a `components/devices.py`
- Migrado `utilidades/constantes.py` a `utils/constants.py`
- Migrado `utilidades/auxiliares.py` a `utils/helpers.py`
- Migrado `pesos.py` a `weights.py`
- Migrado `modelo.py` a `model.py`
- Migrado `app.py` a `app_new.py`
- Creado archivo MIGRATION.md con plan de migración
- Actualizado estado de la migración
- Corregidas inconsistencias en la documentación

## Detalle de Cambios por Archivo

### app_new.py (anteriormente app.py)
#### Variables de Estado
- `dispositivos` → `devices`
- `dispositivos_seleccionados` → `selected_devices`
- `modo_pesos_radio` → `weight_mode_radio`
- `resultado_global` → `global_result`
- `fecha_calculo_global` → `global_calculation_date`
- `pesos_ahp` → `ahp_weights`
- `pesos_manuales` → `manual_weights`
- `configuraciones_ahp` → `ahp_configurations`
- `pesos_guardados` → `saved_weights`

#### Funciones
- `actualizar_seleccion_dispositivos` → `update_device_selection`
- `obtener_dispositivos_seleccionados` → `get_selected_devices`
- `mostrar_dispositivo` → `show_device`
- `mostrar_resultados_globales` → `show_global_results`
- `inicializar_formulario` → `initialize_form`
- `mostrar_interfaz_pesos` → `show_weights_interface`
- `mostrar_matriz_ahp` → `show_ahp_matrix`
- `exportar_resultados_excel` → `export_results_excel`
- `exportar_lista_dispositivos` → `export_devices_list`
- `generar_plantilla_excel` → `generate_excel_template`
- `leer_archivo_dispositivos` → `read_devices_file`
- `generar_plantilla_json` → `generate_json_template`

#### Variables
- `nombre` → `name`
- `potencia` → `power`
- `horas` → `hours`
- `dias` → `days`
- `peso` → `weight`
- `vida` → `life`
- `energia_renovable` → `renewable_energy`
- `funcionalidad` → `functionality`
- `reciclabilidad` → `recyclability`
- `pesos_usuario` → `user_weights`
- `nombre_config_pesos` → `weight_config_name`
- `pesos_limpios` → `clean_weights`
- `dispositivo_data` → `device_data`
- `snapshot_form` → `form_snapshot`
- `snapshot_pesos` → `weights_snapshot`

### model.py (anteriormente modelo.py)
#### Clases
- `SostenibilidadIoT` → `IoTSustainability`

#### Atributos de Clase
- `nombre_dispositivo` → `device_name`
- `resultados` → `results`
- `pesos` → `weights`
- `referencias` → `references`

#### Métodos
- `calcular_consumo_energia` → `calculate_energy_consumption`
- `calcular_huella_carbono` → `calculate_carbon_footprint`
- `calcular_ewaste` → `calculate_ewaste`
- `calcular_energia_renovable` → `calculate_renewable_energy`
- `calcular_eficiencia_energetica` → `calculate_energy_efficiency`
- `calcular_durabilidad` → `calculate_durability`
- `calcular_reciclabilidad` → `calculate_recyclability`
- `calcular_indice_mantenimiento` → `calculate_maintenance_index`
- `normalizar_metrica` → `normalize_metric`
- `calcular_sostenibilidad` → `calculate_sustainability`

#### Variables
- `potencia_W` → `power_W`
- `horas_uso_diario` → `daily_usage_hours`
- `dias_uso_anual` → `annual_usage_days`
- `consumo_kWh` → `consumption_kWh`
- `factor_emision` → `emission_factor`
- `huella_carbono` → `carbon_footprint`
- `peso_dispositivo_kg` → `device_weight_kg`
- `vida_util_años` → `useful_life_years`
- `porcentaje_renovable` → `renewable_percentage`
- `indice_funcionalidad` → `functionality_index`
- `consumo_normalizado` → `normalized_consumption`
- `eficiencia` → `efficiency`
- `porcentaje_reciclable` → `recyclable_percentage`
- `numerador` → `numerator`
- `metricas_normalizadas` → `normalized_metrics`
- `indice_sostenibilidad` → `sustainability_index`
- `metricas_crudas` → `raw_metrics`

### weights.py (anteriormente pesos.py)
#### Funciones
- `razon_consistencia` → `consistency_ratio`
- `obtener_pesos_recomendados` → `get_recommended_weights`
- `validar_pesos_manuales` → `validate_manual_weights`

#### Variables
- `df_criterios` → `criteria_df`
- `suma_columnas` → `column_sums`
- `matriz_normalizada` → `normalized_matrix`
- `pesos` → `weights`
- `matriz_comparacion` → `comparison_matrix`
- `matriz_aleatoria` → `random_matrix`
- `df_temp` → `temp_df`
- `suma` → `sum`
- `ic` → `ci` (Consistency Index)
- `rc` → `cr` (Consistency Ratio)
- `metricas` → `metrics`
- `matriz` → `matrix`
- `pesos_dict` → `weights_dict`
- `suma` → `total`
- `pesos_normalizados` → `normalized_weights`

#### Códigos de Métricas
- `CE` → `EC` (Energy Consumption)
- `HC` → `CF` (Carbon Footprint)
- `EW` → `EW` (Electronic Waste)
- `ER` → `RE` (Renewable Energy Use)
- `EE` → `EE` (Energy Efficiency)
- `DP` → `PD` (Product Durability)
- `RC` → `RC` (Recyclability)
- `IM` → `MT` (Maintenance)

#### Notas Específicas
- Se mantuvieron los mensajes de error y salida en español
- Se mantuvieron los nombres de columnas en DataFrames en inglés ('weight' en lugar de 'peso')
- Se añadieron comentarios explicativos para los códigos de métricas 

### helpers.py (anteriormente auxiliares.py)
#### Imports
- `utilidades.constantes` → `utils.constants`
- `MAPEO_COLUMNAS_IMPORTACION` → `IMPORT_COLUMNS_MAPPING`
- `pesos` → `weights`
- `obtener_pesos_recomendados` → `get_recommended_weights`

#### Funciones
- `to_dict_flat` (se mantiene igual por ser un nombre técnico)
- `obtener_valor_dispositivo` → `get_device_value`
- `extraer_valor_peso` → `extract_weight_value`
- `crear_snapshot_pesos` → `create_weights_snapshot`

#### Variables
- `pesos_usuario` → `user_weights`
- `modo_pesos` → `weight_mode`
- `pesos_limpios` → `clean_weights`
- `nombre_config` → `config_name`
- `nombre_config_ahp` → `ahp_config_name`
- `config` → `config`
- `config_normalizada` → `normalized_config`
- `suma` → `total`
- `nombre_config_manual` → `manual_config_name`

#### Documentación
- Traducidos los docstrings al inglés
- Mantenidos los mensajes de error en español

#### Notas Específicas
- Se mantuvieron los nombres de las claves en el diccionario de retorno en inglés
- Se mantuvieron los mensajes de error en español
- Se actualizaron los imports para reflejar la nueva estructura de carpetas 

### constants.py (anteriormente constantes.py)
#### Notas Importantes
- Se mantuvieron todos los nombres de constantes en español ya que son utilizados en la interfaz de usuario
- Se mantuvieron los nombres de columnas en español para importación/exportación
- Se mantuvieron los códigos de métricas originales (CE, HC, EW, etc.)
- Se mantuvieron las descripciones y mensajes en español
- Se mantuvieron los nombres de las claves del formulario en español
- Se agregaron nombres en inglés en el mapeo de importación solo para compatibilidad

#### Constantes
- `NOMBRES_METRICAS` → `METRIC_NAMES`
- `FORM_KEYS` (se mantiene igual)
- `MAPEO_COLUMNAS_IMPORTACION` → `IMPORT_COLUMN_MAPPING`
- `DESCRIPCION_COLUMNAS_IMPORTACION` → `IMPORT_COLUMN_DESCRIPTIONS`
- `ADVERTENCIA_IMPORTACION` → `IMPORT_WARNING`
- `GUIA_USO_DASHBOARD` → `DASHBOARD_GUIDE`
- `MAPEO_COLUMNAS_EXPORTACION` → `EXPORT_COLUMN_MAPPING`

### devices.py (anteriormente dispositivos.py)
#### Funciones
- `mostrar_dispositivo` → `show_device`
- `mostrar_resultados_globales` → `show_global_results`

#### Variables
- `dispositivo` → `device`
- `idx` → `idx` (se mantiene igual)
- `resultado` → `result`
- `nombre` → `name`
- `recomendaciones` → `recommendations`
- `nombres_campos` → `field_names`
- `datos` → `data`
- `df_datos` → `df_data`
- `snapshot_pesos` → `weights_snapshot`
- `pesos` → `weights`
- `pesos_limpios` → `clean_weights`
- `nombre_config` → `config_name`
- `eliminar_key` → `delete_key`
- `resultado_global` → `global_result`
- `promedio_total` → `total_average`
- `promedio_metricas` → `metrics_average`
- `recomendaciones_globales` → `global_recommendations`
- `dispositivos` → `devices`
- `dispositivos_incluidos` → `included_devices`
- `pesos_usados` → `used_weights`
- `datos_dispositivos` → `device_data`
- `df_dispositivos` → `df_devices`

#### Variables de Estado de Streamlit (se mantienen en español hasta Fase 5)
- `st.session_state.dispositivos`
- `st.session_state.modo_pesos_radio`
- `st.session_state.dispositivos_seleccionados`
- `st.session_state.resultado_global`
- `st.session_state.fecha_calculo_global`
- `st.session_state.pesos_ahp`
- `st.session_state.ahp_resultados`
- `st.session_state.mostrar_tabla_pesos_ahp`
- `st.session_state.snapshot_pesos`

#### Imports
- `componentes.graficos` → `components.charts`
- `utilidades.constantes` → `utils.constants`
- `utilidades.auxiliares` → `utils.helpers`
- `pesos` → `weights`
- `crear_snapshot_pesos` → `create_weights_snapshot`
- `obtener_pesos_recomendados` → `get_recommended_weights`
- `validar_pesos_manuales` → `validate_manual_weights`

#### Estructura de Datos
- Se mantuvieron las claves de los diccionarios en español:
  - `calculo_realizado`
  - `metricas_normalizadas`
  - `indice_sostenibilidad`
  - `pesos_manuales`
  - `pesos_utilizados`
  - `nombre_configuracion`

#### Notas Específicas
- Se mantuvieron todos los mensajes de la interfaz en español
- Se mantuvieron los nombres de las claves en los diccionarios de datos en español
- Se mantuvieron los nombres de las variables de estado de Streamlit en español (serán traducidas en la Fase 5)
- Se actualizaron los imports para reflejar la nueva estructura de carpetas
- Se mantuvieron los nombres de las métricas y sus códigos en español
- Se mantuvieron los nombres de las columnas en los DataFrames en español ('Valor', 'Peso', 'Métrica', etc.)
- Se mantuvieron los nombres de las claves en los diccionarios de configuración en español

### components/weights_ui.py (Migrado desde componentes/pesos_ui.py)

#### Cambios Realizados:
1. **Traducción de nombres de funciones:**
   - `mostrar_selector_pesos` -> `show_weights_selector`
   - `mostrar_pesos_manuales` -> `show_manual_weights`
   - `mostrar_pesos_ahp` -> `show_ahp_weights`
   - `mostrar_pesos_guardados` -> `show_saved_weights`

2. **Traducción de variables:**
   - `pesos_recomendados` -> `recommended_weights`
   - `pesos_manuales` -> `manual_weights`
   - `configuracion` -> `config`
   - `nombre_config` -> `config_name`
   - `pesos_limpios` -> `clean_weights`

3. **Mantenimiento de nombres en español:**
   - Variables de estado de Streamlit
   - Mensajes de la interfaz
   - Nombres de configuraciones
   - Títulos y encabezados
   - Mensajes de ayuda y explicaciones

### services/export.py (Migrado desde servicios/exportacion.py)

#### Cambios Realizados:
1. **Traducción de nombres de funciones:**
   - `exportar_resultados_excel` -> `export_results_excel`
   - `exportar_lista_dispositivos` -> `export_devices_list`

2. **Traducción de nombres de clases:**
   - `ExportadorExcel` -> `ExcelExporter`

3. **Traducción de nombres de métodos:**
   - `_obtener_configuracion_pesos` -> `_get_weights_configuration`
   - `_crear_encabezado_resumen` -> `_create_summary_header`
   - `_crear_tabla_pesos` -> `_create_weights_table`
   - `_crear_grafico_radar` -> `_create_radar_chart`
   - `_crear_hoja_resumen` -> `_create_summary_sheet`
   - `_crear_hoja_dispositivos` -> `_create_devices_sheet`