# Evaluación de Sostenibilidad para Dispositivos IoT

Este proyecto de grado, desarrollado por Juan Camilo Pacheco, Natalia Andrea Ricaurte y Laura Valentina Lara, implementa un sistema interactivo de medición de sostenibilidad ambiental para sistemas IoT, con énfasis en la fase operativa de los dispositivos.

A través de un dashboard desarrollado en Python y Streamlit, el sistema permite evaluar el impacto ambiental de cada dispositivo IoT considerando factores como consumo energético, generación de residuos electrónicos, uso de energías renovables, eficiencia operativa y procesamiento de datos (incluyendo edge computing).

El sistema permite asignar pesos personalizados a las métricas de sostenibilidad mediante un enfoque flexible, combinando criterios cualitativos, alineación con los Objetivos de Desarrollo Sostenible (ODS), y la metodología AHP para estructurar los pesos recomendados.

## Características Principales

### Evaluación Ambiental
- Ocho métricas clave:
  - Consumo de Energía (CE)
  - Huella de Carbono (HC)
  - Residuos Electrónicos (EW)
  - Energía Renovable (ER)
  - Eficiencia Energética (EE)
  - Durabilidad del Producto (DP)
  - Reciclabilidad (RC)
  - Mantenimiento (IM)

- Normalización y ponderación de pesos:
  - Ponderación configurable mediante tres métodos:
    - Pesos recomendados (basados en ODS e impacto ambiental)
    - Ajuste manual
    - Calcular nuevos pesos (matriz de comparacion por pares)

### Visualización y Análisis
- Dashboard interactivo con:
  - Gráficos radar individuales y globales
  - Tablas detalladas de resultados
  - Exportación completa a Excel

### Gestión de Dispositivos
- Ingreso manual o importación masiva desde Excel, CSV o JSON
- Validación automática de datos
- Almacenamiento y recuperación de dispositivos

### Configuración Personalizada
- Guardado y carga de configuraciones de pesos
- Comparación entre configuraciones
- Aplicación de configuraciones a dispositivos nuevos o existentes

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/natalia-ricaurte/IoT
cd IoT
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
streamlit run app.py
```

## Guía de Uso

> **Nota:** Para un uso detallado, consulta la guía integrada dentro del dashboard, que incluye explicaciones paso a paso y advertencias clave durante el análisis.

### 1. Configuración de Pesos
- Elige entre pesos recomendados, ajuste manual o cálculo a través de comparación por pares.
- Puedes guardar configuraciones personalizadas con nombre.
- La configuración activa se aplica al momento de añadir un nuevo dispositivo.

### 2. Gestión de Dispositivos
- Ingresa datos manualmente o importa desde archivo.
- Formatos admitidos: .xlsx, .csv, .json
- Los archivos deben seguir la estructura y nombres exactos de la plantilla.

#### Plantilla de Importación
| Columna                  | Descripción                                                          |
|--------------------------|----------------------------------------------------------------------|
| nombre                   | Nombre del dispositivo                                               |
| potencia_w               | Potencia en vatios (W)                                               |
| horas_uso_diario         | Horas diarias de operación                                           |
| dias_uso_anio            | Días de uso por año                                                  |
| peso_kg                  | Peso total del dispositivo                                           |
| vida_util_anios          | Años de vida útil estimada                                           |
| energia_renovable_pct    | Porcentaje de energía limpia utilizada                               |
| funcionalidad_1_10       | Funcionalidad del dispositivo (escala 1-10)                          |
| reciclabilidad_pct       | Porcentaje de reciclabilidad                                         |
| baterias_vida_util       | Número total de baterías usadas durante su vida útil                 |
| peso_bateria_g           | Peso de cada batería en gramos                                       |
| mantenimientos           | Cantidad de mantenimientos requeridos                               |
| componentes_reemplazados | Número de componentes reemplazados                                   |
| peso_componente_g        | Peso promedio de cada componente reemplazado                         |
| peso_nuevo_g             | Peso inicial del dispositivo en gramos                              |
| peso_final_g             | Peso del dispositivo después del uso                                 |

> Nota: No modifiques los nombres de columna. El sistema valida los datos automáticamente y requiere coincidencia exacta.

### 3. Selección de Dispositivos
- Puedes seleccionar o deseleccionar dispositivos para el cálculo global.
- La lista exportada de dispositivos incluye todos los dispositivos añadidos, independientemente de su estado de selección.

### 4. Cálculo y Resultados
- Calcula el índice de sostenibilidad individual o global.
- Revisa gráficos y métricas detalladas.
- Exporta resultados en Excel.

## Exportación de Datos

### Resultados Completos (.xlsx)
Incluye:
- Índice global
- Tabla de pesos aplicados
- Detalles por dispositivo
- Gráficos y métricas normalizadas

### Lista de Dispositivos
Formatos disponibles: .xlsx, .csv, .json
- Contiene datos de entrada
- Compatible con futuras importaciones
- Incluye todos los dispositivos añadidos, incluso los no seleccionados para el cálculo global.

## Estructura del Proyecto

```
IoT/
├── app.py                 # Aplicación principal (Streamlit)
├── modelo.py              # Cálculo de sostenibilidad
├── pesos.py               # Métodos de ponderación
├── componentes/           # Componentes UI (formularios, gráficos, etc.)
├── servicios/             # Servicios auxiliares (cálculos, exportación)
├── utilidades/            # Constantes, estado, manejo de datos
└── requirements.txt       # Dependencias del proyecto
```

## Contacto

- Juan Camilo Pacheco — jc.pacheco@uniandes.edu.co  
- Natalia Andrea Ricaurte — na.ricaurtep@uniandes.edu.co  
- Laura Valentina Lara — lv.larad@uniandes.edu.co  
- Repositorio: https://github.com/natalia-ricaurte/IoT

## Oportunidades de Mejora

- **Importación de Resultados Exportados**: Implementar una funcionalidad que permita a los usuarios importar resultados exportados anteriormente, facilitando la comparación y el análisis de datos históricos.
