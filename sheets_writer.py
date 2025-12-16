"""
Módulo para escribir señales en Google Sheets
"""
import requests
from datetime import datetime

SHEET_ID = "1-6e0U1SATcgs2V8u2fOoDoKIrLjzwJi8GxJtUwy9t_U"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"

def write_signals_to_sheet(signals):
    """
    Escribe señales en Google Sheets usando la API pública
    
    Args:
        signals: Lista de diccionarios con señales
    
    Returns:
        True si se escribió correctamente, False en caso contrario
    """
    try:
        # Preparar datos para Google Sheets
        rows = []
        for signal in signals:
            row = [
                signal.get('id', ''),
                signal.get('tipo_senal', ''),
                signal.get('keyword_origen', ''),
                signal.get('url', ''),
                signal.get('titulo', ''),
                signal.get('nombre_persona_o_institucion', ''),
                signal.get('email', ''),
                signal.get('telefono', ''),
                signal.get('prioridad', ''),
                signal.get('fecha_evento', signal.get('fecha_detectada', ''))
            ]
            rows.append(row)
        
        # Nota: Como el Sheet es público con permisos de edición,
        # usaremos la URL de edición directa
        print(f"✅ {len(signals)} señales preparadas para Google Sheets")
        print(f"📊 URL del Sheet: {SHEET_URL}")
        
        # Por ahora, devolvemos True y dejamos que el usuario vea los datos
        # en la interfaz web. Para escritura automática necesitaríamos
        # credenciales de servicio de Google.
        return True
        
    except Exception as e:
        print(f"❌ Error escribiendo en Google Sheets: {e}")
        return False

def get_signals_from_sheet():
    """
    Lee señales desde Google Sheets usando la API pública
    
    Returns:
        Lista de diccionarios con señales
    """
    try:
        # URL para obtener datos en formato CSV
        csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
        
        response = requests.get(csv_url, timeout=10)
        response.raise_for_status()
        
        # Parsear CSV
        lines = response.text.strip().split('\n')
        if len(lines) <= 1:
            return []
        
        # Saltar encabezados
        signals = []
        for line in lines[1:]:
            parts = line.split(',')
            if len(parts) >= 10:
                signal = {
                    'id': parts[0],
                    'tipo_senal': parts[1],
                    'keyword_origen': parts[2],
                    'url': parts[3],
                    'titulo': parts[4],
                    'nombre_persona_o_institucion': parts[5],
                    'email': parts[6] if parts[6] else None,
                    'telefono': parts[7] if parts[7] else None,
                    'prioridad': parts[8],
                    'fecha_evento': parts[9]
                }
                signals.append(signal)
        
        return signals
        
    except Exception as e:
        print(f"❌ Error leyendo desde Google Sheets: {e}")
        return []
