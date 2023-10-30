from django.contrib import admin
from .models import Experimento

class experimentoAdmin(admin.ModelAdmin):
    """
    Clase que personaliza la administración del modelo Experimento en el panel de administración de Django.
    Define cómo se mostrarán los datos del modelo y qué campos serán visibles en la lista de experimentos.

    Atributos:
        - `list_display` (list): Una lista de nombres de campos que se mostrarán en la lista de experimentos en el panel de administración.

    """
    list_display = ["nombre", "fecha_inicio", "fecha_final", "status"]

# Registrar el modelo Experimento en el panel de administración utilizando la clase experimentoAdmin
admin.site.register(Experimento, experimentoAdmin)
