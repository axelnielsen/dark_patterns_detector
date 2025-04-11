"""
Módulo para integrar el nuevo manejador de descargas en la aplicación principal.
"""

import sys
from pathlib import Path

# Añadir el directorio raíz al path para importar módulos
sys.path.append(str(Path(__file__).parent.parent.parent))

def update_app2_download_route():
    """Actualiza la ruta de descarga en app2.py con la nueva implementación."""
    app2_path = Path(__file__).parent / "app2.py"
    download_handler_path = Path(__file__).parent / "download_handler.py"
    
    if not app2_path.exists():
        print(f"ERROR: No se encontró el archivo app2.py en {app2_path}")
        return False
    
    if not download_handler_path.exists():
        print(f"ERROR: No se encontró el archivo download_handler.py en {download_handler_path}")
        return False
    
    # Leer el contenido del nuevo manejador de descargas
    with open(download_handler_path, 'r') as f:
        new_download_handler = f.read()
    
    # Leer el contenido de app2.py
    with open(app2_path, 'r') as f:
        app2_content = f.read()
    
    # Buscar la función download_file actual
    download_route_start = app2_content.find("@app.route('/download/<path:filepath>')")
    if download_route_start == -1:
        print("ERROR: No se encontró la ruta de descarga en app2.py")
        return False
    
    # Encontrar el final de la función
    function_end = app2_content.find("@app.route", download_route_start + 1)
    if function_end == -1:
        # Si no hay más rutas, buscar el final del archivo o una función de creación de app
        function_end = app2_content.find("def create_app", download_route_start + 1)
        if function_end == -1:
            function_end = app2_content.find("if __name__", download_route_start + 1)
            if function_end == -1:
                function_end = len(app2_content)
    
    # Extraer la función actual
    current_download_function = app2_content[download_route_start:function_end].strip()
    
    # Reemplazar la función actual con la nueva
    updated_content = app2_content.replace(current_download_function, new_download_handler.strip())
    
    # Guardar el archivo actualizado
    with open(app2_path, 'w') as f:
        f.write(updated_content)
    
    print("Ruta de descarga actualizada en app2.py")
    return True

def update_task_js():
    """Actualiza task.js para abrir HTML en nueva pestaña."""
    task_js_path = Path(__file__).parent / "static" / "js" / "task.js"
    
    if not task_js_path.exists():
        print(f"ERROR: No se encontró el archivo task.js en {task_js_path}")
        return False
    
    # Leer el contenido de task.js
    with open(task_js_path, 'r') as f:
        task_js_content = f.read()
    
    # Buscar y actualizar los enlaces HTML para que se abran en nueva pestaña
    if "htmlButton.href = `/download/${result.reports.html}`;" in task_js_content:
        # Actualizar para abrir HTML en nueva pestaña
        old_html_button = "htmlButton.href = `/download/${result.reports.html}`;\n                    htmlButton.target = '_blank';"
        new_html_button = "htmlButton.href = `/download/${result.reports.html}`;\n                    htmlButton.target = '_blank';\n                    htmlButton.setAttribute('download', false);"
        
        updated_content = task_js_content.replace(old_html_button, new_html_button)
        
        # Actualizar para descargar JSON
        if "jsonButton.href = `/download/${result.reports.json}`;" in updated_content:
            old_json_button = "jsonButton.href = `/download/${result.reports.json}`;"
            new_json_button = "jsonButton.href = `/download/${result.reports.json}`;\n                    jsonButton.setAttribute('download', true);"
            
            updated_content = updated_content.replace(old_json_button, new_json_button)
        
        # Actualizar para descargar CSV
        if "csvButton.href = `/download/${result.reports.csv}`;" in updated_content:
            old_csv_button = "csvButton.href = `/download/${result.reports.csv}`;"
            new_csv_button = "csvButton.href = `/download/${result.reports.csv}`;\n                    csvButton.setAttribute('download', true);"
            
            updated_content = updated_content.replace(old_csv_button, new_csv_button)
        
        # Guardar el archivo actualizado
        with open(task_js_path, 'w') as f:
            f.write(updated_content)
        
        print("Archivo task.js actualizado para manejar correctamente los tipos de archivos")
        return True
    else:
        print("No se encontraron las referencias a los botones HTML en task.js")
        return False

def main():
    """Función principal para actualizar el manejo de descargas."""
    print("=== Actualizando manejo de descargas ===")
    
    # Actualizar la ruta de descarga en app2.py
    app2_updated = update_app2_download_route()
    
    # Actualizar task.js para manejar correctamente los tipos de archivos
    task_js_updated = update_task_js()
    
    # Resumen
    print("\n=== Resumen de actualizaciones ===")
    print(f"app2.py: {'ACTUALIZADO' if app2_updated else 'ERROR'}")
    print(f"task.js: {'ACTUALIZADO' if task_js_updated else 'ERROR'}")
    
    if app2_updated and task_js_updated:
        print("\nTodas las actualizaciones se han completado correctamente.")
        print("Ahora los archivos HTML se abrirán en una nueva pestaña, mientras que los CSV y JSON se descargarán directamente.")
        print("Las rutas de archivo ahora son relativas al proyecto cuando es posible.")
    else:
        print("\nAlgunas actualizaciones no pudieron completarse. Revise los mensajes anteriores para más detalles.")

if __name__ == "__main__":
    main()
