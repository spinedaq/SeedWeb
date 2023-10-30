import cv2
from datetime import datetime
import os

class VideoCamera(object):
    def __init__(self, Image):
        """
        Inicializa una instancia de la clase VideoCamera.

        Parámetros:
        - Image: Una clase (probablemente un modelo de Django) para manejar imágenes.
        """
        self.video = cv2.VideoCapture(0)  # Inicia la captura de video desde la cámara 0.
        self.Image = Image  # Almacena la clase de imagen para su posterior uso.

    def __del__(self):
        """
        Libera los recursos de la cámara cuando la instancia se destruye.
        """
        self.video.release()

    def get_frame(self):
        """
        Captura un marco de video desde la cámara, lo voltea horizontalmente y lo convierte en un objeto JPEG.

        Retorna:
        - jpeg_bytes: Los bytes de la imagen JPEG.
        """
        success, image = self.video.read()  # Captura un marco de video.
        frame_flip = cv2.flip(image, 1)  # Voltea horizontalmente la imagen.
        ret, jpeg = cv2.imencode('.jpg', frame_flip)  # Convierte la imagen en formato JPEG.
        return jpeg.tobytes()  # Retorna los bytes de la imagen JPEG.

    def save_frame(self, fecha, experimento):
        """
        Captura un marco de video desde la cámara, lo voltea horizontalmente, guarda la imagen en el sistema de archivos
        y crea un registro de imagen en la base de datos utilizando la clase Image.

        Parámetros:
        - fecha: La fecha y hora en la que se tomó la imagen.
        - experimento: Información sobre el experimento asociado a la imagen.

        Retorna:
        - path: La ruta donde se guardó la imagen en el sistema de archivos.
        - frame_flip: El marco de video volcado horizontalmente.
        """
        success, image = self.video.read()  # Captura un marco de video.
        frame_flip = cv2.flip(image, 1)  # Voltea horizontalmente la imagen.
        path = f"./images/{fecha.strftime('%m:%d:%Y_%H:%M:%S')}.jpg"  # Genera la ruta de archivo para la imagen.
        cv2.imwrite(path, frame_flip)  # Guarda la imagen en el sistema de archivos.

        # Crea un objeto de imagen en la base de datos utilizando la clase Image.
        image_obj = self.Image(fecha=fecha, experimento=experimento, photo=path)
        image_obj.save()

        return path, frame_flip  # Retorna la ruta del archivo y el marco de video volcado.


		