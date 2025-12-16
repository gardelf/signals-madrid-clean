"""
Módulo para procesar y extraer información de las señales
"""
import re
from datetime import datetime

def extract_email(text):
    """Extrae emails del texto"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text)
    return emails[0] if emails else None

def extract_phone(text):
    """Extrae teléfonos del texto"""
    pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{2,4}[-.\s]?\d{2,4}'
    phones = re.findall(pattern, text)
    return phones[0] if phones else None

def extract_institution(url, title):
    """Extrae el nombre de la institución desde URL o título"""
    # Extraer dominio
    domain_match = re.search(r'https?://(?:www\.)?([^/]+)', url)
    if domain_match:
        domain = domain_match.group(1)
        # Limpiar dominio
        domain = domain.split('.')[0] if '.' in domain else domain
        return domain
    return None

def process_signal(result, keyword):
    """
    Procesa un resultado de búsqueda y extrae información relevante
    
    Args:
        result: Diccionario con datos del resultado de Google
        keyword: Keyword de búsqueda original
    
    Returns:
        Diccionario con la señal procesada o None si no es válida
    """
    if not result.get('url') or not result.get('titulo'):
        return None
    
    text = f"{result.get('titulo', '')} {result.get('snippet', '')}"
    
    signal = {
        'id': f"SIG-{datetime.now().strftime('%Y%m%d%H%M')}-{abs(hash(result['url'])) % 1000}",
        'titulo': result.get('titulo', ''),
        'url': result.get('url', ''),
        'tipo_senal': 'Institucional - Programa 2026',
        'email': extract_email(text),
        'telefono': extract_phone(text),
        'nombre_persona_o_institucion': extract_institution(result['url'], result['titulo']),
        'keyword_origen': keyword,
        'fecha_detectada': datetime.now().strftime('%Y-%m-%d'),
        'fecha_evento': '2026'
    }
    
    return signal
