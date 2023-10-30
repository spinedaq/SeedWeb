from django.db import models

class Experimento(models.Model):
    """
    Clase que representa un experimento en el sistema.
    Contiene información sobre el nombre del experimento, fechas de inicio y finalización, frecuencia de captura de imágenes, cantidad de imágenes capturadas, observaciones, cantidad de semillas, estado y progreso del experimento.
    """
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateTimeField(blank=True, editable=False, null=True)
    fecha_final = models.DateTimeField()
    frecuencia = models.FloatField()
    cantidad_imagenes = models.IntegerField(editable=False, null=True)
    imagenes_capturadas = models.IntegerField(editable=False, default=0)
    observaciones = models.CharField(max_length=200)
    cantidad_semillas = models.IntegerField()
    status = models.CharField(max_length=20, default="Creado", editable=False)
    progreso = models.FloatField(default=0, editable=False)

class Image(models.Model):
    """
    Clase que representa una imagen capturada en el contexto de un experimento.
    Almacena la imagen, la fecha de captura y se relaciona con un experimento.
    """
    photo = models.ImageField(upload_to='pics')
    fecha = models.DateTimeField()
    experimento = models.ForeignKey(Experimento, on_delete=models.CASCADE)

class Mask(models.Model):
    """
    Clase que representa una máscara asociada a una imagen capturada en el contexto de un experimento.
    Almacena la máscara, la fecha de creación y se relaciona con un experimento.
    """
    mask = models.ImageField(upload_to='masks')
    fecha = models.DateTimeField()
    experimento = models.ForeignKey(Experimento, on_delete=models.CASCADE)

class Semillas(models.Model):
    """
    Clase que representa datos de conteo de semillas para un experimento específico.
    Almacena la fecha de conteo, la cantidad de semillas germinadas y la cantidad de semillas no germinadas, y se relaciona con un experimento.
    """
    fecha = models.DateTimeField()
    germinadas = models.IntegerField()
    no_germinadas = models.IntegerField()
    experimento = models.ForeignKey(Experimento, on_delete=models.CASCADE)
