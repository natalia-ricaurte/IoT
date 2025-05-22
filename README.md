
# Sustainability Evaluation for IoT Devices

This undergraduate thesis project, developed by Juan Camilo Pacheco, Natalia Andrea Ricaurte, and Laura Valentina Lara, implements an interactive system for assessing the environmental sustainability of IoT systems, with a focus on the operational phase of devices.

Through a dashboard built with Python and Streamlit, the system evaluates the environmental impact of each IoT device by considering factors such as energy consumption, electronic waste generation, use of renewable energy, operational efficiency, and data processing (including edge computing).

The system allows users to assign custom weights to sustainability metrics using a flexible approach that combines qualitative criteria, alignment with the Sustainable Development Goals (SDGs), and the AHP methodology to structure the recommended weights.


## Table of Contents

- [Key Features](#key-features)
- [Installation](#installation)
- [User Guide](#user-guide)
  - [1. Weight Configuration](#1-weight-configuration)
  - [2. Device Management](#2-device-management)
  - [3. Device Selection](#3-device-selection)
  - [4. Calculation and Results](#4-calculation-and-results)
- [Data Export](#data-export)
- [Project Structure](#project-structure)
- [Contact](#contact)
- [Opportunities for Improvement](#opportunities-for-improvement)
- [Model Integrity Note](#model-integrity-note)

## Key Features

### Environmental Assessment
- Eight key metrics:
  - Energy Consumption (EC)
  - Carbon Footprint (CF)
  - Electronic Waste (EW)
  - Renewable Energy Use (RE)
  - Energy Efficiency (EE)
  - Product Durability (PD)
  - Recyclability (RC)
  - Maintenance (MT)

- Metric normalization and weighting:
  - Configurable weighting via three methods:
    - Recommended Weights (based on SDGs and environmental impact)
    - Manual Adjustment
    - Calculate New Weights (pairwise comparison matrix)

### Visualization and Analysis
- Interactive dashboard featuring:
  - Radar charts (individual and global)
  - Detailed results tables
  - Full Excel export with traceability of included devices

### Device Management
- Manual entry or bulk import from Excel, CSV, or JSON
- Automatic data validation
- Storage and retrieval of devices
- Flexible device selection for global index calculation

### Custom Configuration
- Save and load custom weight configurations
- Compare between configurations
- Apply configurations to new or existing devices

## Installation

1. Clone the repository:
```bash
git clone https://github.com/natalia-ricaurte/IoT
cd IoT
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## User Guide

> **Note:** For detailed instructions, please refer to the in-dashboard guide, which includes step-by-step explanations and key warnings during analysis.

### 1. Weight Configuration
- Choose between recommended weights, manual adjustment, or pairwise comparison.
- You can save custom configurations with a descriptive name.
- The active configuration is applied at the time of adding a new device.

### 2. Device Management
- Manually enter data or import from file.
- Supported formats: .xlsx, .csv, .json
- Files must follow the structure and exact column names of the template.

#### Import Template
| Column                   | Description                                                     |
|--------------------------|-----------------------------------------------------------------|
| nombre                   | Descriptive name of the IoT device                              |
| potencia_w               | Power consumption in watts (W)                                  |
| horas_uso_diario         | Hours of daily operation                                        |
| dias_uso_anio            | Days of operation per year                                      |
| peso_kg                  | Total device weight in kilograms                                |
| vida_util_anios          | Expected lifespan in years                                      |
| energia_renovable_pct    | Percentage of energy from renewable sources                     |
| funcionalidad_1_10       | Device functionality rating (scale 1–10)                        |
| reciclabilidad_pct       | Percentage of recyclable materials                             |
| baterias_vida_util       | Number of batteries required during the device's lifespan       |
| peso_bateria_g           | Weight of each battery in grams                                 |
| mantenimientos           | Number of required maintenance operations                       |
| componentes_reemplazados | Number of components replaced                                   |
| peso_componente_g        | Average weight of each replaced component in grams              |
| peso_nuevo_g             | Total weight when new (grams)                                   |
| peso_final_g             | Final weight after usage (grams)                                |

> Note: Do not modify column names. The system automatically validates the data and requires exact matches.

### 3. Device Selection
- Use the "Include in calculation" checkboxes to select devices for the global index.
- Selection state is preserved and reflected in all exports.
- Use "Select All" and "Deselect All" buttons for quick management.

### 4. Calculation and Results
- Compute the sustainability index (individual and global).
- Review charts and detailed metrics.
- Export results to Excel with full traceability.

## Data Export

### Full Results (.xlsx)
Includes:
- Global index and device count in the filename
- Summary sheet with global index and charts
- Device sheet with input data and inclusion status
- Individual detail sheets per device
- Applied weight table
- Normalized metrics and radar charts

### Device List
Available formats: .xlsx, .csv, .json
- Option to export only selected devices
- Includes input data and selection status
- Compatible with future imports
- Filename includes device count and date

## Project Structure

```
IoT/
├── app.py                 # Main application (Streamlit)
├── model.py               # Sustainability index calculation
├── weights.py             # Weighting methods
├── components/            # UI components (forms, charts, weights_ui)
├── services/              # Auxiliary services (import_service, export, ahp_service)
├── utils/                 # Constants, state management, helpers
└── requirements.txt       # Project dependencies
```

## Contact

- Juan Camilo Pacheco — jc.pacheco@uniandes.edu.co  
- Natalia Andrea Ricaurte — na.ricaurtep@uniandes.edu.co  
- Laura Valentina Lara — lv.larad@uniandes.edu.co  
- Repository: https://github.com/natalia-ricaurte/IoT

## Opportunities for Improvement

- **User Accounts:** Add authentication and account management to persist configurations and device data across sessions.
- **Importing Exported Results:** Allow re-importing exported results to compare and analyze historical data.
- **Temporal Analysis:** Enable tracking of sustainability index changes over time.
- **Device Grouping:** Allow users to create groups based on type, location, or function and compute sustainability indexes per group.
- **API Integration:** Connect to APIs from energy providers and IoT services to retrieve real-time data.
- **Specialized Export Formats:** Support exporting reports formatted for corporate sustainability reporting or environmental certifications.
- **Import format validation** validate column names and data types
- **Device management** allow user to edit device data

## Model Integrity Note

The system maintains all sustainability metrics as an integral set for the following reasons:

### Model Integrity
- The model is designed for holistic sustainability evaluation.
- Metrics are interrelated and complementary.
- Omitting metrics could lead to incomplete or biased assessments.

### Scientific Validity
- The AHP+SDG model was developed considering all metrics.
- Weights were calculated based on each metric’s relative importance.
- The pairwise comparison matrix was built with all metrics in mind.

### Project Purpose
- The goal is to provide a complete sustainability evaluation.
- Allowing metric exclusion could encourage cherry-picking.
- This may result in less rigorous or biased assessments.

### Evaluation Consistency
- Keeping all metrics ensures consistent evaluation across devices.
- This enables fair and objective comparison.

### SDG Alignment
- The model aligns with the Sustainable Development Goals.
- Omitting metrics may prevent the evaluation from fully reflecting SDG impacts.
