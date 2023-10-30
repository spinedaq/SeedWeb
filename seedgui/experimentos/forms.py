from django import forms

class UploadFileForm(forms.Form):
    """
    Clase que define un formulario para cargar archivos en la aplicación web.
    Permite a los usuarios cargar archivos, incluyendo un título y un archivo en sí.
    """
    title = forms.CharField(max_length=50)
    file = forms.FileField()

