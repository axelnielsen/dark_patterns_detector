@app.route('/download/<path:filepath>')
def download_file(filepath):
    """Descarga un archivo o abre HTML en nueva pestaña según extensión."""
    try:
        # Intentar diferentes formas de construir la ruta
        file_path = Path(filepath)
        
        # Si la ruta no es absoluta, intentar construirla desde los directorios permitidos
        if not file_path.is_absolute():
            # Verificar en cada directorio permitido
            allowed_dirs = [REPORTS_FOLDER, SCREENSHOTS_FOLDER, EVIDENCE_FOLDER]
            for allowed_dir in allowed_dirs:
                test_path = allowed_dir / filepath
                if test_path.exists():
                    file_path = test_path
                    break
        
        # Verificar que el archivo existe
        if not file_path.exists():
            print(f"Archivo no encontrado: {file_path}")
            return jsonify({"error": f"File not found: {file_path}"}), 404
        
        # Verificar que el archivo está en un directorio permitido
        allowed_dirs = [REPORTS_FOLDER, SCREENSHOTS_FOLDER, EVIDENCE_FOLDER]
        if not any(str(file_path).resolve().startswith(str(allowed_dir.resolve())) for allowed_dir in allowed_dirs):
            return jsonify({"error": "Access denied: file not in allowed directory"}), 403
        
        # Determinar si el archivo debe descargarse o abrirse en nueva pestaña
        file_extension = file_path.suffix.lower()
        
        # HTML se abre en nueva pestaña, CSV y JSON se descargan
        as_attachment = file_extension != '.html'
        
        # Convertir a ruta relativa al proyecto
        try:
            # Intentar obtener ruta relativa al directorio base
            rel_path = file_path.relative_to(BASE_DIR)
            print(f"Ruta relativa generada: {rel_path}")
        except ValueError:
            # Si no es posible, usar la ruta original
            rel_path = file_path
            print(f"No se pudo generar ruta relativa, usando: {rel_path}")
        
        # Enviar el archivo
        return send_file(str(file_path), as_attachment=as_attachment)
    except Exception as e:
        print(f"Error al procesar archivo: {e}")
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500
