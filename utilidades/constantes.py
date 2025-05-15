# Definición de nombres de métricas
NOMBRES_METRICAS = {
    'CE': 'Consumo de Energía',
    'HC': 'Huella de Carbono',
    'EW': 'E-waste',
    'ER': 'Energía Renovable',
    'EE': 'Eficiencia Energética',
    'DP': 'Durabilidad',
    'RC': 'Reciclabilidad',
    'IM': 'Mantenimiento'
}

# Claves y valores por defecto para el formulario
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