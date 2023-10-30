# Generated by Django 4.1.3 on 2022-11-26 21:23

from django.db import migrations, models

class Migration(migrations.Migration):
    """
    Clase de migración generada por Django que representa un cambio en la base de datos.
    La migración modifica el campo "frecuencia" en el modelo "Experimento".

    Atributos:
        - `dependencies` (list): Una lista de dependencias de otras migraciones.
        - `operations` (list): Una lista de operaciones que se realizarán durante la migración.
    """

    dependencies = [
        ('experimentos', '0007_alter_experimento_cantidad_imagenes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimento',
            name='frecuencia',
            field=models.FloatField(),
        ),
    ]