from streamlit_echarts import st_echarts

def radar_chart(metrics, title, key):
    """Generates a radar chart to visualize sustainability metrics.
    
    Args:
        metrics (dict): Dictionary with metrics and their values
        title (str): Chart title
        key (str): Unique key for the Streamlit component
    """
    labels = {
        'EC': 'Cons. Energía', 
        'CF': 'Huella CO₂', 
        'EW': 'E-waste',
        'RE': 'Energía Renov.', 
        'EE': 'Eficiencia', 
        'PD': 'Durabilidad',
        'RC': 'Reciclabilidad', 
        'MT': 'Mantenimiento'
    }
    
    label_values = [labels[m] for m in metrics.keys()]
    values = list(metrics.values())

    options = {
        "backgroundColor": "#111111",
        "title": {
            "text": title,
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
            "indicator": [{"name": label, "max": 10} for label in label_values],
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
                "name": title,
                "type": "radar",
                "data": [
                    {
                        "value": values,
                        "name": title,
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

    # Render with ECharts using the unique key
    st_echarts(options=options, height="500px", key=key) 