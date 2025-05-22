import pandas as pd
import io
from utils.constants import IMPORT_COLUMN_DESCRIPTIONS, IMPORT_WARNING
import json

# Template for importing devices from CSV, Excel or JSON files

# Fixed mapping: template names -> internal names
TEMPLATE_COLUMNS_MAPPING = {
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

def read_devices_file(file):
    """
    Reads a devices file in CSV, Excel or JSON format and returns a DataFrame.
    Renames template columns to standard internal names.
    """
    name = file.name.lower()
    if name.endswith('.csv'):
        df = pd.read_csv(file)
    elif name.endswith('.xlsx'):
        df = pd.read_excel(file)
    elif name.endswith('.json'):
        df = pd.read_json(file)
    else:
        raise ValueError("Formato de archivo no soportado. Usa CSV, Excel o JSON.")
    # Rename columns using fixed mapping
    mapped_columns = {col: TEMPLATE_COLUMNS_MAPPING[col] for col in df.columns if col in TEMPLATE_COLUMNS_MAPPING}
    df = df.rename(columns=mapped_columns)
    return df

def to_float(val):
    if isinstance(val, str):
        val = val.replace(',', '.')
    return float(val)

def generate_excel_template():
    """
    Generates and returns a buffer with the devices template in Excel format (.xlsx).
    """
    columns = [
        "nombre",
        "potencia_w",
        "horas_uso_diario",
        "dias_uso_anio",
        "peso_kg",
        "vida_util_anios",
        "energia_renovable_pct",
        "funcionalidad_1_10",
        "reciclabilidad_pct",
        "baterias_vida_util",
        "peso_bateria_g",
        "mantenimientos",
        "componentes_reemplazados",
        "peso_componente_g",
        "peso_nuevo_g",
        "peso_final_g"
    ]
    example_data = [
        ["Sensor de temperatura", 2, 24, 365, 0.1, 5, 30, 8, 65, 2, 50, 1, 2, 20, 200, 180],
        ["Actuador de válvula", 5, 12, 300, 0.2, 7, 50, 9, 70, 3, 60, 2, 1, 25, 250, 230]
    ]
    template_df = pd.DataFrame(example_data, columns=columns)
    # Create help sheet
    help_data = [
        [col, IMPORT_COLUMN_DESCRIPTIONS.get(col, "")] for col in columns
    ]
    help_df = pd.DataFrame(help_data, columns=["Columna", "Descripción y unidad"])
    warning = IMPORT_WARNING
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        template_df.to_excel(writer, index=False, sheet_name="Plantilla")
        help_df.to_excel(writer, index=False, sheet_name="Ayuda")
        # Write warning in the first cell of the help sheet
        ws = writer.sheets["Ayuda"]
        ws.insert_rows(0)
        ws["A1"] = warning
    buffer.seek(0)
    return buffer

def generate_json_template():
    example = [
        {
            "nombre": "Sensor de temperatura",
            "potencia_w": 2,
            "horas_uso_diario": 24,
            "dias_uso_anio": 365,
            "peso_kg": 0.1,
            "vida_util_anios": 5,
            "energia_renovable_pct": 50,
            "funcionalidad_1_10": 8,
            "reciclabilidad_pct": 80,
            "baterias_vida_util": 1,
            "peso_bateria_g": 50,
            "mantenimientos": 2,
            "componentes_reemplazados": 1,
            "peso_componente_g": 10,
            "peso_nuevo_g": 100,
            "peso_final_g": 90
        }
    ]
    return io.BytesIO(json.dumps(example, indent=2, ensure_ascii=False).encode('utf-8')) 