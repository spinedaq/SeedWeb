from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from test.camera import VideoCamera
import time
from datetime import datetime
import os
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    """
    Vista que renderiza la página de inicio.

    Args:
        request (HttpRequest): La solicitud HTTP enviada por el cliente.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la página de inicio.

    """
    return render(request, 'seedgui/index.html')
