import os
import re


entorno_virtual = None
# Verifica si la variable VIRTUAL_ENV está establecida
if "VIRTUAL_ENV" in os.environ:
    # Obtiene la ruta del entorno virtual
    entorno_virtual = os.environ["VIRTUAL_ENV"]
    # Si necesitas la carpeta raíz del entorno virtual
    entorno_virtual = re.sub(r"venv", "", entorno_virtual)
