from django.apps import AppConfig

class ExperimentosConfig(AppConfig):
    """
    Clase de configuración de la aplicación "experimentos" en el proyecto Django.
    Define la configuración específica de esta aplicación, como el nombre y el campo de clave principal automática.

    Atributos:
        - `default_auto_field` (str): El nombre del campo de clave principal automática utilizado por los modelos de esta aplicación.
        - `name` (str): El nombre de la aplicación.

    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'experimentos'
