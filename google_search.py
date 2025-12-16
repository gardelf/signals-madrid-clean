"""
Módulo para realizar búsquedas en Google usando Custom Search API
"""
import os
import requests

def search_google(query, num_results=10):
    """
    Realiza una búsqueda en Google y devuelve los resultados
    
    Args:
        query: Término de búsqueda
        num_results: Número de resultados a devolver
    
    Returns:
        Lista de diccionarios con los resultados
    """
    api_key = os.environ.get('GOOGLE_API_KEY')
    search_engine_id = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
    
    if not api_key or not search_engine_id:
        print("⚠️  Error: Faltan variables de entorno GOOGLE_API_KEY o GOOGLE_SEARCH_ENGINE_ID")
        return []
    
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        'num': min(num_results, 10)  # Google API max 10 per request
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('items', []):
            results.append({
                'titulo': item.get('title', ''),
                'url': item.get('link', ''),
                'snippet': item.get('snippet', ''),
                'displayLink': item.get('displayLink', '')
            })
        
        return results
    
    except Exception as e:
        print(f"❌ Error en búsqueda de Google: {e}")
        return []
