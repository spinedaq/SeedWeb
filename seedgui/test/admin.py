from django.contrib import admin
from .models import Image

class imageAdmin(admin.ModelAdmin):
    """
    Clase personalizada para administrar el modelo 'Image' en el panel de administración de Django.

    Attributes:
        list_display (list): Una lista de campos del modelo 'Image' que se mostrarán en la lista de objetos en el panel de administración.

    """
    list_display = ["title", "photo"]

# Registrar el modelo 'Image' junto con la clase 'imageAdmin' para personalizar su administración.
admin.site.register(Image, imageAdmin)
