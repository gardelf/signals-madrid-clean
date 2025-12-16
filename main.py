#!/usr/bin/env python3
"""
Motor de Captación de Señales - Madrid
Genera señales de oportunidades de negocio sin base de datos
"""
import json
import os
from datetime import datetime
from google_search import search_google
from processors import process_signal
from classifiers import classify_priority

# Configuración
OUTPUT_FILE = '/app/signals_today.json'
SEARCH_QUERIES = [
    "summer school Madrid 2026 contact",
    "business school summer course Madrid email",
    "IE summer school contact",
    "ESADE summer madrid admissions",
    "Comillas summer school housing",
    "EOI summer madrid contact",
    "UC3M study abroad housing",
    "Saint Louis University Madrid housing",
    "SLU Madrid accommodation contact",
    "Suffolk University Madrid study abroad contact",
    "NYU Madrid study abroad housing",
    "spanish school madrid summer course contact"
]

def main():
    """Ejecuta el motor de captación de señales"""
    print("🎯 Iniciando Motor de Captación de Señales - Madrid")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_signals = []
    
    for query in SEARCH_QUERIES:
        print(f"\n🔍 Buscando: {query}")
        results = search_google(query, num_results=15)
        
        for result in results:
            signal = process_signal(result, query)
            if signal:
                signal['prioridad'] = classify_priority(signal)
                all_signals.append(signal)
                print(f"  ✅ {signal['titulo'][:50]}... [{signal['prioridad']}]")
    
    # Guardar en JSON
    output_data = {
        'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_senales': len(all_signals),
        'senales': all_signals
    }
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Proceso completado: {len(all_signals)} señales generadas")
    print(f"📄 Archivo guardado en: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
