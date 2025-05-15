from streamlit_echarts import st_echarts

def radar_chart(metricas, titulo, key):
    """Genera un gráfico radar para visualizar las métricas de sostenibilidad.
    
    Args:
        metricas (dict): Diccionario con las métricas y sus valores
        titulo (str): Título del gráfico
        key (str): Clave única para el componente Streamlit
    """
    etiquetas = {
        'CE': 'Cons. Energía', 
        'HC': 'Huella CO₂', 
        'EW': 'E-waste',
        'ER': 'Energía Renov.', 
        'EE': 'Eficiencia', 
        'DP': 'Durabilidad',
        'RC': 'Reciclabilidad', 
        'IM': 'Mantenimiento'
    }
    
    labels = [etiquetas[m] for m in metricas.keys()]
    valores = list(metricas.values())

    options = {
        "backgroundColor": "#111111",
        "title": {
            "text": titulo,
            "left": "center",
            "top": "5%",
            "textStyle": {
                "color": "#ffffff",
                "fontSize": 20,
            },
        },
        "tooltip": {
            "trigger": "item"
        },
        "radar": {
            "indicator": [{"name": label, "max": 10} for label in labels],
            "radius": "60%",
            "center": ["50%", "55%"],
            "splitNumber": 5,
            "axisLine": {
                "lineStyle": {"color": "#3498db"}
            },
            "splitLine": {
                "lineStyle": {"color": "#444444"},
                "show": True
            },
            "splitArea": {
                "areaStyle": {"color": ["#2e2e3e", "#1e1e2f"]}
            }
        },
        "series": [
            {
                "name": titulo,
                "type": "radar",
                "data": [
                    {
                        "value": valores,
                        "name": titulo,
                        "itemStyle": {
                            "color": "#3498db"
                        },
                        "lineStyle": {
                            "color": "#3498db"
                        },
                        "areaStyle": {
                            "color": "#3498db",
                            "opacity": 0.3
                        }
                    }
                ]
            }
        ]
    }

    # Renderizar con ECharts usando el key único
    st_echarts(options=options, height="500px", key=key) 