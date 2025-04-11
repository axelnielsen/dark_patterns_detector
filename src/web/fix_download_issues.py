"""
Módulo para verificar y corregir rutas de archivos para la descarga de informes.
Este script debe ejecutarse para diagnosticar y solucionar problemas con las rutas de archivos.
"""

import os
import sys
from pathlib import Path

# Añadir el directorio raíz al path para importar módulos
sys.path.append(str(Path(__file__).parent.parent.parent))

# Configuración de directorios
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_FOLDER = DATA_DIR / "reports"
SCREENSHOTS_FOLDER = DATA_DIR / "screenshots"
EVIDENCE_FOLDER = DATA_DIR / "evidence"

def check_directory(directory, name):
    """Verifica si un directorio existe y tiene permisos correctos."""
    print(f"Verificando directorio {name}: {directory}")
    
    # Verificar si existe
    if not directory.exists():
        print(f"  - ERROR: El directorio no existe")
        try:
            directory.mkdir(exist_ok=True, parents=True)
            print(f"  - CORREGIDO: Directorio creado")
        except Exception as e:
            print(f"  - ERROR: No se pudo crear el directorio: {e}")
            return False
    else:
        print(f"  - OK: El directorio existe")
    
    # Verificar permisos
    try:
        test_file = directory / ".test_write_permission"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print(f"  - OK: El directorio tiene permisos de escritura")
    except Exception as e:
        print(f"  - ERROR: Problema con permisos: {e}")
        try:
            os.chmod(directory, 0o755)
            print(f"  - CORREGIDO: Permisos actualizados")
        except Exception as e:
            print(f"  - ERROR: No se pudieron corregir los permisos: {e}")
            return False
    
    return True

def list_directory_contents(directory, name):
    """Lista el contenido de un directorio."""
    print(f"Contenido del directorio {name}:")
    
    if not directory.exists():
        print(f"  - El directorio no existe")
        return
    
    files = list(directory.glob("*"))
    
    if not files:
        print(f"  - El directorio está vacío")
        return
    
    for file in files:
        file_size = os.path.getsize(file) if os.path.isfile(file) else "directorio"
        print(f"  - {file.name} ({file_size} bytes)")

def fix_download_route():
    """Corrige la ruta de descarga en app2.py."""
    app2_path = Path(__file__).parent / "app2.py"
    
    if not app2_path.exists():
        print(f"ERROR: No se encontró el archivo app2.py en {app2_path}")
        return False
    
    with open(app2_path, 'r') as f:
        content = f.read()
    
    # Buscar y corregir la función download_file
    if "@app.route('/download/<path:filepath>')" in content:
        print("Encontrada ruta de descarga en app2.py")
        
        # Verificar si hay problemas con la función
        if "file_path = Path(filepath)" in content:
            print("Corrigiendo función download_file...")
            
            # Reemplazar la función con una versión mejorada
            old_function = '@app.route(\'/download/<path:filepath>\')\ndef download_file(filepath):\n    """Descarga un archivo."""\n    # Verificar que el archivo existe y está dentro de los directorios permitidos\n    file_path = Path(filepath)\n    \n    if not file_path.exists():\n        return jsonify({"error": "File not found"}), 404\n    \n    # Verificar que el archivo está en un directorio permitido\n    allowed_dirs = [REPORTS_FOLDER, SCREENSHOTS_FOLDER, EVIDENCE_FOLDER]\n    if not any(str(file_path).startswith(str(allowed_dir)) for allowed_dir in allowed_dirs):\n        return jsonify({"error": "Access denied"}), 403\n    \n    return send_file(file_path, as_attachment=True)'
            
            new_function = '@app.route(\'/download/<path:filepath>\')\ndef download_file(filepath):\n    """Descarga un archivo."""\n    # Verificar que el archivo existe y está dentro de los directorios permitidos\n    try:\n        # Intentar diferentes formas de construir la ruta\n        file_path = Path(filepath)\n        \n        # Si la ruta no es absoluta, intentar construirla desde los directorios permitidos\n        if not file_path.is_absolute():\n            # Verificar en cada directorio permitido\n            allowed_dirs = [REPORTS_FOLDER, SCREENSHOTS_FOLDER, EVIDENCE_FOLDER]\n            for allowed_dir in allowed_dirs:\n                test_path = allowed_dir / filepath\n                if test_path.exists():\n                    file_path = test_path\n                    break\n        \n        # Verificar que el archivo existe\n        if not file_path.exists():\n            print(f"Archivo no encontrado: {file_path}")\n            return jsonify({"error": f"File not found: {file_path}"}), 404\n        \n        # Verificar que el archivo está en un directorio permitido\n        allowed_dirs = [REPORTS_FOLDER, SCREENSHOTS_FOLDER, EVIDENCE_FOLDER]\n        if not any(str(file_path).resolve().startswith(str(allowed_dir.resolve())) for allowed_dir in allowed_dirs):\n            return jsonify({"error": "Access denied: file not in allowed directory"}), 403\n        \n        # Enviar el archivo\n        return send_file(str(file_path), as_attachment=True)\n    except Exception as e:\n        print(f"Error al descargar archivo: {e}")\n        return jsonify({"error": f"Error downloading file: {str(e)}"}), 500'
            
            # Reemplazar la función en el contenido
            updated_content = content.replace(old_function, new_function)
            
            # Guardar el archivo actualizado
            with open(app2_path, 'w') as f:
                f.write(updated_content)
            
            print("Función download_file corregida")
            return True
        else:
            print("La función download_file parece tener un formato diferente al esperado")
            return False
    else:
        print("No se encontró la ruta de descarga en app2.py")
        return False

def main():
    """Función principal para verificar y corregir problemas de descarga."""
    print("=== Diagnóstico de problemas de descarga de archivos ===")
    
    # Verificar directorios
    reports_ok = check_directory(REPORTS_FOLDER, "REPORTS_FOLDER")
    screenshots_ok = check_directory(SCREENSHOTS_FOLDER, "SCREENSHOTS_FOLDER")
    evidence_ok = check_directory(EVIDENCE_FOLDER, "EVIDENCE_FOLDER")
    
    # Listar contenido de directorios
    list_directory_contents(REPORTS_FOLDER, "REPORTS_FOLDER")
    list_directory_contents(SCREENSHOTS_FOLDER, "SCREENSHOTS_FOLDER")
    list_directory_contents(EVIDENCE_FOLDER, "EVIDENCE_FOLDER")
    
    # Corregir ruta de descarga
    route_fixed = fix_download_route()
    
    # Resumen
    print("\n=== Resumen del diagnóstico ===")
    print(f"Directorio de informes: {'OK' if reports_ok else 'ERROR'}")
    print(f"Directorio de capturas: {'OK' if screenshots_ok else 'ERROR'}")
    print(f"Directorio de evidencias: {'OK' if evidence_ok else 'ERROR'}")
    print(f"Ruta de descarga: {'CORREGIDA' if route_fixed else 'SIN CAMBIOS'}")
    
    if reports_ok and screenshots_ok and evidence_ok and route_fixed:
        print("\nTodos los problemas han sido corregidos. La descarga de archivos debería funcionar correctamente ahora.")
    else:
        print("\nAlgunos problemas no pudieron ser corregidos automáticamente. Revise los mensajes anteriores para más detalles.")

if __name__ == "__main__":
    main()
