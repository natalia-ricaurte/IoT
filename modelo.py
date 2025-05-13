import numpy as np
from pesos import NOMBRES_METRICAS

class SostenibilidadIoT:
    def __init__(self, nombre_dispositivo):
        self.nombre_dispositivo = nombre_dispositivo
        self.resultados = {}
        self.pesos = {
            'CE': 0.22,
            'HC': 0.18,
            'EW': 0.18,
            'ER': 0.12,
            'EE': 0.14,
            'DP': 0.08,
            'RC': 0.05,
            'IM': 0.03
        }
        self.referencias = {
            'CE': {'min': 0, 'max': 100},
            'HC': {'min': 0, 'max': 50},
            'EW': {'min': 0, 'max': 2},
            'ER': {'min': 0, 'max': 100},
            'EE': {'min': 0, 'max': 10},
            'DP': {'min': 1, 'max': 10},
            'RC': {'min': 0, 'max': 100},
            'IM': {'min': 0, 'max': 100}
        }

    def calcular_consumo_energia(self, potencia_W, horas_uso_diario, dias_uso_anual):
        consumo_kWh = (potencia_W * horas_uso_diario * dias_uso_anual) / 1000
        self.resultados['CE'] = consumo_kWh
        return consumo_kWh

    def calcular_huella_carbono(self, consumo_kWh=None, factor_emision=0.5):
        if consumo_kWh is None:
            if 'CE' not in self.resultados:
                raise ValueError("Debe calcular primero el consumo de energía")
            consumo_kWh = self.resultados['CE']
        huella_carbono = consumo_kWh * factor_emision
        self.resultados['HC'] = huella_carbono
        return huella_carbono

    def calcular_ewaste(self, peso_dispositivo_kg, vida_util_años):
        ewaste = peso_dispositivo_kg / vida_util_años
        self.resultados['EW'] = ewaste
        return ewaste

    def calcular_energia_renovable(self, porcentaje_renovable):
        self.resultados['ER'] = porcentaje_renovable
        return porcentaje_renovable

    def calcular_eficiencia_energetica(self, indice_funcionalidad, consumo_kWh=None):
        if consumo_kWh is None:
            if 'CE' not in self.resultados:
                raise ValueError("Debe calcular primero el consumo de energía")
            consumo_kWh = self.resultados['CE']
        consumo_normalizado = 10 - (min(consumo_kWh, 100) / 10)
        eficiencia = (indice_funcionalidad * consumo_normalizado) / 10
        self.resultados['EE'] = eficiencia
        return eficiencia

    def calcular_durabilidad(self, vida_util_años):
        self.resultados['DP'] = vida_util_años
        return vida_util_años

    def calcular_reciclabilidad(self, porcentaje_reciclable):
        self.resultados['RC'] = porcentaje_reciclable
        return porcentaje_reciclable

    def calcular_indice_mantenimiento(self, B, Wb, M, C, Wc, W0, W):
        numerador = (B * Wb) + (M * C * Wc) + (W0 - W)
        IM = (numerador / W0) * 100
        self.resultados['IM'] = IM
        return IM

    def normalizar_metrica(self, codigo_metrica, valor):
        ref = self.referencias[codigo_metrica]
        min_val = ref['min']
        max_val = ref['max']
        if codigo_metrica in ['CE', 'HC', 'EW']:
            if valor >= max_val: return 0
            elif valor <= min_val: return 10
            else: return 10 - (10 * (valor - min_val) / (max_val - min_val))
        else:
            if valor <= min_val: return 0
            elif valor >= max_val: return 10
            else: return 10 * (valor - min_val) / (max_val - min_val)

    def calcular_sostenibilidad(self):
        if not all(key in self.resultados for key in self.pesos.keys()):
            raise ValueError("Debe calcular todas las métricas antes de obtener el índice de sostenibilidad")
        metricas_normalizadas = {
            metrica: self.normalizar_metrica(metrica, valor)
            for metrica, valor in self.resultados.items()
        }
        indice_sostenibilidad = sum(
            metricas_normalizadas[metrica] * self.pesos[metrica]
            for metrica in self.pesos
        )
        return {
            'metricas_crudas': self.resultados,
            'metricas_normalizadas': metricas_normalizadas,
            'indice_sostenibilidad': indice_sostenibilidad
        }
