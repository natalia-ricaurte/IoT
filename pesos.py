# pesos.py
import pandas as pd
import numpy as np

# Función para calcular los pesos usando el método AHP
def ahp_attributes(df_criterios):
    suma_columnas = np.array(df_criterios.sum(numeric_only=True))
    matriz_normalizada = df_criterios.div(suma_columnas, axis=1)
    pesos = pd.DataFrame(
        matriz_normalizada.mean(axis=1),
        index=df_criterios.index,
        columns=['peso']
    )
    return pesos.transpose()

# Función para calcular la razón de consistencia de la matriz de comparación
def razon_consistencia(pesos, matriz_comparacion, verbose=True):
    matriz_aleatoria = {
        1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
        9: 1.45, 10: 1.49, 11: 1.51, 12: 1.48, 13: 1.56, 14: 1.57, 15: 1.59,
        16: 1.605, 17: 1.61, 18: 1.615, 19: 1.62, 20: 1.625
    }

    df_temp = matriz_comparacion.multiply(np.array(pesos.loc['peso']), axis=1)
    df_temp['suma'] = df_temp.sum(axis=1)
    lambda_max = df_temp['suma'].div(np.array(pesos.transpose()['peso'])).mean()

    ic = round((lambda_max - len(matriz_comparacion)) / (len(matriz_comparacion) - 1), 3)
    rc = round(ic / matriz_aleatoria[len(matriz_comparacion)], 3)

    if verbose:
        print(f"Índice de Consistencia: {ic}")
        print(f"Razón de Consistencia: {rc}")
        print("La matriz es consistente." if rc < 0.1 else "La matriz NO es consistente.")

    return ic, rc

# Función para obtener los pesos recomendados basados en AHP y ODS
def obtener_pesos_recomendados():
    scores = {
        'CE': 12, 'HC': 11, 'EW': 9, 'ER': 11,
        'EE': 9, 'DP': 8, 'RC': 8, 'IM': 5
    }
    metricas = list(scores.keys())

    def escala_saaty(d):
        if d == 0: return 1
        elif d == 1: return 2
        elif d == 2: return 3
        elif d == 3: return 5
        elif d == 4: return 7
        else: return 9

    matriz = np.ones((len(metricas), len(metricas)))
    for i in range(len(metricas)):
        for j in range(len(metricas)):
            if i != j:
                diff = abs(scores[metricas[i]] - scores[metricas[j]])
                val = escala_saaty(diff)
                matriz[i, j] = val if scores[metricas[i]] > scores[metricas[j]] else 1 / val

    df_criterios = pd.DataFrame(matriz, index=metricas, columns=metricas)
    pesos = ahp_attributes(df_criterios)
    return pesos.loc['peso'].to_dict()

# Función para validar y normalizar los pesos manuales ingresados
def validar_pesos_manuales(pesos_dict):
    suma = sum(pesos_dict.values())
    if abs(suma - 1.0) > 0.01:
        pesos_normalizados = {k: v / suma for k, v in pesos_dict.items()}
        return pesos_normalizados, False
    return pesos_dict, True

# Función que retorna el texto explicativo para la interfaz de usuario
def texto_explicacion_pesos():
    return (
        "Los pesos recomendados se calcularon mediante el método AHP, "
        "combinando el número de Objetivos de Desarrollo Sostenible (ODS) "
        "relacionados con cada métrica y una evaluación cualitativa del impacto ambiental."
    )

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
