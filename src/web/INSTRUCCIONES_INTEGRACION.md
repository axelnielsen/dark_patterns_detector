"""
Instrucciones para integrar las funcionalidades de exportación en el sistema principal
"""

# Paso 1: Añadir las importaciones necesarias al inicio de app.py
"""
import os
import json
import csv
from datetime import datetime
"""

# Paso 2: Añadir las funciones auxiliares después de las importaciones
"""
def calculate_severity_score(detections):
    """
    Calcula una puntuación de severidad basada en las detecciones.
    
    Args:
        detections: Lista de detecciones de patrones oscuros
        
    Returns:
        float: Puntuación de severidad entre 0 y 10
    """
    if not detections:
        return 0
    
    # Pesos por tipo de patrón
    pattern_weights = {
        "confirmshaming": 0.8,
        "preselection": 0.7,
        "hidden_costs": 0.9,
        "difficult_cancellation": 0.85,
        "misleading_ads": 0.75,
        "false_urgency": 0.8,
        "confusing_interface": 0.7
    }
    
    # Calcular puntuación
    total_weight = 0
    weighted_sum = 0
    
    for detection in detections:
        pattern_type = detection.get("pattern_type", "")
        confidence = detection.get("confidence", 0)
        
        weight = pattern_weights.get(pattern_type, 0.5)
        weighted_sum += weight * confidence
        total_weight += weight
    
    # Normalizar a escala 0-10
    if total_weight > 0:
        score = (weighted_sum / total_weight) * 10
    else:
        score = 0
    
    return round(score, 1)


def get_pattern_display_name(pattern_type):
    """
    Obtiene el nombre de visualización para un tipo de patrón.
    
    Args:
        pattern_type: Tipo de patrón (clave interna)
        
    Returns:
        str: Nombre de visualización
    """
    pattern_names = {
        "confirmshaming": "Confirmshaming (Avergonzar al rechazar)",
        "preselection": "Preselección de opciones",
        "hidden_costs": "Costos ocultos",
        "difficult_cancellation": "Cancelación difícil",
        "misleading_ads": "Publicidad engañosa",
        "false_urgency": "Falsa urgencia o escasez",
        "confusing_interface": "Interfaz confusa"
    }
    
    return pattern_names.get(pattern_type, pattern_type.replace("_", " ").title())
"""

# Paso 3: Añadir la ruta de API para exportar todos los informes
"""
@app.route('/api/export-all/<task_id>/<format>')
def api_export_all_reports(task_id, format):
    """API para exportar todos los informes en diferentes formatos."""
    if task_id not in analysis_tasks:
        return jsonify({"error": "Task not found"}), 404
    
    task = analysis_tasks[task_id]
    
    if task.status != "completed":
        return jsonify({"error": "Task not completed yet"}), 400
    
    if format not in ["json", "html", "csv"]:
        return jsonify({"error": "Unsupported format"}), 400
    
    try:
        # Crear gestor de informes
        report_manager = ReportManager(str(REPORTS_FOLDER))
        
        # Preparar datos para el informe
        all_reports = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for url, result in task.results.items():
            if result.get("success", False):
                report_data = {
                    "url": url,
                    "title": result.get("title", "Sin título"),
                    "timestamp": datetime.now().isoformat(),
                    "summary": {
                        "total_patterns_detected": len(result.get("detections", [])),
                        "pattern_types_detected": list(set(d.get("pattern_type", "") for d in result.get("detections", []))),
                        "severity_score": calculate_severity_score(result.get("detections", []))
                    },
                    "patterns": [],
                    "screenshots": result.get("screenshots", {})
                }
                
                # Agrupar detecciones por tipo
                patterns_by_type = {}
                for detection in result.get("detections", []):
                    pattern_type = detection.get("pattern_type", "unknown")
                    if pattern_type not in patterns_by_type:
                        patterns_by_type[pattern_type] = []
                    patterns_by_type[pattern_type].append(detection)
                
                # Añadir información de cada tipo de patrón
                for pattern_type, pattern_detections in patterns_by_type.items():
                    pattern_info = {
                        "type": pattern_type,
                        "count": len(pattern_detections),
                        "detections": pattern_detections
                    }
                    report_data["patterns"].append(pattern_info)
                
                all_reports.append(report_data)
        
        # Generar archivo según el formato solicitado
        output_filename = f"all_reports_{task_id}_{timestamp}"
        
        if format == "json":
            # Exportar todos los informes en un solo archivo JSON
            output_path = os.path.join(str(REPORTS_FOLDER), f"{output_filename}.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(all_reports, f, indent=2, ensure_ascii=False)
            
            return jsonify({"file": output_path})
            
        elif format == "csv":
            # Exportar todos los informes en un solo archivo CSV
            output_path = os.path.join(str(REPORTS_FOLDER), f"{output_filename}.csv")
            
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                
                # Escribir encabezados
                writer.writerow([
                    "URL", "Título", "Patrones Detectados", "Tipos de Patrones", 
                    "Puntuación de Severidad", "Timestamp"
                ])
                
                # Escribir datos de cada informe
                for report in all_reports:
                    writer.writerow([
                        report["url"],
                        report["title"],
                        report["summary"]["total_patterns_detected"],
                        ", ".join(report["summary"]["pattern_types_detected"]),
                        report["summary"]["severity_score"],
                        report["timestamp"]
                    ])
                    
                    # Añadir línea en blanco para separar
                    writer.writerow([])
                    
                    # Añadir detalles de cada patrón
                    for pattern in report["patterns"]:
                        writer.writerow([
                            f"Patrón: {pattern['type']}",
                            f"Cantidad: {pattern['count']}",
                            "", "", "", ""
                        ])
                        
                        # Añadir detalles de cada detección
                        for detection in pattern["detections"]:
                            writer.writerow([
                                f"  - {detection.get('location', 'Ubicación desconocida')}",
                                f"  Confianza: {detection.get('confidence', 0)}",
                                "", "", "", ""
                            ])
                    
                    # Añadir línea en blanco para separar informes
                    writer.writerow([])
                    writer.writerow(["---", "---", "---", "---", "---", "---"])
                    writer.writerow([])
            
            return jsonify({"file": output_path})
            
        elif format == "html":
            # Exportar todos los informes en un solo archivo HTML
            output_path = os.path.join(str(REPORTS_FOLDER), f"{output_filename}.html")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                # Escribir encabezado HTML
                f.write(f\"\"\"<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Informes de Patrones Oscuros - Tarea {task_id}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; color: #333; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .report {{ border: 1px solid #ddd; border-radius: 5px; padding: 20px; margin-bottom: 30px; }}
        .report-header {{ background-color: #f8f9fa; padding: 15px; margin: -20px -20px 20px; border-bottom: 1px solid #ddd; border-radius: 5px 5px 0 0; }}
        .summary {{ display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 20px; }}
        .summary-item {{ flex: 1; min-width: 200px; background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
        .pattern {{ margin-bottom: 20px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }}
        .detection {{ margin: 10px 0; padding: 10px; background-color: #fff; border: 1px solid #ddd; border-radius: 5px; }}
        .confidence {{ display: inline-block; padding: 3px 8px; border-radius: 3px; font-size: 0.8em; }}
        .confidence.high {{ background-color: #f8d7da; color: #721c24; }}
        .confidence.medium {{ background-color: #fff3cd; color: #856404; }}
        .confidence.low {{ background-color: #d1ecf1; color: #0c5460; }}
        .screenshots {{ margin-top: 20px; }}
        .screenshots img {{ max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 5px; margin-top: 10px; }}
        .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center; font-size: 0.9em; color: #6c757d; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Informes de Patrones Oscuros</h1>
        <p>Tarea: {task_id}</p>
        <p>Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        <p>Total de URLs analizadas: {len(all_reports)}</p>
\"\"\")
                
                # Escribir cada informe
                for report in all_reports:
                    f.write(f\"\"\"
        <div class="report">
            <div class="report-header">
                <h2>{report["title"]}</h2>
                <p><a href="{report["url"]}" target="_blank">{report["url"]}</a></p>
            </div>
            
            <div class="summary">
                <div class="summary-item">
                    <h3>Patrones Detectados</h3>
                    <p>{report["summary"]["total_patterns_detected"]}</p>
                </div>
                <div class="summary-item">
                    <h3>Tipos de Patrones</h3>
                    <p>{", ".join(report["summary"]["pattern_types_detected"])}</p>
                </div>
                <div class="summary-item">
                    <h3>Puntuación de Severidad</h3>
                    <p>{report["summary"]["severity_score"]}</p>
                </div>
            </div>
\"\"\")
                    
                    # Escribir detalles de cada patrón
                    if report["patterns"]:
                        f.write(f\"\"\"
            <h3>Detalles de Patrones Detectados</h3>
\"\"\")
                        
                        for pattern in report["patterns"]:
                            pattern_name = get_pattern_display_name(pattern["type"])
                            f.write(f\"\"\"
            <div class="pattern">
                <h4>{pattern_name} ({pattern["count"]})</h4>
\"\"\")
                            
                            # Escribir detalles de cada detección
                            for detection in pattern["detections"]:
                                confidence = detection.get("confidence", 0)
                                confidence_class = "high" if confidence > 0.8 else "medium" if confidence > 0.6 else "low"
                                
                                f.write(f\"\"\"
                <div class="detection">
                    <p><strong>Ubicación:</strong> {detection.get("location", "Ubicación desconocida")}</p>
                    <p><strong>Confianza:</strong> <span class="confidence {confidence_class}">{confidence:.2f}</span></p>
\"\"\")
                                
                                # Añadir evidencia si está disponible
                                if "evidence" in detection and detection["evidence"]:
                                    f.write(f\"\"\"
                    <p><strong>Evidencia:</strong></p>
                    <pre>{json.dumps(detection["evidence"], indent=2, ensure_ascii=False)}</pre>
\"\"\")
                                
                                f.write(f\"\"\"
                </div>
\"\"\")
                            
                            f.write(f\"\"\"
            </div>
\"\"\")
                    else:
                        f.write(f\"\"\"
            <p>No se detectaron patrones oscuros en esta URL.</p>
\"\"\")
                    
                    # Añadir capturas de pantalla si están disponibles
                    if "screenshots" in report and report["screenshots"]:
                        f.write(f\"\"\"
            <div class="screenshots">
                <h3>Capturas de Pantalla</h3>
\"\"\")
                        
                        for screenshot_type, screenshot_path in report["screenshots"].items():
                            if screenshot_path:
                                screenshot_filename = os.path.basename(screenshot_path)
                                f.write(f\"\"\"
                <p><strong>{screenshot_type.capitalize()}:</strong></p>
                <img src="/download/{screenshot_path}" alt="Captura de pantalla {screenshot_type}">
\"\"\")
                        
                        f.write(f\"\"\"
            </div>
\"\"\")
                    
                    f.write(f\"\"\"
        </div>
\"\"\")
                
                # Escribir pie de página
                f.write(f\"\"\"
        <div class="footer">
            <p>Generado por el Detector de Patrones Oscuros - {datetime.now().strftime('%Y')}</p>
        </div>
    </div>
</body>
</html>
\"\"\")
            
            return jsonify({"file": output_path})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""
