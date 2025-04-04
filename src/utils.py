import os
import sys

def resource_path(relative_path):
    """
    Obtiene la ruta correcta para los archivos, ya sea en desarrollo o en un ejecutable empaquetado.
    """
    try:
        # Para cuando se ejecuta el archivo empaquetado
        base_path = sys._MEIPASS
    except Exception:
        # Para cuando se ejecuta el archivo directamente desde el código fuente
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)
