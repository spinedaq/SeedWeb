from django.apps import AppConfig

class TestConfig(AppConfig):
    """
    Configuración de la aplicación 'test'.

    Esta clase define la configuración de la aplicación 'test' en el proyecto Django.

    Attributes:
        default_auto_field (str): Especifica el campo de clave principal automática utilizado por los modelos. 
        name (str): Especifica el nombre de la aplicación.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test'
