# Evaluación de Sostenibilidad para Dispositivos IoT

Este proyecto de grado, desarrollado por Juan Camilo Pacheco, Natalia Andrea Ricaurte y Laura Valentina Lara, implementa un sistema interactivo para evaluar la sostenibilidad ambiental de sistemas IoT, con énfasis en la fase operativa de los dispositivos.

A través de un dashboard desarrollado en Python y Streamlit, el sistema evalúa el impacto ambiental de cada dispositivo IoT considerando factores como consumo energético, generación de residuos electrónicos, uso de energías renovables, eficiencia operativa y procesamiento de datos (incluyendo edge computing).

El sistema permite asignar pesos personalizados a las métricas de sostenibilidad mediante un enfoque flexible que combina criterios cualitativos, alineación con los Objetivos de Desarrollo Sostenible (ODS), y la metodología AHP para estructurar los pesos recomendados.

## Tabla de Contenidos

- [Características Principales](#caracteristicas-principales)
- [Instalación](#instalacion)
- [Guía de Uso](#guia-de-uso)
  - [1. Configuración de Pesos](#1-configuracion-de-pesos)
  - [2. Gestión de Dispositivos](#2-gestion-de-dispositivos)
  - [3. Selección de Dispositivos](#3-seleccion-de-dispositivos)
  - [4. Cálculo y Resultados](#4-calculo-y-resultados)
- [Validación de Datos y Rangos](#validacion-de-datos-y-rangos)
- [Comprensión de Resultados](#comprension-de-resultados)
- [Pesos por Defecto](#pesos-por-defecto)
- [Exportación de Datos](#exportacion-de-datos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Contacto](#contacto)
- [Oportunidades de Mejora](#oportunidades-de-mejora)
- [Nota sobre la Integridad del Modelo](#nota-sobre-la-integridad-del-modelo)

## Características Principales

### Evaluación Ambiental
- Ocho métricas clave:
  - Consumo de Energía (EC)
  - Huella de Carbono (CF)
  - Residuos Electrónicos (EW)
  - Energía Renovable (RE)
  - Eficiencia Energética (EE)
  - Durabilidad del Producto (PD)
  - Reciclabilidad (RC)
  - Mantenimiento (MT)

- Normalización y ponderación de métricas:
  - Ponderación configurable mediante tres métodos:
    - Pesos Recomendados (basados en ODS e impacto ambiental)
    - Ajuste Manual
    - Calcular Nuevos Pesos (matriz de comparación por pares)

### Visualización y Análisis
- Dashboard interactivo con:
  - Gráficos radar (individuales y globales)
  - Tablas detalladas de resultados
  - Exportación completa a Excel con trazabilidad de dispositivos incluidos

### Gestión de Dispositivos
- Ingreso manual o importación masiva desde Excel, CSV o JSON
- Validación automática de datos
- Almacenamiento y recuperación de dispositivos
- Selección flexible de dispositivos para el cálculo del índice global

### Configuración Personalizada
- Guardado y carga de configuraciones de pesos personalizadas
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
python -m streamlit run app.py
```

## Guía de Uso

> **Nota:** Para instrucciones detalladas, consulta la guía integrada en el dashboard, que incluye explicaciones paso a paso y advertencias clave durante el análisis.

### 1. Configuración de Pesos
- Elige entre pesos recomendados, ajuste manual o comparación por pares.
- Puedes guardar configuraciones personalizadas con un nombre descriptivo.
- La configuración activa se aplica al momento de añadir un nuevo dispositivo.

### 2. Gestión de Dispositivos
- Ingresa datos manualmente o importa desde archivo.
- Formatos admitidos: .xlsx, .csv, .json
- Los archivos deben seguir la estructura y nombres exactos de la plantilla.

#### Plantilla de Importación
| Columna                  | Descripción                                                          |
|:------------------------|:---------------------------------------------------------------------|
| nombre                   | Nombre descriptivo del dispositivo IoT                               |
| potencia_w               | Consumo de potencia en vatios (W)                                    |
| horas_uso_diario         | Horas de operación diaria                                            |
| dias_uso_anio            | Días de operación por año                                            |
| peso_kg                  | Peso total del dispositivo en kilogramos                             |
| vida_util_anios          | Vida útil esperada en años                                           |
| energia_renovable_pct    | Porcentaje de energía de fuentes renovables                          |
| funcionalidad_1_10       | Calificación de funcionalidad del dispositivo (escala 1-10)          |
| reciclabilidad_pct       | Porcentaje de materiales reciclables                                |
| baterias_vida_util       | Número de baterías requeridas durante la vida útil del dispositivo   |
| peso_bateria_g           | Peso de cada batería en gramos                                       |
| mantenimientos           | Número de operaciones de mantenimiento requeridas                    |
| componentes_reemplazados | Número de componentes reemplazados                                   |
| peso_componente_g        | Peso promedio de cada componente reemplazado en gramos               |
| peso_nuevo_g             | Peso total cuando es nuevo (gramos)                                  |
| peso_final_g             | Peso final después del uso (gramos)                                  |

> Nota: No modifiques los nombres de columna. El sistema valida los datos automáticamente y requiere coincidencia exacta.

### 3. Selección de Dispositivos
- Usa los checkboxes "Incluir en cálculo" para seleccionar dispositivos para el índice global.
- El estado de selección se mantiene y se refleja en todas las exportaciones.
- Usa los botones "Seleccionar Todos" y "Deseleccionar Todos" para una gestión rápida.

### 4. Cálculo y Resultados
- Calcula el índice de sostenibilidad (individual y global).
- Revisa gráficos y métricas detalladas.
- Exporta resultados a Excel con trazabilidad completa.

## Validación de Datos y Rangos

El sistema valida todos los datos de entrada según los siguientes rangos y tipos:

### Campos de Entrada y Rangos Válidos
| Campo | Tipo | Rango Válido | Descripción |
|:------|:-----|:-------------|:------------|
| Potencia (W) | Float | > 0 | Consumo de potencia del dispositivo en vatios |
| Uso Diario (horas) | Float | 0-24 | Horas de operación por día |
| Uso Anual (días) | Integer | 0-365 | Días de operación por año |
| Peso (kg) | Float | > 0 | Peso total del dispositivo en kilogramos |
| Vida Útil (años) | Integer | > 0 | Vida útil esperada del dispositivo |
| Energía Renovable (%) | Float | 0-100 | Porcentaje de energía renovable utilizada |
| Funcionalidad (1-10) | Float | 1-10 | Calificación de funcionalidad del dispositivo |
| Reciclabilidad (%) | Float | 0-100 | Porcentaje de materiales reciclables |
| Baterías | Integer | ≥ 0 | Número de baterías utilizadas |
| Peso de Batería (g) | Float | ≥ 0 | Peso de cada batería |
| Mantenimiento | Integer | ≥ 0 | Número de operaciones de mantenimiento |
| Componentes Reemplazados | Integer | ≥ 0 | Número de componentes reemplazados |
| Peso de Componente (g) | Float | ≥ 0 | Peso de cada componente |
| Peso Inicial (g) | Float | > 0 | Peso del dispositivo cuando es nuevo |
| Peso Final (g) | Float | > 0 | Peso del dispositivo después del uso |

### Reglas de Validación
- Todos los campos numéricos deben ser números positivos
- Los porcentajes deben estar entre 0 y 100
- La funcionalidad debe estar entre 1 y 10
- Los valores de tiempo deben estar dentro de rangos lógicos (ej. horas diarias ≤ 24)
- Los pesos deben ser positivos y el peso final debe ser menor o igual al peso inicial

## Comprensión de Resultados

### Escala de Normalización
Todas las métricas se normalizan a una escala de 0-10 donde:
- 10 representa el mejor rendimiento posible
- 0 representa el peor rendimiento posible

### Codificación de Colores en Resultados
Los resultados se codifican por colores para facilitar la interpretación:
- 🟢 Verde (8-10): Alto rendimiento
- 🟡 Amarillo (5-7.99): Rendimiento moderado
- 🔴 Rojo (< 5): Bajo rendimiento

### Cálculo del Índice Global
El índice global de sostenibilidad se calcula como:
1. Cada métrica se normaliza a escala 0-10
2. Los valores normalizados se ponderan según la configuración seleccionada
3. El índice global es la suma ponderada de todas las métricas
4. Para múltiples dispositivos, el índice global es el promedio de los índices individuales

### Interpretación de Métricas
Todas las métricas siguen el principio de que valores más altos indican mejor rendimiento:
- Consumo de Energía (EC): Valores más altos indican mejor gestión energética
- Huella de Carbono (CF): Valores más altos indican mejor gestión de carbono
- Residuos Electrónicos (EW): Valores más altos indican mejor gestión de residuos
- Energía Renovable (RE): Valores más altos indican mejor uso de energía renovable
- Eficiencia Energética (EE): Valores más altos indican mejor eficiencia
- Durabilidad del Producto (PD): Valores más altos indican mejor durabilidad
- Reciclabilidad (RC): Valores más altos indican mejor reciclabilidad
- Mantenimiento (MT): Valores más altos indican mejor gestión del mantenimiento

## Pesos por Defecto

### Pesos Recomendados
El sistema proporciona pesos recomendados basados en un método de priorización estructurado que combina:
1. Alineación con los Objetivos de Desarrollo Sostenible (ODS)
2. Evaluación cualitativa del impacto ambiental

| Métrica | Peso | Descripción |
|:--------|:-----|:------------|
| Consumo de Energía (EC) | 0.3267 | Mayor peso debido al impacto ambiental directo |
| Huella de Carbono (CF) | 0.1992 | Alto peso por impacto en cambio climático |
| Energía Renovable (RE) | 0.1992 | Alto peso por uso de energía sostenible |
| Residuos Electrónicos (EW) | 0.0811 | Peso medio por gestión de recursos |
| Eficiencia Energética (EE) | 0.0811 | Peso medio por eficiencia operativa |
| Durabilidad del Producto (PD) | 0.0477 | Peso menor por ciclo de vida del producto |
| Reciclabilidad (RC) | 0.0477 | Peso menor por gestión de fin de vida |
| Mantenimiento (MT) | 0.0174 | Peso más bajo por aspectos operativos |

### Método de Cálculo de Pesos
Los pesos recomendados se derivaron usando:
1. Un método de priorización estructurado basado en relevancia ambiental
2. Técnica de comparación por pares de Saaty
3. Integración de alineación con ODS y evaluación de impacto ambiental
4. Validación a través de ratio de consistencia (CR = 0.037, por debajo del umbral de 0.10)

### Configuración de Pesos Personalizada
Los usuarios pueden:
- Usar los pesos recomendados
- Ajustar pesos manualmente (el sistema normalizará para sumar 1)
- Calcular nuevos pesos usando comparación por pares
- Guardar y cargar configuraciones de pesos personalizadas

## Exportación de Datos

### Resultados Completos (.xlsx)
Incluye:
- Índice global y número de dispositivos en el nombre del archivo
- Hoja de resumen con índice global y gráficos
- Hoja de dispositivos con datos de entrada y estado de inclusión
- Hojas de detalle individuales por dispositivo
- Tabla de pesos aplicados
- Métricas normalizadas y gráficos radar

### Lista de Dispositivos
Formatos disponibles: .xlsx, .csv, .json
- Opción para exportar solo dispositivos seleccionados
- Incluye datos de entrada y estado de selección
- Compatible con futuras importaciones
- Nombre del archivo incluye número de dispositivos y fecha

## Estructura del Proyecto

```
IoT/
├── app.py                 # Aplicación principal (Streamlit)
├── model.py               # Cálculo del índice de sostenibilidad
├── weights.py             # Métodos de ponderación
├── components/            # Componentes UI (formularios, gráficos, weights_ui)
├── services/              # Servicios auxiliares (import_service, export, ahp_service)
├── utils/                 # Constantes, gestión de estado, helpers
├── requirements.txt       # Dependencias del proyecto
└── readme.md              # Este archivo
```

## Contacto

- Juan Camilo Pacheco — jc.pacheco@uniandes.edu.co  
- Natalia Andrea Ricaurte — na.ricaurtep@uniandes.edu.co  
- Laura Valentina Lara — lv.larad@uniandes.edu.co  
- Repositorio: https://github.com/natalia-ricaurte/IoT

## Oportunidades de Mejora

- **Gestión de Cuentas**: Añadir autenticación y gestión de cuentas para persistir configuraciones y datos de dispositivos entre sesiones.
- **Importación de Resultados Exportados**: Permitir re-importar resultados exportados para comparar y analizar datos históricos.
- **Análisis Temporal**: Habilitar seguimiento de cambios en el índice de sostenibilidad a lo largo del tiempo.
- **Agrupación de Dispositivos**: Permitir a los usuarios crear grupos basados en tipo, ubicación o función y calcular índices de sostenibilidad por grupo.
- **Integración con APIs**: Conectar con APIs de proveedores de energía y servicios IoT para obtener datos en tiempo real.
- **Formatos de Exportación Especializados**: Soportar exportación de reportes formateados para reportes de sostenibilidad corporativos o certificaciones ambientales.
- **Validación del formato de importación**: validar nombres de columnas y tipos de datos
- **Validación de datos**: validar datos antes de calcular el índice para entradas manuales
- **Gestión de dispositivos**: permitir al usuario editar datos de dispositivos
- **Procesamiento de datos y Edge Computing**: integrar factor de Edge Computing para contextos específicos
- **Recomendaciones**: añadir recomendaciones para resultados obtenidos en archivos exportados
- **Modificaciones de idioma**: añadir función para cambiar el idioma de la interfaz entre "English" y "Español"

## Nota sobre la Integridad del Modelo

El sistema mantiene todas las métricas de sostenibilidad como un conjunto integral por las siguientes razones:

### Integridad del Modelo
- El modelo está diseñado para evaluación holística de sostenibilidad
- Las métricas están interrelacionadas y son complementarias
- Omitir métricas podría llevar a evaluaciones incompletas o sesgadas

### Validez Científica
- El modelo AHP+ODS fue desarrollado considerando todas las métricas
- Los pesos fueron calculados basados en la importancia relativa de cada métrica
- La matriz de comparación por pares se construyó considerando todas las métricas

### Propósito del Proyecto
- El objetivo es proporcionar una evaluación completa de sostenibilidad
- Permitir la exclusión de métricas podría fomentar la selección parcial
- Esto podría resultar en evaluaciones menos rigurosas o sesgadas

### Consistencia en la Evaluación
- Mantener todas las métricas asegura evaluación consistente entre dispositivos
- Esto permite comparaciones justas y objetivas

### Alineación con ODS
- El modelo está alineado con los Objetivos de Desarrollo Sostenible
- Omitir métricas podría impedir que la evaluación refleje completamente los impactos en los ODS

