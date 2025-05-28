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
- [Data Validation and Ranges](#data-validation-and-ranges)
- [Understanding Results](#understanding-results)
- [Default Weights](#default-weights)
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
python -m streamlit run app.py
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
|:------------------------|:---------------------------------------------------------------|
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

## Data Validation and Ranges

The system validates all input data according to the following ranges and types:

### Input Fields and Valid Ranges
| Field | Type | Valid Range | Description |
|:------|:-----|:------------|:------------|
| Power (W) | Float | > 0 | Device power consumption in watts |
| Daily Usage (hours) | Float | 0-24 | Hours of operation per day |
| Annual Usage (days) | Integer | 0-365 | Days of operation per year |
| Weight (kg) | Float | > 0 | Total device weight in kilograms |
| Lifespan (years) | Integer | > 0 | Expected device lifespan |
| Renewable Energy (%) | Float | 0-100 | Percentage of renewable energy used |
| Functionality (1-10) | Float | 1-10 | Device functionality rating |
| Recyclability (%) | Float | 0-100 | Percentage of recyclable materials |
| Batteries | Integer | ≥ 0 | Number of batteries used |
| Battery Weight (g) | Float | ≥ 0 | Weight of each battery |
| Maintenance | Integer | ≥ 0 | Number of maintenance operations |
| Replaced Components | Integer | ≥ 0 | Number of components replaced |
| Component Weight (g) | Float | ≥ 0 | Weight of each component |
| Initial Weight (g) | Float | > 0 | Device weight when new |
| Final Weight (g) | Float | > 0 | Device weight after use |

### Validation Rules
- All numeric fields must be positive numbers
- Percentages must be between 0 and 100
- Functionality must be between 1 and 10
- Time values must be within logical ranges (e.g., daily hours ≤ 24)
- Weights must be positive and final weight must be less than or equal to initial weight

## Understanding Results

### Normalization Scale
All metrics are normalized to a 0-10 scale where:
- 10 represents the best possible performance
- 0 represents the worst possible performance

### Color Coding in Results
Results are color-coded for easy interpretation:
- 🟢 Green (8-10): High performance
- 🟡 Yellow (5-7.99): Moderate performance
- 🔴 Red (< 5): Low performance

### Global Index Calculation
The global sustainability index is calculated as:
1. Each metric is normalized to 0-10 scale
2. Normalized values are weighted according to the selected configuration
3. The global index is the weighted sum of all metrics
4. For multiple devices, the global index is the average of individual indices

### Metric Interpretation
All metrics follow the principle that higher values indicate better performance:
- Energy Consumption (EC): Higher values indicate better energy management
- Carbon Footprint (CF): Higher values indicate better carbon management
- Electronic Waste (EW): Higher values indicate better waste management
- Renewable Energy (RE): Higher values indicate better renewable energy usage
- Energy Efficiency (EE): Higher values indicate better efficiency
- Product Durability (PD): Higher values indicate better durability
- Recyclability (RC): Higher values indicate better recyclability
- Maintenance (MT): Higher values indicate better maintenance management

## Default Weights

### Recommended Weights
The system provides recommended weights based on a structured prioritization method that combines:
1. Alignment with Sustainable Development Goals (SDGs)
2. Qualitative assessment of environmental impact

| Metric | Weight | Description |
|:-------|:-------|:------------|
| Energy Consumption (EC) | 0.3267 | Highest weight due to direct environmental impact |
| Carbon Footprint (CF) | 0.1992 | High weight for climate change impact |
| Renewable Energy (RE) | 0.1992 | High weight for sustainable energy use |
| Electronic Waste (EW) | 0.0811 | Medium weight for resource management |
| Energy Efficiency (EE) | 0.0811 | Medium weight for operational efficiency |
| Product Durability (PD) | 0.0477 | Lower weight for product lifecycle |
| Recyclability (RC) | 0.0477 | Lower weight for end-of-life management |
| Maintenance (MT) | 0.0174 | Lowest weight for operational aspects |

### Weight Calculation Method
The recommended weights were derived using:
1. A structured prioritization method based on environmental relevance
2. Saaty's pairwise comparison technique
3. Integration of SDG alignment and environmental impact assessment
4. Validation through consistency ratio (CR = 0.037, below the 0.10 threshold)

### Custom Weight Configuration
Users can:
- Use the recommended weights
- Manually adjust weights (system will normalize to sum 1)
- Calculate new weights using pairwise comparison
- Save and load custom weight configurations

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
├── requirements.txt       # Project dependencies
└── readme.md              # This file

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
- **Data validation** validate data before calculating the index for manual inputs
- **Device management** allow user to edit device data
- **Data processong and Edge Computing**: integrate factor  of Edge Computing for specific contexts
- **Recommendations**: add recommendations for results obtained on exported files
- **Lenguage modifications**: add feature to change UI language "English" and "Español"

## Model Integrity Note

The system maintains all sustainability metrics as an integral set for the following reasons:

### Model Integrity
- The model is designed for holistic sustainability evaluation.
- Metrics are interrelated and complementary.
- Omitting metrics could lead to incomplete or biased assessments.

### Scientific Validity
- The AHP+SDG model was developed considering all metrics.
- Weights were calculated based on each metric's relative importance.
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
