import os
import json
import csv
from datetime import datetime
import sys
from pathlib import Path

# Añadir el directorio raíz al path para importar módulos
sys.path.append(str(Path(__file__).parent.parent.parent))

# Importar las funciones necesarias del archivo app_export.py
from app_export import api_export_all_reports, calculate_severity_score, get_pattern_display_name

# Importar Flask y otras dependencias necesarias
from flask import Flask, jsonify

# Crear una aplicación Flask para integrar las nuevas rutas
app = Flask(__name__)

# Definir la ruta para la exportación de todos los informes
@app.route('/api/export-all/<task_id>/<format>')
def export_all_reports(task_id, format):
    """
    Ruta para exportar todos los informes en diferentes formatos.
    Esta función actúa como un wrapper para la implementación real en app_export.py
    
    Args:
        task_id: ID de la tarea
        format: Formato de exportación (json, html, csv)
        
    Returns:
        Respuesta JSON con la ruta del archivo generado
    """
    return api_export_all_reports(task_id, format)

# Punto de entrada para pruebas
if __name__ == '__main__':
    print("Módulo de exportación cargado correctamente")
