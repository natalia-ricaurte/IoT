# Metric names definition
METRIC_NAMES = {
    'EC': 'Energy Consumption',
    'CF': 'Carbon Footprint',
    'EW': 'Electronic Waste',
    'RE': 'Renewable Energy Use',
    'EE': 'Energy Efficiency',
    'PD': 'Product Durability',
    'RC': 'Recyclability',
    'MT': 'Maintenance'
}

METRIC_NAMES_ES = {
    'EC': 'Consumo de Energía',
    'CF': 'Huella de Carbono',
    'EW': 'Residuos Electrónicos',
    'RE': 'Uso de Energía Renovable',
    'EE': 'Eficiencia Energética',
    'PD': 'Durabilidad del Producto',
    'RC': 'Reciclabilidad',
    'MT': 'Mantenimiento'
}


# Form keys and default values
FORM_KEYS = {
    'nombre': ("Sensor de temperatura", "Nombre descriptivo del dispositivo IoT."),
    'potencia': (2.0, "Potencia eléctrica en vatios (W) del dispositivo cuando está en funcionamiento."),
    'horas': (24.0, "Cantidad de horas al día que el dispositivo está en uso."),
    'dias': (365, "Número de días al año que el dispositivo opera."),
    'peso': (0.1, "Peso total del dispositivo en kilogramos."),
    'vida': (5, "Duración esperada del dispositivo antes de desecharse o reemplazarse."),
    'energia_renovable': (30, "Porcentaje de energía que proviene de fuentes renovables."),
    'funcionalidad': (8, "Nivel de funcionalidad y utilidad que ofrece el dispositivo."),
    'reciclabilidad': (65, "Porcentaje del dispositivo que puede reciclarse al finalizar su vida útil."),
    'B': (2, "Cantidad de baterías necesarias durante toda la vida útil del dispositivo."),
    'Wb': (50, "Peso de cada batería en gramos."),
    'M': (1, "Número de veces que el dispositivo requiere mantenimiento."),
    'C': (2, "Número de componentes reemplazados en mantenimientos."),
    'Wc': (20, "Peso promedio de cada componente reemplazado en gramos."),
    'W0': (200, "Peso total del dispositivo cuando es nuevo."),
    'W': (180, "Peso final del dispositivo después del uso.")
}

# Simplified column names and their mapping to internal names
IMPORT_COLUMN_MAPPING = {
    # simplified column name : internal name
    "nombre": "nombre",
    "potencia_w": "potencia",
    "horas_uso_diario": "horas",
    "dias_uso_anio": "dias",
    "peso_kg": "peso",
    "vida_util_anios": "vida",
    "energia_renovable_pct": "energia_renovable",
    "funcionalidad_1_10": "funcionalidad",
    "reciclabilidad_pct": "reciclabilidad",
    "baterias_vida_util": "B",
    "peso_bateria_g": "Wb",
    "mantenimientos": "M",
    "componentes_reemplazados": "C",
    "peso_componente_g": "Wc",
    "peso_nuevo_g": "W0",
    "peso_final_g": "W"
}

# Descriptions and units for each template field
IMPORT_COLUMN_DESCRIPTIONS = {
    "nombre": "Nombre descriptivo del dispositivo IoT.",
    "potencia_w": "Potencia eléctrica en vatios (W) del dispositivo cuando está en funcionamiento.",
    "horas_uso_diario": "Cantidad de horas al día que el dispositivo está en uso.",
    "dias_uso_anio": "Número de días al año que el dispositivo opera.",
    "peso_kg": "Peso total del dispositivo en kilogramos.",
    "vida_util_anios": "Duración esperada del dispositivo antes de desecharse o reemplazarse (años).",
    "energia_renovable_pct": "Porcentaje de energía que proviene de fuentes renovables.",
    "funcionalidad_1_10": "Nivel de funcionalidad y utilidad que ofrece el dispositivo (1-10).",
    "reciclabilidad_pct": "Porcentaje del dispositivo que puede reciclarse al finalizar su vida útil.",
    "baterias_vida_util": "Cantidad de baterías necesarias durante toda la vida útil del dispositivo.",
    "peso_bateria_g": "Peso de cada batería en gramos.",
    "mantenimientos": "Número de veces que el dispositivo requiere mantenimiento.",
    "componentes_reemplazados": "Número de componentes reemplazados en mantenimientos.",
    "peso_componente_g": "Peso promedio de cada componente reemplazado en gramos.",
    "peso_nuevo_g": "Peso total del dispositivo cuando es nuevo (gramos).",
    "peso_final_g": "Peso final del dispositivo después del uso (gramos)."
}

IMPORT_WARNING = (
    "IMPORTANTE: No cambies los nombres de las columnas para evitar errores de importación. "
    "El sistema solo acepta los nombres exactos de la plantilla, sin variantes ni traducciones. "
    "No cambies el orden de las hojas ni elimines la hoja de datos (debe ser la primera hoja del archivo). "
    "Puedes renombrar el archivo, pero asegúrate de mantener la estructura de la plantilla."
)

DASHBOARD_GUIDE = f"""
### Métricas clave del modelo
**Métricas de sostenibilidad evaluadas:**
1. **CE - Consumo de Energía:** kWh anuales usados por el dispositivo.
2. **HC - Huella de Carbono:** kg de CO₂eq emitidos.
3. **EW - E-waste:** kg de residuos electrónicos generados por año.
4. **ER - Energía Renovable:** Porcentaje de energía limpia usada.
5. **EE - Eficiencia Energética:** Relación funcionalidad / consumo.
6. **DP - Durabilidad del Producto:** Vida útil esperada.
7. **RC - Reciclabilidad:** Porcentaje de materiales reciclables.
8. **IM - Mantenimiento:** Impacto de baterías, reemplazos y desgaste.

---

### Guía rápida de uso del dashboard
1. **Define los pesos de las métricas**
   - Selecciona el método de asignación de pesos en la columna derecha antes de ingresar dispositivos.
   - Puedes usar los pesos recomendados, ajustarlos manualmente o calcular nuevos pesos mediante comparación por pares.
   - **Pesos Recomendados:** Basados en análisis y alineación con ODS.
   - **Ajuste Manual:** Permite personalizar los pesos y guardar configuraciones personalizadas.
   - **Pesos Calculados:** Utiliza la matriz de comparación por pares y permite guardar diferentes configuraciones.
   - **Nota:** Los pesos activos al momento de añadir un dispositivo serán los que se usen para su cálculo. El nombre de la configuración utilizada se guarda y se muestra en los resultados y exportaciones.

2. **Ingresa las características de tus dispositivos IoT**
   - Puedes completar el formulario manualmente **o importar una lista de dispositivos usando la plantilla**.
   - {IMPORT_WARNING}
   - La plantilla incluye una hoja de ayuda con la descripción y unidad de cada campo.
   - Sube el archivo en formato Excel, CSV o JSON y revisa los datos antes de añadirlos al sistema.
   - Tras importar, puedes añadir los dispositivos individualmente o todos juntos.
   - Al añadir un nuevo dispositivo, los resultados globales previos se eliminan automáticamente. Deberás recalcular el índice global para ver los resultados actualizados.

3. **Gestiona tu lista de dispositivos**
   - Puedes ver los detalles completos de cada dispositivo pulsando **'Mostrar detalles'**.
   - Dentro de los detalles, consulta los datos de entrada y los pesos utilizados para ese dispositivo, junto con el nombre de la configuración de pesos aplicada.
   - Para eliminar un dispositivo, marca la casilla **'Eliminar dispositivo'** y confirma la acción con el botón correspondiente. Al eliminar cualquier dispositivo, los resultados globales se eliminan y deberás recalcular.
   - Puedes seleccionar o deseleccionar dispositivos para el cálculo global usando los checkboxes **'Incluir en cálculo'**. La lista exportada de dispositivos incluye todos los dispositivos añadidos, independientemente de su estado de selección.
   - Puedes descargar la lista actual de dispositivos en formato Excel, CSV o JSON usando el botón **'Descargar lista de dispositivos añadidos'**. Los archivos exportados mantienen los nombres de columnas de la plantilla para facilitar su reutilización.

4. **Calcula y analiza los resultados**
   - Pulsa **'Calcular Índice de Sostenibilidad'** para ver los resultados individuales y globales.
   - El índice global y los detalles del sistema solo reflejan los dispositivos actualmente seleccionados para el cálculo.

5. **Consulta los detalles del sistema**
   - En la sección de resultados globales, expande **'Detalles del sistema'** para ver:
     - Cantidad total de dispositivos evaluados.
     - Desviación estándar de los índices individuales.
     - Fecha y hora del cálculo global.
     - Nota sobre comparabilidad si los dispositivos fueron evaluados con diferentes pesos.
     - Pesos utilizados para el cálculo global y nombre de la configuración aplicada.
     - Lista de dispositivos incluidos y su índice individual.

6. **Exporta los resultados**
   - **Resultados completos:** Tras calcular el índice global, utiliza el botón **'Descargar Resultados Completos'** para exportar toda la información a un archivo Excel profesional. El archivo incluye:
     - Hoja de resumen con el índice global y gráficos
     - Hoja de dispositivos con todos los datos y su estado de inclusión en el cálculo
     - Hojas de detalle individuales para cada dispositivo
     - El nombre del archivo incluye el índice global, número de dispositivos incluidos y fecha
   - **Lista de dispositivos:** Usa el botón **'Descargar lista de dispositivos añadidos'** para exportar los datos en formato Excel, CSV o JSON:
     - Puedes elegir incluir solo los dispositivos seleccionados para el cálculo global
     - Los archivos exportados mantienen los nombres de columnas de la plantilla
     - El nombre del archivo incluye el número de dispositivos y la fecha

---

**Consejos y advertencias:**
- Si cambias los pesos o la lista de dispositivos, recuerda recalcular el índice global para obtener resultados actualizados.
- Si los dispositivos fueron evaluados con diferentes configuraciones de pesos, los índices individuales pueden no ser directamente comparables.
- El dashboard elimina automáticamente los resultados globales al añadir o eliminar dispositivos para evitar mostrar información desactualizada.
- Puedes guardar y cargar diferentes configuraciones de pesos tanto para el ajuste manual como para los pesos calculados mediante comparación por pares.
- El nombre de la configuración de pesos utilizada se guarda y se muestra en todos los resultados y exportaciones para máxima trazabilidad.
- Los archivos exportados incluyen información sobre qué dispositivos fueron incluidos en el cálculo global para facilitar el seguimiento y la trazabilidad.
"""

# Mapping of internal names to template names for export
EXPORT_COLUMN_MAPPING = {
    "nombre": "nombre",
    "potencia": "potencia_w",
    "horas": "horas_uso_diario",
    "dias": "dias_uso_anio",
    "peso": "peso_kg",
    "vida": "vida_util_anios",
    "energia_renovable": "energia_renovable_pct",
    "funcionalidad": "funcionalidad_1_10",
    "reciclabilidad": "reciclabilidad_pct",
    "B": "baterias_vida_util",
    "Wb": "peso_bateria_g",
    "M": "mantenimientos",
    "C": "componentes_reemplazados",
    "Wc": "peso_componente_g",
    "W0": "peso_nuevo_g",
    "W": "peso_final_g"
} 