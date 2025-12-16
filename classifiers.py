"""
Módulo para clasificar la prioridad de las señales
"""

def classify_priority(signal):
    """
    Clasifica la prioridad de una señal basándose en la información disponible
    
    Args:
        signal: Diccionario con los datos de la señal
    
    Returns:
        'Alta', 'Media' o 'Baja'
    """
    score = 0
    
    # Tiene email (+2 puntos)
    if signal.get('email'):
        score += 2
    
    # Tiene teléfono (+1 punto)
    if signal.get('telefono'):
        score += 1
    
    # Keywords de alta prioridad
    high_priority_keywords = ['contact', 'admissions', 'housing', 'accommodation']
    titulo_lower = signal.get('titulo', '').lower()
    
    for keyword in high_priority_keywords:
        if keyword in titulo_lower:
            score += 1
            break
    
    # Clasificación
    if score >= 3:
        return 'Alta'
    elif score >= 1:
        return 'Media'
    else:
        return 'Baja'
