from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from test.camera import VideoCamera
import time
from datetime import datetime
import os
from .models import Image
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime

@staff_member_required
def index(request):
    """
    Renderiza la página de inicio para usuarios con permisos de administrador.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: Respuesta HTTP que representa la página de inicio.
    """
    return render(request, 'test/index.html')

def gen(camera):
    """
    Generador para el video en vivo de la cámara.

    Args:
        camera (VideoCamera): Instancia de la cámara de video.

    Yields:
        bytes: Los fotogramas del video en formato JPEG.
    """
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@staff_member_required
def video_feed(request):
    """
    Transmite el video en vivo desde la cámara.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        StreamingHttpResponse: Respuesta HTTP que transmite el video en vivo.
    """
    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')

@staff_member_required
def captures(request):
    """
    Captura imágenes de la cámara y las guarda.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: Respuesta HTTP con los resultados de las capturas.
    """
    camera = VideoCamera()
    for i in range(5):
        title = datetime.now()
        camera.save_frame(title=title, path=f"./results/{title}.jpg")
        print("Saved image")
        time.sleep(1)
    return render(request, 'test/captures_results.html')

@staff_member_required
def captures_results(request):
    """
    Muestra las imágenes capturadas en el día actual.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: Respuesta HTTP que muestra las imágenes capturadas.
    """
    data = Image.objects.filter(fecha=datetime.today())
    context = {'data': data}
    return render(request, 'test/display_captures.html', context)
