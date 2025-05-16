# Evaluación de Sostenibilidad para Dispositivos IoT

Este proyecto de grado, desarrollado por Juan Camilo Pacheco, Natalia Andrea Ricaurte y Laura Valentina Lara, implementa un modelo de medición de sostenibilidad ambiental para sistemas IoT, enfocado en la fase operativa de los dispositivos. El dashboard interactivo permite evaluar el impacto ambiental de cada dispositivo individual considerando factores como el consumo energético, la generación de residuos electrónicos, el uso de energías renovables, la eficiencia operativa y el procesamiento de datos, incluyendo el enfoque de edge computing.

El sistema utiliza el método AHP (Analytic Hierarchy Process) combinado con los Objetivos de Desarrollo Sostenible (ODS) para proporcionar una evaluación cuantitativa del impacto ambiental, permitiendo escalar el análisis desde dispositivos individuales hasta despliegues completos de IoT.

## Características Principales

- **Evaluación Integral**: 8 métricas clave para una evaluación completa:
  - Consumo de Energía (CE): Evalúa el consumo eléctrico en kWh
  - Huella de Carbono (HC): Calcula las emisiones de CO₂ en kg
  - E-waste (EW): Mide la generación de residuos electrónicos
  - Energía Renovable (ER): Porcentaje de energía limpia utilizada
  - Eficiencia Energética (EE): Evalúa la relación entre funcionalidad y consumo
  - Durabilidad del Producto (DP): Vida útil del dispositivo
  - Reciclabilidad (RC): Porcentaje de materiales reciclables
  - Mantenimiento (IM): Impacto ambiental del mantenimiento

- **Métodos de Asignación de Pesos**:
  - **Pesos Recomendados**: Basados en análisis AHP+ODS, ideal para evaluaciones estándar
  - **Ajuste Manual**: Personalización directa de pesos según necesidades específicas
  - **Comparación por Pares**: Cálculo mediante matriz de comparación AHP con verificación de consistencia

- **Gestión de Configuraciones de pesos**:
  - Guardado y carga de configuraciones personalizadas
  - Comparación entre diferentes configuraciones
  - Exportación de resultados con detalles de configuración

- **Visualización y Análisis**:
  - Gráficos radar para métricas individuales y globales
  - Tablas detalladas de resultados
  - Exportación completa a Excel

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

## Guía de Uso

### 1. Inicio Rápido

1. Iniciar la aplicación:
```bash
streamlit run app.py
```

2. Acceder al dashboard:
   - URL local: http://localhost:8501
   - URL de red: http://[TU_IP]:8501

### 2. Flujo de Trabajo

#### A. Configuración de Pesos
1. Seleccionar método de asignación:
   - **Pesos Recomendados**: Ideal para evaluaciones estándar
   - **Ajuste Manual**: Para personalización directa
   - **Comparación por Pares**: Para análisis detallado AHP

2. Guardar configuraciones personalizadas:
   - Asignar nombre descriptivo
   - Verificar consistencia (en caso de AHP)
   - Aplicar a dispositivos existentes o futuros

#### B. Ingreso de Dispositivos
1. **Método Manual**:
   - Completar formulario con datos del dispositivo
   - Verificar valores y unidades
   - Añadir al sistema

2. **Importación Masiva**:
   - Descargar plantilla Excel/CSV/JSON
   - Completar datos manteniendo nombres de columnas
   - Importar y validar
   - Añadir dispositivos individualmente o en grupo

#### C. Análisis y Resultados
1. Calcular índice de sostenibilidad
2. Revisar resultados individuales y globales
3. Exportar resultados si es necesario

### 3. Importación de Dispositivos

#### Plantilla de Importación
La plantilla incluye los siguientes campos (nombres exactos requeridos):

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

#### Consideraciones Importantes sobre importaciones
> **Nota:** No modifiques los nombres de las columnas en la plantilla. El sistema requiere los nombres exactos.
- **Unidades**: Respetar las unidades especificadas para cada campo
- **Validación**: El sistema valida automáticamente los datos
- **Cancelación**: Puedes cancelar la importación en cualquier momento

### 4. Método de Cálculo

El índice de sostenibilidad se calcula en dos pasos:

1. **Normalización de Métricas**:
   - Cada métrica se normaliza a una escala de 0-10
   - Valores más altos indican mejor sostenibilidad
   - Se consideran rangos de referencia para cada métrica

2. **Cálculo del Índice**:
   - Combinación ponderada de métricas normalizadas
   - Pesos asignados según el método seleccionado
   - Resultado final en escala de 0-10

> **Interpretación:** Un índice cercano a 10 indica un dispositivo altamente sostenible; valores bajos sugieren áreas de mejora.

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

## Contacto

Juan Camilo Pacheco - jc.pacheco@uniandes.edu.co
Natalia Andrea Ricaurte - na.ricaurtep@uniandes.edu.co
Laura Valentina Lara - lv.larad@uniandes.edu.co

Link del proyecto: https://github.com/natalia-ricaurte/IoT

### Flujo de trabajo del dashboard

1. **Configuración de pesos**
   - Selecciona el método de asignación de pesos (recomendados, manual o calculados)
   - Los pesos activos al momento de añadir un dispositivo serán los que se usen para su cálculo
   - El nombre de la configuración utilizada se guarda y se muestra en los resultados

2. **Ingreso de dispositivos**
   - Completa el formulario manualmente o importa una lista usando la plantilla
   - La plantilla incluye una hoja de ayuda con la descripción y unidad de cada campo
   - Sube el archivo en formato Excel, CSV o JSON
   - Revisa los datos antes de añadirlos al sistema
   - Añade los dispositivos individualmente o todos juntos

3. **Gestión de dispositivos**
   - Consulta los detalles completos de cada dispositivo
   - Elimina dispositivos según sea necesario
   - Descarga la lista actual de dispositivos en formato Excel, CSV o JSON
   - Los archivos exportados mantienen los nombres de columnas de la plantilla para facilitar su reutilización

4. **Cálculo y análisis**
   - Calcula el índice de sostenibilidad para ver resultados individuales y globales
   - Consulta los detalles del sistema y las métricas individuales
   - Exporta los resultados completos a Excel o la lista de dispositivos en varios formatos

### Exportación de datos

El dashboard ofrece dos tipos de exportación:

1. **Resultados completos**
   - Formato: Excel (.xlsx)
   - Incluye:
     - Resumen general con índice global
     - Tabla de pesos utilizados
     - Lista de dispositivos y sus índices
     - Hojas de detalle para cada dispositivo
     - Gráficos radar y tablas de datos

2. **Lista de dispositivos**
   - Formatos disponibles: Excel (.xlsx), CSV (.csv), JSON (.json)
   - Contiene los datos de entrada de los dispositivos
   - Mantiene los nombres de columnas de la plantilla para facilitar su reutilización
   - Ideal para guardar y compartir la base de dispositivos

### Importación de dispositivos

1. **Formato de archivo**
   - Excel (.xlsx), CSV (.csv) o JSON (.json)
   - Debe seguir la estructura de la plantilla
   - Los nombres de las columnas deben coincidir con los de la plantilla

2. **Proceso de importación**
   - Sube el archivo usando el botón "Importar dispositivos"
   - Revisa los datos en la tabla de previsualización
   - Añade los dispositivos individualmente o todos juntos
   - Los dispositivos importados se añaden a la lista actual

3. **Compatibilidad**
   - Los archivos exportados son compatibles con la importación
   - Se mantienen los nombres de columnas de la plantilla
   - Facilita la reutilización y edición de la base de dispositivos