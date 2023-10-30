import cv2
from .models import Image
from datetime import datetime

class VideoCamera(object):
    """
    Clase para capturar video desde una cámara y guardar imágenes.

    Attributes:
        video: Instancia del objeto de captura de video de OpenCV.
        
    Methods:
        __init__(): Constructor de la clase que inicializa el objeto de captura de video.
        __del__(): Destructor que libera los recursos de la cámara al destruir la instancia.
        get_frame(): Captura un fotograma desde la cámara, lo invierte horizontalmente y lo devuelve en formato JPEG.
        save_frame(path, title): Captura y guarda un fotograma de la cámara en la ubicación especificada y crea un registro en la base de datos.

    """
    def __init__(self):
        """
        Inicializa un objeto de captura de video desde la cámara.
        """
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        """
        Destructor que libera los recursos de la cámara al destruir la instancia.
        """
        self.video.release()

    def get_frame(self):
        """
        Captura un fotograma desde la cámara, lo invierte horizontalmente y lo devuelve en formato JPEG.

        Returns:
            bytes: Imagen en formato JPEG.
        """
        success, image = self.video.read()
        frame_flip = cv2.flip(image, 1)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()

    def save_frame(self, path, title):
        """
        Captura y guarda un fotograma de la cámara en la ubicación especificada y crea un registro en la base de datos.

        Args:
            path (str): Ruta donde se guardará la imagen.
            title (str): Título de la imagen.

        Returns:
            None
        """
        success, image = self.video.read()
        frame_flip = cv2.flip(image, 1)
        cv2.imwrite(path, frame_flip)

        # Crea un registro en la base de datos para la imagen
        image = Image(title=title, photo=path, fecha=datetime.now())
        image.save()
