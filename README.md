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

## Guía Rápida

1. **Definir Pesos**:
   - Seleccione el método de asignación de pesos
   - Ajuste los pesos según sus necesidades
   - Guarde configuraciones personalizadas

2. **Ingresar Dispositivos**:
   - Complete el formulario con los datos del dispositivo
   - Añada tantos dispositivos como necesite

3. **Calcular Resultados**:
   - Presione "Calcular Índice de Sostenibilidad"
   - Revise los resultados individuales y globales
   - Exporte los resultados a Excel si lo desea

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