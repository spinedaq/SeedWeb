from django.db import models

class Image(models.Model):
    """
    Modelo que representa imágenes capturadas.

    Attributes:
        title (str): Título de la imagen con un máximo de 20 caracteres.
        photo (FileField): Campo para cargar la imagen.
        fecha (DateField): Fecha de la captura de la imagen.
    """

    title = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='pics')
    fecha = models.DateField()

    def __str__(self):
        """
        Devuelve una representación legible en cadena de la instancia de Image.

        Returns:
            str: Representación en cadena del modelo Image.
        """
        return self.title
