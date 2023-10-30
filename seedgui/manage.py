#!/usr/bin/env python
"""
Este script es la utilidad de línea de comandos de Django para tareas administrativas.
"""

import os
import sys

def main():
    """
    Función principal que ejecuta tareas administrativas.
    """
    # Configura la variable de entorno 'DJANGO_SETTINGS_MODULE' con la configuración del proyecto Django.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seedgui.settings')

    try:
        # Intenta importar el módulo 'execute_from_command_line' del paquete 'django.core.management'.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Estás seguro de que está instalado y disponible en tu variable de entorno PYTHONPATH? ¿Olvidaste activar un entorno virtual?"
        ) from exc

    # Ejecuta comandos desde la línea de comandos con los argumentos proporcionados en 'sys.argv'.
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    # Si este archivo es ejecutado directamente como un script, llama a la función 'main()'.
    main()
