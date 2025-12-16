from flask import Flask, render_template_string, jsonify
import json
import os
from datetime import datetime
import threading

app = Flask(__name__)

DATA_FILE = '/app/signals_today.json'
LAST_EXECUTION = None

def run_motor():
    """Ejecuta el motor de captación"""
    global LAST_EXECUTION
    try:
        from main import main as motor_main
        motor_main()
        LAST_EXECUTION = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Error ejecutando motor: {e}")

@app.route('/')
def index():
    """Página principal con tabla interactiva"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/signals')
def get_signals():
    """API para obtener las señales desde Google Sheets"""
    try:
        from sheets_writer import get_signals_from_sheet
        signals = get_signals_from_sheet()
        
        # Fallback a JSON si Google Sheets falla
        if not signals and os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                signals = data.get('senales', [])
                last_exec = data.get('fecha_generacion', 'N/A')
        else:
            last_exec = LAST_EXECUTION or 'N/A'
        
        return jsonify({
            'success': True,
            'signals': signals,
            'total': len(signals),
            'last_execution': last_exec
        })
    except Exception as e:
        print(f"Error en /api/signals: {e}")
        return jsonify({'success': False, 'error': str(e), 'signals': [], 'total': 0})

@app.route('/regenerate', methods=['POST'])
def regenerate():
    """Regenera el informe ejecutando el motor en segundo plano"""
    thread = threading.Thread(target=run_motor)
    thread.start()
    return jsonify({'success': True, 'message': 'Motor ejecutándose...'})

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motor de Captación de Señales</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.datatables.net/1.13.6/css/dataTables.bootstrap5.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; }
        .container { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
        h1 { color: #667eea; margin-bottom: 30px; }
        .badge-alta { background-color: #dc3545; }
        .badge-media { background-color: #ffc107; color: #000; }
        .badge-baja { background-color: #6c757d; }
        .stats { display: flex; gap: 20px; margin-bottom: 30px; flex-wrap: wrap; }
        .stat-card { flex: 1; min-width: 150px; padding: 15px; border-radius: 10px; text-align: center; }
        .stat-card h3 { margin: 0; font-size: 2em; }
        .stat-card p { margin: 5px 0 0 0; color: #666; }
        table.dataTable tbody tr:hover { background-color: #f8f9fa; }
        .url-cell { max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Motor de Captación de Señales - Madrid</h1>
        
        <div class="mb-4">
            <button id="btnRegenerate" class="btn btn-success">🔄 Regenerar Informe</button>
            <span id="lastExecution" class="ms-3 text-muted"></span>
        </div>

        <div class="stats" id="stats"></div>

        <table id="signalsTable" class="table table-striped table-hover" style="width:100%">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Prioridad</th>
                    <th>Título</th>
                    <th>Tipo</th>
                    <th>Email</th>
                    <th>Teléfono</th>
                    <th>Institución</th>
                    <th>Keyword</th>
                    <th>Fecha</th>
                    <th>URL</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>
    </div>

    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.6/js/dataTables.bootstrap5.min.js"></script>
    <script>
        let table;

        function loadSignals() {
            fetch('/api/signals')
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        updateStats(data.signals);
                        updateTable(data.signals);
                        $('#lastExecution').text('Última ejecución: ' + data.last_execution);
                    }
                });
        }

        function updateStats(signals) {
            const alta = signals.filter(s => s.prioridad === 'Alta').length;
            const media = signals.filter(s => s.prioridad === 'Media').length;
            const baja = signals.filter(s => s.prioridad === 'Baja').length;
            const conEmail = signals.filter(s => s.email).length;

            $('#stats').html(`
                <div class="stat-card" style="background: #e3f2fd;">
                    <h3>${signals.length}</h3>
                    <p>Total Señales</p>
                </div>
                <div class="stat-card" style="background: #ffebee;">
                    <h3>${alta}</h3>
                    <p>Prioridad Alta</p>
                </div>
                <div class="stat-card" style="background: #fff3e0;">
                    <h3>${media}</h3>
                    <p>Prioridad Media</p>
                </div>
                <div class="stat-card" style="background: #f3e5f5;">
                    <h3>${conEmail}</h3>
                    <p>Con Email</p>
                </div>
            `);
        }

        function updateTable(signals) {
            if (table) {
                table.destroy();
            }

            const tableData = signals.map(s => [
                s.id || '',
                `<span class="badge badge-${s.prioridad.toLowerCase()}">${s.prioridad}</span>`,
                s.titulo || '',
                s.tipo_senal || '',
                s.email || '-',
                s.telefono || '-',
                s.nombre_persona_o_institucion || '',
                s.keyword_origen || '',
                s.fecha_evento || s.fecha_detectada || '',
                `<a href="${s.url}" target="_blank" class="url-cell">${s.url}</a>`
            ]);

            table = $('#signalsTable').DataTable({
                data: tableData,
                order: [[1, 'asc'], [0, 'desc']],
                pageLength: 25,
                language: {
                    url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json'
                }
            });
        }

        $('#btnRegenerate').click(function() {
            $(this).prop('disabled', true).text('⏳ Ejecutando...');
            fetch('/regenerate', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    alert('Motor ejecutándose. Actualiza la página en 2 minutos.');
                    setTimeout(() => {
                        $('#btnRegenerate').prop('disabled', false).text('🔄 Regenerar Informe');
                    }, 3000);
                });
        });

        $(document).ready(function() {
            loadSignals();
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
