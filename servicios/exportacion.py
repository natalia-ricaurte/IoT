import streamlit as st
from datetime import datetime
from io import BytesIO
import openpyxl
from openpyxl.chart import RadarChart, Reference
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

from utilidades.constantes import NOMBRES_METRICAS
from utilidades.auxiliares import to_dict_flat
from pesos import obtener_pesos_recomendados, validar_pesos_manuales

class ExportadorExcel:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws_resumen = self.wb.active
        self.ws_resumen.title = "Resumen"
        self.fecha_calculo = st.session_state.get('fecha_calculo_global', 
                                                datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def _obtener_configuracion_pesos(self):
        """Obtiene la configuración de pesos actual y su nombre."""
        if st.session_state.modo_pesos_radio == "Calcular nuevos pesos" and 'pesos_ahp' in st.session_state:
            nombre_config = "Pesos Calculados"
            pesos_global = st.session_state.pesos_ahp
            for nombre_config, config in st.session_state.configuraciones_ahp.items():
                if to_dict_flat(config['pesos']) == to_dict_flat(pesos_global):
                    nombre_config = f"Configuración Calculada: {nombre_config}"
                    break
        elif st.session_state.modo_pesos_radio == "Ajuste Manual":
            nombre_config = "Pesos Manuales Personalizados"
            pesos_manuales = {k: st.session_state[f"peso_manual_{k}"] for k in NOMBRES_METRICAS}
            pesos_global, _ = validar_pesos_manuales(pesos_manuales)
            for nombre_config, config in st.session_state.pesos_guardados.items():
                if to_dict_flat(config) == to_dict_flat(pesos_global):
                    nombre_config = f"Configuración Manual: {nombre_config}"
                    break
        else:
            nombre_config = "Pesos Recomendados"
            pesos_global = obtener_pesos_recomendados()
        
        return nombre_config, pesos_global

    def _crear_encabezado_resumen(self):
        """Crea el encabezado de la hoja de resumen."""
        self.ws_resumen['A1'] = "Dashboard de Evaluación de Sostenibilidad - Dispositivos IoT"
        self.ws_resumen['A1'].font = Font(bold=True, size=14)
        self.ws_resumen['A3'] = f"Fecha y hora del cálculo: {self.fecha_calculo}"
        self.ws_resumen['A4'] = f"Índice de Sostenibilidad Global: {st.session_state.resultado_global['promedio_total']:.2f}/10"
        
        nombre_config, _ = self._obtener_configuracion_pesos()
        self.ws_resumen['A5'] = f"Configuración de pesos utilizada: {nombre_config}"

    def _crear_tabla_pesos(self, ws, fila_inicio, pesos):
        """Crea una tabla de pesos en la hoja especificada."""
        ws[f'A{fila_inicio}'] = "Pesos utilizados"
        ws[f'A{fila_inicio}'].font = Font(bold=True)
        ws[f'A{fila_inicio+1}'] = "Métrica"
        ws[f'B{fila_inicio+1}'] = "Peso"
        ws[f'A{fila_inicio+1}'].font = ws[f'B{fila_inicio+1}'].font = Font(bold=True)
        
        for i, k in enumerate(NOMBRES_METRICAS.keys()):
            valor_peso = pesos.get(k, None)
            if isinstance(valor_peso, dict):
                valor_peso = list(valor_peso.values())[0]
            try:
                valor_peso = float(valor_peso)
            except Exception:
                valor_peso = ''
            ws[f'A{fila_inicio+2+i}'] = NOMBRES_METRICAS[k]
            ws[f'B{fila_inicio+2+i}'] = valor_peso
        
        return fila_inicio + 2 + len(NOMBRES_METRICAS)

    def _crear_grafico_radar(self, ws, fila_inicio, datos, categorias, titulo, posicion, col_valores=2, col_categorias=1):
        """Crea un gráfico radar en la hoja especificada."""
        chart = RadarChart()
        chart.type = "standard"
        chart.style = 2
        chart.title = titulo
        data = Reference(ws, min_col=col_valores, min_row=fila_inicio, max_row=fila_inicio+len(datos)-1)
        cats = Reference(ws, min_col=col_categorias, min_row=fila_inicio, max_row=fila_inicio+len(datos)-1)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        chart.y_axis.scaling.min = 0
        chart.y_axis.scaling.max = 10
        ws.add_chart(chart, posicion)

    def _crear_hoja_resumen(self):
        """Crea la hoja de resumen con todos sus componentes."""
        self._crear_encabezado_resumen()
        _, pesos_global = self._obtener_configuracion_pesos()
        
        # Tabla de pesos
        fila_actual = self._crear_tabla_pesos(self.ws_resumen, 7, pesos_global)
        
        # Gráfico de métricas globales
        self.ws_resumen[f'A{fila_actual+1}'] = "Gráfico de Métricas Globales"
        self.ws_resumen[f'A{fila_actual+1}'].font = Font(bold=True)
        
        metricas = list(NOMBRES_METRICAS.values())
        valores = [st.session_state.resultado_global['promedio_metricas'][k] for k in NOMBRES_METRICAS.keys()]
        
        fila_metricas = fila_actual + 3
        for i, (metrica, valor) in enumerate(zip(metricas, valores)):
            self.ws_resumen[f'A{fila_metricas+i}'] = metrica
            self.ws_resumen[f'B{fila_metricas+i}'] = valor
        
        self._crear_grafico_radar(
            self.ws_resumen, 
            fila_metricas,  # Fila de inicio de métricas normalizadas
            valores, 
            metricas, 
            "Promedio de Métricas Normalizadas",
            f"D{fila_actual+1}"
        )

    def _crear_hoja_dispositivos(self):
        """Crea la hoja con la lista de dispositivos."""
        ws_dispositivos = self.wb.create_sheet("Dispositivos")
        ws_dispositivos['A1'] = "Lista de Dispositivos Evaluados"
        ws_dispositivos['A1'].font = Font(bold=True, size=14)
        
        headers = ['Nombre', 'Índice de Sostenibilidad']
        for i, header in enumerate(headers):
            ws_dispositivos[f'{get_column_letter(i+1)}3'] = header
            ws_dispositivos[f'{get_column_letter(i+1)}3'].font = Font(bold=True)
        
        for i, dispositivo in enumerate(st.session_state.dispositivos):
            ws_dispositivos[f'A{i+4}'] = dispositivo['nombre']
            ws_dispositivos[f'B{i+4}'] = dispositivo['resultado']['indice_sostenibilidad']

    def _crear_hoja_detalle_dispositivo(self, dispositivo):
        """Crea una hoja de detalle para un dispositivo específico."""
        ws_detalle = self.wb.create_sheet(f"Detalle_{dispositivo['nombre'][:20]}")
        ws_detalle['A1'] = f"Detalles del Dispositivo: {dispositivo['nombre']}"
        ws_detalle['A1'].font = Font(bold=True, size=14)
        ws_detalle['A3'] = f"Índice de Sostenibilidad: {dispositivo['resultado']['indice_sostenibilidad']:.2f}/10"
        
        # Datos de entrada
        ws_detalle['A5'] = "Datos de Entrada"
        ws_detalle['A5'].font = Font(bold=True)
        datos_entrada = {
            'Potencia (W)': dispositivo['potencia'],
            'Horas uso diario': dispositivo['horas'],
            'Días uso/año': dispositivo['dias'],
            'Peso (kg)': dispositivo['peso'],
            'Vida útil (años)': dispositivo['vida'],
            'Energía renovable (%)': dispositivo['energia_renovable'],
            'Funcionalidad': dispositivo['funcionalidad'],
            'Reciclabilidad (%)': dispositivo['reciclabilidad']
        }
        
        for i, (key, value) in enumerate(datos_entrada.items()):
            ws_detalle[f'A{6+i}'] = key
            ws_detalle[f'B{6+i}'] = value
        
        # Configuración de pesos
        nombre_config_disp = self._obtener_nombre_configuracion_dispositivo(dispositivo)
        ws_detalle['D4'] = f"Configuración de pesos utilizada: {nombre_config_disp}"
        ws_detalle['D4'].font = Font(bold=True)
        
        # Tabla de pesos
        fila_actual = self._crear_tabla_pesos(ws_detalle, 5, dispositivo.get('pesos_utilizados', {}))
        
        # Métricas normalizadas y gráfico
        ws_detalle[f'G5'] = "Métricas Normalizadas"
        ws_detalle[f'G5'].font = Font(bold=True)
        
        metricas = []
        valores = []
        fila_metricas = 6
        for i, (key, value) in enumerate(dispositivo['resultado']['metricas_normalizadas'].items()):
            ws_detalle[f'G{fila_metricas+i}'] = NOMBRES_METRICAS[key]
            ws_detalle[f'H{fila_metricas+i}'] = value
            metricas.append(NOMBRES_METRICAS[key])
            valores.append(value)
        
        self._crear_grafico_radar(
            ws_detalle,
            fila_metricas,
            valores,
            metricas,
            f"Métricas Normalizadas - {dispositivo['nombre']}",
            "J5",
            col_valores=8,      # Columna H
            col_categorias=7    # Columna G
        )

    def _obtener_nombre_configuracion_dispositivo(self, dispositivo):
        """Obtiene el nombre de la configuración de pesos utilizada por un dispositivo."""
        pesos_disp = dispositivo.get('pesos_utilizados', {})
        modo_disp = dispositivo.get('snapshot_pesos', {}).get('modo', None)
        
        if modo_disp == "Ajuste Manual":
            pesos_limpios = {k: float(list(v.values())[0]) if isinstance(v, dict) else float(v) 
                           for k, v in pesos_disp.items()}
            pesos_recomendados = obtener_pesos_recomendados()
            if to_dict_flat(pesos_limpios) == to_dict_flat(pesos_recomendados):
                return "Pesos Recomendados"
            
            for nombre, config in st.session_state.pesos_guardados.items():
                if to_dict_flat(config) == to_dict_flat(pesos_limpios):
                    return f"Configuración Manual: {nombre}"
            return "Pesos Manuales Personalizados"
            
        elif modo_disp == "Calcular nuevos pesos":
            pesos_limpios = {k: float(list(v.values())[0]) if isinstance(v, dict) else float(v) 
                           for k, v in pesos_disp.items()}
            for nombre_config, config in st.session_state.configuraciones_ahp.items():
                if to_dict_flat(config['pesos']) == to_dict_flat(pesos_limpios):
                    return f"Configuración Calculada: {nombre_config}"
            return "Pesos Calculados"
        
        return "Pesos Recomendados"

    def exportar(self):
        """Exporta todos los resultados a un archivo Excel."""
        self._crear_hoja_resumen()
        self._crear_hoja_dispositivos()
        
        for dispositivo in st.session_state.dispositivos:
            self._crear_hoja_detalle_dispositivo(dispositivo)
        
        excel_file = BytesIO()
        self.wb.save(excel_file)
        excel_file.seek(0)
        return excel_file

def exportar_resultados_excel():
    """Función principal para exportar resultados a Excel."""
    exportador = ExportadorExcel()
    return exportador.exportar() 