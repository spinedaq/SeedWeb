# Generated by Django 4.1.2 on 2022-11-16 19:52

import datetime
from django.db import migrations, models

class Migration(migrations.Migration):
    """
    Representa una migración generada por Django.

    Attributes:
        dependencies (list): Lista de dependencias de migración para esta migración.
        operations (list): Lista de operaciones que se realizarán durante esta migración.

    """

    dependencies = [
        ('test', '0001_initial'),  # Dependencia de otra migración llamada '0001_initial' en la aplicación 'test'.
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2022, 11, 16, 19, 52, 17, 810860)),
            preserve_default=False,
        )
    ]
