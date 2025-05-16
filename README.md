# Evaluación de Sostenibilidad para Dispositivos IoT

Este proyecto de grado, desarrollado por Juan Camilo Pacheco, Natalia Andrea Ricaurte y Laura Valentina Lara, implementa un modelo de medición de sostenibilidad ambiental para sistemas IoT, enfocado en la fase operativa de los dispositivos. El dashboard interactivo permite evaluar el impacto ambiental de cada dispositivo individual considerando factores como el consumo energético, la generación de residuos electrónicos, el uso de energías renovables, la eficiencia operativa y el procesamiento de datos, incluyendo el enfoque de edge computing.

El sistema utiliza el método AHP (Analytic Hierarchy Process) combinado con los Objetivos de Desarrollo Sostenible (ODS) para proporcionar una evaluación cuantitativa del impacto ambiental, permitiendo escalar el análisis desde dispositivos individuales hasta despliegues completos de IoT.

## Características Principales

- Evaluación de sostenibilidad basada en 8 métricas clave:
  - Consumo de Energía (CE)
  - Huella de Carbono (HC)
  - E-waste (EW)
  - Energía Renovable (ER)
  - Eficiencia Energética (EE)
  - Durabilidad del Producto (DP)
  - Reciclabilidad (RC)
  - Mantenimiento (IM)
- Tres métodos de asignación de pesos:
  - Pesos recomendados (basados en AHP+ODS)
  - Ajuste manual
  - Cálculo mediante comparación por pares
- Exportación de resultados a Excel
- Gestión de configuraciones de pesos
- Visualización de resultados mediante gráficos

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/natalia-ricaurte/IoT
cd IoT
```

2. Crear y activar un entorno virtual (opcional pero recomendado):
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

1. Iniciar la aplicación:
```bash
streamlit run app.py
```

2. Acceder al dashboard en el navegador:
   - URL local: http://localhost:8501
   - URL de red: http://[TU_IP]:8501

## Importación de Dispositivos

Puedes importar una lista de dispositivos desde un archivo Excel, CSV o JSON usando una plantilla robusta y fácil de usar.

- Descarga la plantilla desde el dashboard (botón "Descargar plantilla Excel").
- **No cambies los nombres de las columnas**: el sistema solo acepta los nombres exactos de la plantilla, sin variantes ni traducciones.
- La plantilla incluye una hoja de ayuda con la descripción y unidad de cada campo, y una advertencia destacada.
- Los nombres de las columnas son cortos, en minúsculas, sin tildes ni espacios, y compatibles con cualquier sistema:

| Columna                | Descripción y unidad                                                        |
|------------------------|-----------------------------------------------------------------------------|
| nombre                 | Nombre descriptivo del dispositivo IoT.                                     |
| potencia_w             | Potencia eléctrica en vatios (W) del dispositivo.                           |
| horas_uso_diario       | Cantidad de horas al día que el dispositivo está en uso.                     |
| dias_uso_anio          | Número de días al año que el dispositivo opera.                             |
| peso_kg                | Peso total del dispositivo en kilogramos.                                   |
| vida_util_anios        | Duración esperada del dispositivo antes de desecharse o reemplazarse (años).|
| energia_renovable_pct  | Porcentaje de energía que proviene de fuentes renovables.                   |
| funcionalidad_1_10     | Nivel de funcionalidad y utilidad que ofrece el dispositivo (1-10).         |
| reciclabilidad_pct     | Porcentaje del dispositivo que puede reciclarse al finalizar su vida útil.   |
| baterias_vida_util     | Cantidad de baterías necesarias durante toda la vida útil del dispositivo.   |
| peso_bateria_g         | Peso de cada batería en gramos.                                             |
| mantenimientos         | Número de veces que el dispositivo requiere mantenimiento.                   |
| componentes_reemplazados| Número de componentes reemplazados en mantenimientos.                      |
| peso_componente_g      | Peso promedio de cada componente reemplazado en gramos.                     |
| peso_nuevo_g           | Peso total del dispositivo cuando es nuevo (gramos).                        |
| peso_final_g           | Peso final del dispositivo después del uso (gramos).                        |

- Puedes importar archivos en formato **.xlsx, .csv o .json**.
- El sistema valida automáticamente los datos y muestra advertencias si falta algún campo obligatorio.
- Tras importar, puedes añadir los dispositivos individualmente o todos juntos al sistema.
- El flujo de importación es robusto: el uploader desaparece tras importar, y solo se muestra la lista de dispositivos pendientes de añadir.
- Puedes cancelar la importación en cualquier momento y limpiar el estado.

## Guía Rápida

1. **Definir Pesos**:
   - Selecciona el método de asignación de pesos (recomendados, manual o comparación por pares).
   - Ajusta y guarda configuraciones personalizadas si lo deseas.

2. **Ingresar Dispositivos**:
   - Completa el formulario manualmente **o importa una lista usando la plantilla**.
   - **Recuerda:** solo se aceptan los nombres de columna exactos de la plantilla.
   - Añade los dispositivos individualmente o todos juntos.

3. **Calcular Resultados**:
   - Presiona "Calcular Índice de Sostenibilidad" para ver los resultados individuales y globales.
   - Exporta los resultados a Excel si lo deseas.

## Estructura del Proyecto

```
IoT/
├── app.py                 # Aplicación principal
├── modelo.py             # Modelo de cálculo de sostenibilidad
├── pesos.py              # Lógica de cálculo de pesos AHP
├── componentes/          # Componentes de la interfaz
│   ├── dispositivos.py   # Gestión de dispositivos
│   ├── formularios.py    # Formularios de entrada
│   ├── graficos.py       # Visualizaciones
│   └── pesos_ui.py       # Interfaz de gestión de pesos
├── servicios/            # Servicios auxiliares
│   ├── ahp_servicio.py   # Servicio de cálculo AHP
│   └── exportacion.py    # Exportación de datos
└── utilidades/           # Utilidades generales
    ├── constantes.py     # Constantes del sistema
    ├── estado.py         # Gestión del estado
    └── manejo_datos.py   # Utilidades de datos
```

## Método de Cálculo

El índice de sostenibilidad se calcula combinando:

1. **Métricas Normalizadas**: Cada métrica se normaliza a una escala de 0-10
2. **Pesos AHP**: Asignados mediante:
   - Pesos recomendados basados en ODS
   - Ajuste manual
   - Comparación por pares

El modelo considera aspectos clave de la sostenibilidad ambiental en IoT:
- Consumo energético y eficiencia
- Gestión de residuos electrónicos
- Uso de energías renovables
- Durabilidad y mantenimiento
- Procesamiento de datos y edge computing

## Contacto

Juan Camilo Pacheco - jc.pacheco@uniandes.edu.co
Natalia Andrea Ricaurte - na.ricaurtep@uniandes.edu.co
Laura Valentina Lara - lv.larad@uniandes.edu.co

Link del proyecto: https://github.com/natalia-ricaurte/IoT

## Características y funcionalidades generales.

- **Importación robusta de dispositivos** desde plantilla Excel/CSV/JSON.
- **Validación automática** de campos y tipos de datos.
- **Gestión de estado mejorada**: el uploader desaparece tras importar, y puedes cancelar la importación en cualquier momento.
- **Hoja de ayuda en la plantilla** con descripciones y advertencia.
- **Mapeo flexible de columnas**: aunque se recomienda no cambiar los nombres, el sistema es tolerante a variantes comunes.
- **Adición individual o masiva** de dispositivos importados.
- **Mensajes claros de éxito y advertencia** durante todo el flujo.
- **Sincronización total entre plantilla, mapeo y procesamiento interno.**