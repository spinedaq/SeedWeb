from django.apps import AppConfig

class SeedGuiConfig(AppConfig):
    """
    Configuración de la aplicación SeedGui.

    Esta clase de configuración define la configuración de la aplicación SeedGui.

    Attributes:
        default_auto_field (str): Campo automático predeterminado para modelos.
        name (str): Nombre de la aplicación.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seedgui'
