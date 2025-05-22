# Evaluación de Sostenibilidad para Dispositivos IoT

Este proyecto de grado, desarrollado por Juan Camilo Pacheco, Natalia Andrea Ricaurte y Laura Valentina Lara, implementa un sistema interactivo de medición de sostenibilidad ambiental para sistemas IoT, con énfasis en la fase operativa de los dispositivos.

A través de un dashboard desarrollado en Python y Streamlit, el sistema permite evaluar el impacto ambiental de cada dispositivo IoT considerando factores como consumo energético, generación de residuos electrónicos, uso de energías renovables, eficiencia operativa y procesamiento de datos (incluyendo edge computing).

El sistema permite asignar pesos personalizados a las métricas de sostenibilidad mediante un enfoque flexible, combinando criterios cualitativos, alineación con los Objetivos de Desarrollo Sostenible (ODS), y la metodología AHP para estructurar los pesos recomendados.

## Tabla de Contenidos

- [Características Principales](#caracteristicas-principales)
- [Instalación](#instalacion)
- [Guía de Uso](#guia-de-uso)
  - [1. Configuración de Pesos](#1-configuracion-de-pesos)
  - [2. Gestión de Dispositivos](#2-gestion-de-dispositivos)
  - [3. Selección de Dispositivos](#3-seleccion-de-dispositivos)
  - [4. Cálculo y Resultados](#4-calculo-y-resultados)
- [Exportación de Datos](#exportacion-de-datos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contacto](#contacto)
- [Oportunidades de Mejora](#oportunidades-de-mejora)
- [Nota sobre la Integridad del Modelo](#nota-sobre-la-integridad-del-modelo)


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
  - Exportación completa a Excel con trazabilidad de dispositivos incluidos

### Gestión de Dispositivos
- Ingreso manual o importación masiva desde Excel, CSV o JSON
- Validación automática de datos
- Almacenamiento y recuperación de dispositivos
- Selección flexible de dispositivos para el cálculo global

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
- Usa los checkboxes "Incluir en cálculo" para seleccionar qué dispositivos se incluirán en el cálculo global.
- El estado de selección se mantiene y se refleja en todas las exportaciones.
- Puedes usar los botones "Seleccionar Todos" y "Deseleccionar Todos" para una gestión rápida.

### 4. Cálculo y Resultados
- Calcula el índice de sostenibilidad individual o global.
- Revisa gráficos y métricas detalladas.
- Exporta resultados en Excel con información completa de trazabilidad.

## Exportación de Datos

### Resultados Completos (.xlsx)
Incluye:
- Índice global y número de dispositivos incluidos en el nombre del archivo
- Hoja de resumen con el índice global y gráficos
- Hoja de dispositivos con todos los datos y su estado de inclusión en el cálculo
- Hojas de detalle individuales para cada dispositivo
- Tabla de pesos aplicados
- Gráficos y métricas normalizadas

### Lista de Dispositivos
Formatos disponibles: .xlsx, .csv, .json
- Opción para incluir solo dispositivos seleccionados para el cálculo global
- Contiene datos de entrada y estado de selección
- Compatible con futuras importaciones
- Nombre del archivo incluye el número de dispositivos y fecha

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

- **Gestión de Cuentas**: Implementar un sistema de autenticación y gestión de cuentas que permita a los usuarios guardar su progreso, configuraciones y dispositivos, asegurando la persistencia de los datos entre sesiones y facilitando la recuperación de información en caso de cierre inesperado del dashboard.
- **Importación de Resultados Exportados**: Implementar una funcionalidad que permita a los usuarios importar resultados exportados anteriormente, facilitando la comparación y el análisis de datos históricos.
- **Análisis Temporal**: Implementar seguimiento de cambios en el índice de sostenibilidad a lo largo del tiempo.
- **Agrupación de Dispositivos**: Permitir crear grupos de dispositivos basados en diferentes criterios (tipo, ubicación, función, etc.) y calcular índices de sostenibilidad por grupo, facilitando el análisis comparativo entre diferentes categorías de dispositivos IoT.
- **Integración con APIs**: Permitir la conexión con APIs de proveedores de energía y servicios IoT para obtener datos en tiempo real sobre consumo energético y otros parámetros relevantes.
- **Exportación a Formatos Especializados**: Añadir soporte para exportar resultados en formatos específicos para reportes de sostenibilidad corporativos o certificaciones ambientales.
- **Validación del formato de importación**: validar nombres de columnas y tipos de datos
- **Gestión de dispositivos**: permitir al usuario editar los datos de los dispositivos

## Nota sobre la Integridad del Modelo

El sistema mantiene todas las métricas de sostenibilidad como un conjunto integral por las siguientes razones:

### Integridad del Modelo
- El modelo fue diseñado para evaluar la sostenibilidad de manera holística
- Las métricas están interrelacionadas y se complementan entre sí
- La exclusión de métricas podría llevar a evaluaciones incompletas o sesgadas

### Validez Científica
- El modelo AHP+ODS fue desarrollado considerando todas las métricas
- Los pesos fueron calculados considerando la importancia relativa de cada métrica
- La matriz de comparación por pares se construyó con todas las métricas en mente

### Propósito del Proyecto
- El objetivo es proporcionar una evaluación completa de la sostenibilidad
- Permitir la selección de métricas podría llevar a que los usuarios elijan solo las métricas que les convienen
- Esto podría resultar en evaluaciones menos rigurosas o sesgadas

### Consistencia en la Evaluación
- Al mantener todas las métricas, aseguramos que todos los dispositivos sean evaluados con los mismos criterios
- Esto permite comparaciones más justas y objetivas entre diferentes dispositivos

### Alineación con ODS
- El modelo está alineado con los Objetivos de Desarrollo Sostenible
- La exclusión de métricas podría resultar en una evaluación que no refleje adecuadamente el impacto en los ODS

