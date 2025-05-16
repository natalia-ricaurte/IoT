import pandas as pd

def to_dict_flat(p):
    """
    Convierte diferentes tipos de datos a un diccionario plano.
    
    Args:
        p: Puede ser un objeto con método to_dict(), una Serie de pandas, un diccionario o un objeto iterable.
    
    Returns:
        dict: Un diccionario plano con los datos.
    """
    if hasattr(p, 'to_dict'):
        return p.to_dict()
    if isinstance(p, pd.Series):
        return p.to_dict()
    if isinstance(p, dict):
        return p
    return dict(p) 