"""
Módulo para escribir y leer señales en Google Sheets usando gspread
"""
import gspread
from google.oauth2.service_account import Credentials
import json
import os

SHEET_ID = "1-6e0U1SATcgs2V8u2fOoDoKIrLjzwJi8GxJtUwy9t_U"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"

# Credenciales de servicio (se cargarán desde variable de entorno en Railway)
SERVICE_ACCOUNT_JSON = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON')

def get_sheet_client():
    """Obtiene cliente autenticado de Google Sheets"""
    try:
        if SERVICE_ACCOUNT_JSON:
            # Cargar credenciales desde variable de entorno
            creds_dict = json.loads(SERVICE_ACCOUNT_JSON)
            creds = Credentials.from_service_account_info(
                creds_dict,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
        else:
            # Fallback: intentar cargar desde archivo local (solo para desarrollo)
            creds = Credentials.from_service_account_file(
                'service_account.json',
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
        
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"❌ Error autenticando con Google Sheets: {e}")
        return None

def write_signals_to_sheet(signals):
    """
    Escribe señales en Google Sheets
    
    Args:
        signals: Lista de diccionarios con señales
    
    Returns:
        True si se escribió correctamente, False en caso contrario
    """
    try:
        client = get_sheet_client()
        if not client:
            print("⚠️  No se pudo autenticar con Google Sheets")
            return False
        
        # Abrir el sheet
        sheet = client.open_by_key(SHEET_ID).sheet1
        
        # Limpiar datos existentes (excepto encabezados)
        sheet.delete_rows(2, sheet.row_count)
        
        # Preparar datos
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
        
        # Escribir datos
        if rows:
            sheet.append_rows(rows)
        
        print(f"✅ {len(signals)} señales escritas en Google Sheets")
        print(f"📊 URL del Sheet: {SHEET_URL}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error escribiendo en Google Sheets: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_signals_from_sheet():
    """
    Lee señales desde Google Sheets
    
    Returns:
        Lista de diccionarios con señales
    """
    try:
        client = get_sheet_client()
        if not client:
            print("⚠️  No se pudo autenticar con Google Sheets")
            return []
        
        # Abrir el sheet
        sheet = client.open_by_key(SHEET_ID).sheet1
        
        # Obtener todos los valores
        rows = sheet.get_all_values()
        
        if len(rows) <= 1:
            print("[DEBUG] Google Sheets vacío (solo encabezados)")
            return []
        
        # Saltar encabezados
        signals = []
        for parts in rows[1:]:
            if len(parts) >= 10 and parts[0].strip():  # Verificar que tenga ID
                signal = {
                    'id': parts[0].strip(),
                    'tipo_senal': parts[1].strip(),
                    'keyword_origen': parts[2].strip(),
                    'url': parts[3].strip(),
                    'titulo': parts[4].strip(),
                    'nombre_persona_o_institucion': parts[5].strip(),
                    'email': parts[6].strip() if parts[6].strip() else None,
                    'telefono': parts[7].strip() if parts[7].strip() else None,
                    'prioridad': parts[8].strip(),
                    'fecha_evento': parts[9].strip()
                }
                signals.append(signal)
        
        print(f"[DEBUG] Leídas {len(signals)} señales desde Google Sheets")
        return signals
        
    except Exception as e:
        print(f"❌ Error leyendo desde Google Sheets: {e}")
        import traceback
        traceback.print_exc()
        return []
