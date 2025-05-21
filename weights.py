# weights.py
import pandas as pd
import numpy as np

# Function to calculate weights using AHP method
def ahp_attributes(criteria_df):
    column_sums = np.array(criteria_df.sum(numeric_only=True))
    normalized_matrix = criteria_df.div(column_sums, axis=1)
    weights = pd.DataFrame(
        normalized_matrix.mean(axis=1),
        index=criteria_df.index,
        columns=['weight']
    )
    return weights.transpose()

# Function to calculate the consistency ratio of the comparison matrix
def consistency_ratio(weights, comparison_matrix, verbose=True):
    random_matrix = {
        1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41,
        9: 1.45, 10: 1.49, 11: 1.51, 12: 1.48, 13: 1.56, 14: 1.57, 15: 1.59,
        16: 1.605, 17: 1.61, 18: 1.615, 19: 1.62, 20: 1.625
    }

    temp_df = comparison_matrix.multiply(np.array(weights.loc['weight']), axis=1)
    temp_df['sum'] = temp_df.sum(axis=1)
    lambda_max = temp_df['sum'].div(np.array(weights.transpose()['weight'])).mean()

    ci = round((lambda_max - len(comparison_matrix)) / (len(comparison_matrix) - 1), 3)
    cr = round(ci / random_matrix[len(comparison_matrix)], 3)

    if verbose:
        print(f"Índice de Consistencia: {ci}")
        print(f"Razón de Consistencia: {cr}")
        print("La matriz es consistente." if cr < 0.1 else "La matriz NO es consistente.")

    return ci, cr

# Function to get recommended weights based on AHP and SDG
def get_recommended_weights():
    scores = {
        'EC': 12,  # Energy Consumption
        'CF': 11,  # Carbon Footprint
        'EW': 9,   # Electronic Waste
        'RE': 11,  # Renewable Energy Use
        'EE': 9,   # Energy Efficiency
        'PD': 8,   # Product Durability
        'RC': 8,   # Recyclability
        'MT': 5    # Maintenance
    }
    metrics = list(scores.keys())

    def saaty_scale(d):
        if d == 0: return 1
        elif d == 1: return 2
        elif d == 2: return 3
        elif d == 3: return 5
        elif d == 4: return 7
        else: return 9

    matrix = np.ones((len(metrics), len(metrics)))
    for i in range(len(metrics)):
        for j in range(len(metrics)):
            if i != j:
                diff = abs(scores[metrics[i]] - scores[metrics[j]])
                val = saaty_scale(diff)
                matrix[i, j] = val if scores[metrics[i]] > scores[metrics[j]] else 1 / val

    criteria_df = pd.DataFrame(matrix, index=metrics, columns=metrics)
    weights = ahp_attributes(criteria_df)
    return weights.loc['weight'].to_dict()

# Function to validate and normalize manually entered weights
def validate_manual_weights(weights_dict):
    total = sum(weights_dict.values())
    if abs(total - 1.0) > 0.01:
        normalized_weights = {k: v / total for k, v in weights_dict.items()}
        return normalized_weights, False
    return weights_dict, True 