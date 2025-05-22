
class IoTSustainability:
    def __init__(self, device_name):
        self.device_name = device_name
        self.results = {}
        self.weights = {
            'EC': 0.22,
            'CF': 0.18,
            'EW': 0.18,
            'RE': 0.12,
            'EE': 0.14,
            'PD': 0.08,
            'RC': 0.05,
            'MT': 0.03
        }
        self.references = {
            'EC': {'min': 0, 'max': 100},
            'CF': {'min': 0, 'max': 50},
            'EW': {'min': 0, 'max': 2},
            'RE': {'min': 0, 'max': 100},
            'EE': {'min': 0, 'max': 10},
            'PD': {'min': 1, 'max': 10},
            'RC': {'min': 0, 'max': 100},
            'MT': {'min': 0, 'max': 100}
        }

    def calculate_energy_consumption(self, power_W, daily_usage_hours, annual_usage_days):
        consumption_kWh = (power_W * daily_usage_hours * annual_usage_days) / 1000
        self.results['EC'] = consumption_kWh
        return consumption_kWh

    def calculate_carbon_footprint(self, consumption_kWh=None, emission_factor=0.5):
        if consumption_kWh is None:
            if 'EC' not in self.results:
                raise ValueError("Debe calcular primero el consumo de energía")
            consumption_kWh = self.results['EC']
        carbon_footprint = consumption_kWh * emission_factor
        self.results['CF'] = carbon_footprint
        return carbon_footprint

    def calculate_ewaste(self, device_weight_kg, useful_life_years):
        ewaste = device_weight_kg / useful_life_years
        self.results['EW'] = ewaste
        return ewaste

    def calculate_renewable_energy(self, renewable_percentage):
        self.results['RE'] = renewable_percentage
        return renewable_percentage

    def calculate_energy_efficiency(self, functionality_index, consumption_kWh=None):
        if consumption_kWh is None:
            if 'EC' not in self.results:
                raise ValueError("Debe calcular primero el consumo de energía")
            consumption_kWh = self.results['EC']
        normalized_consumption = 10 - (min(consumption_kWh, 100) / 10)
        efficiency = (functionality_index * normalized_consumption) / 10
        self.results['EE'] = efficiency
        return efficiency

    def calculate_durability(self, useful_life_years):
        self.results['PD'] = useful_life_years
        return useful_life_years

    def calculate_recyclability(self, recyclable_percentage):
        self.results['RC'] = recyclable_percentage
        return recyclable_percentage

    def calculate_maintenance_index(self, B, Wb, M, C, Wc, W0, W):
        numerator = (B * Wb) + (M * C * Wc) + (W0 - W)
        MT = (numerator / W0) * 100
        self.results['MT'] = MT
        return MT

    def normalize_metric(self, metric_code, value):
        ref = self.references[metric_code]
        min_val = ref['min']
        max_val = ref['max']
        if metric_code in ['EC', 'CF', 'EW']:
            if value >= max_val: return 0
            elif value <= min_val: return 10
            else: return 10 - (10 * (value - min_val) / (max_val - min_val))
        else:
            if value <= min_val: return 0
            elif value >= max_val: return 10
            else: return 10 * (value - min_val) / (max_val - min_val)

    def calculate_sustainability(self):
        if not all(key in self.results for key in self.weights.keys()):
            raise ValueError("Debe calcular todas las métricas antes de obtener el índice de sostenibilidad")
        normalized_metrics = {
            metric: self.normalize_metric(metric, value)
            for metric, value in self.results.items()
        }
        sustainability_index = sum(
            normalized_metrics[metric] * self.weights[metric]
            for metric in self.weights
        )
        return {
            'raw_metrics': self.results,
            'normalized_metrics': normalized_metrics,
            'sustainability_index': sustainability_index
        } 