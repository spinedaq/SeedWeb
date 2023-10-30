from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Experimento
from .models import Image
from .models import Semillas
from .models import Mask
from datetime import datetime, timedelta
from django.utils import timezone
from .camera import VideoCamera
import time
from django.contrib.admin.views.decorators import staff_member_required
from .segmentation import count
import cv2
from .forms import UploadFileForm
import plotly.express as px
import pandas as pd
from plotly.offline import plot
import io
from .counter import Counter

# Create your views here.

@staff_member_required
def index(request):
    """
    Muestra una página de inicio para usuarios con permisos de administrador.
    """
    return render(request, "experimentos/index.html")

@staff_member_required
def lista_experimentos(request):
    """
    Muestra una lista de experimentos almacenados en la base de datos.
    """
    data = Experimento.objects.all()
    context = {'experimentos': data}
    return render(request, 'experimentos/lista_experimentos.html', context)

@staff_member_required
def ver_experimento(request, experimento_id):
    """
    Muestra los detalles de un experimento específico.
    """
    experimento = get_object_or_404(Experimento, pk=experimento_id)
    context = {'experimento': experimento}
    return render(request, 'experimentos/detalle.html', context)

@staff_member_required
def iniciar_experimento(request, experimento_id):
    """
    Inicia un experimento específico, realiza capturas de imágenes y realiza el conteo de objetos en las imágenes.
    """
    experimento = get_object_or_404(Experimento, pk=experimento_id)

    experimento.fecha_inicio = timezone.now()
    experimento.status = 'Iniciado'

    tiempo_total = (experimento.fecha_final - experimento.fecha_inicio).total_seconds() / 3600
    total_imgs = int(tiempo_total / experimento.frecuencia)
    experimento.cantidad_imagenes = total_imgs
    experimento.save()

    camera = VideoCamera(Image)
    counter = Counter("./yolov8.tflite")

    for i in range(total_imgs):
        fecha = datetime.now()
        fecha_conteo = timezone.now()
        path, image = camera.save_frame(fecha, experimento)
        out_path = path.replace("images", "detection")

        result, count_ = counter.predict(image)

        conteo = Semillas(fecha=fecha_conteo, germinadas=count_['germinated'], no_germinadas=count_['no_germinated'], experimento=experimento)
        conteo.save()

        cv2.imwrite(out_path, result)
        mask = Mask(mask=out_path, experimento=experimento, fecha=fecha)
        mask.save()

        time.sleep(experimento.frecuencia * 3600)

        progreso = ((i + 1) / total_imgs) * 100
        experimento.progreso = progreso
        experimento.imagenes_capturadas += 1
        experimento.save()

    experimento.status = 'Finalizado'
    experimento.save()

    return HttpResponse("Experimento terminado.")

@staff_member_required
def mostrar_resultados(request, experimento_id):
    """
    Muestra los resultados de un experimento, incluyendo imágenes, máscaras y datos de conteo.
    """
    experimento = get_object_or_404(Experimento, pk=experimento_id)

    images = Image.objects.filter(experimento=experimento)
    masks = Mask.objects.filter(experimento=experimento)
    conteo = Semillas.objects.filter(experimento=experimento)

    if experimento.status == "Creado":
        conteo_data = [
            {
                'Fecha': 0,
                'Germinadas': 0,
                'No Germinadas': 0,
            }
        ]
    else:
        conteo_data = [
            {
                'Fecha': x.fecha,
                'Germinadas': x.germinadas,
                'No Germinadas': x.no_germinadas,
            } for x in conteo
        ]

    df = pd.DataFrame(conteo_data)
    
    fig = px.line(df, x="Fecha", y=["Germinadas", "No Germinadas"], markers=True)
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', gridcolor="LightGray")
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', gridcolor="LightGray")
    lista = zip(images, masks, conteo)
    fig_plot = plot(fig, output_type="div")
    context = {'experimento': experimento, 'lista': lista, 'plot_div': fig_plot}

    return render(request, 'experimentos/resultados.html', context)

@staff_member_required
def cargar_experimento(request):
    """
    Muestra una página para cargar un nuevo experimento.
    """
    return render(request, 'experimentos/cargar_experimento.html')

# Imaginary function to handle an uploaded file.
def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def download_csv(request, experimento_id):
    """
    Descarga los datos de conteo de un experimento en formato CSV.
    """
    experimento = get_object_or_404(Experimento, pk=experimento_id)

    conteo = Semillas.objects.filter(experimento=experimento)

    if experimento.status == "Creado":
        conteo_data = [
            {
                'Fecha': 0,
                'Germinadas': 0,
                'No Germinadas': 0,
            }
        ]
    else:
        conteo_data = [
            {
                'Fecha': x.fecha,
                'Germinadas': x.germinadas,
                'No Germinadas': x.no_germinadas,
            } for x in conteo
        ]

    df = pd.DataFrame(conteo_data)

    csv_bytes = io.BytesIO()
    df.to_csv(csv_bytes, index=False, encoding='utf-8')
    csv_bytes.seek(0)

    response = HttpResponse(csv_bytes, content_type='text/csv')
   
