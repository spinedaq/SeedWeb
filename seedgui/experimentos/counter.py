import tensorflow as tf
import cv2
import numpy as np

class Counter:
    """
    Clase que implementa un contador de objetos en imágenes utilizando un modelo de detección.
    Permite cargar un modelo TensorFlow o TensorFlow Lite y realizar predicciones en imágenes.

    Args:
        model_path (str): La ruta al archivo del modelo, que puede ser un archivo ".h5" (TensorFlow) o ".tflite" (TensorFlow Lite).

    Atributos:
        - `model` (tf.keras.Model): El modelo cargado desde un archivo ".h5" si se proporcionó un modelo TensorFlow.
        - `interpreter` (tf.lite.Interpreter): El intérprete del modelo cargado desde un archivo ".tflite" si se proporcionó un modelo TensorFlow Lite.
        - `input_details` (list): Los detalles de la entrada del modelo (solo para modelos TensorFlow Lite).
        - `output_details` (list): Los detalles de la salida del modelo (solo para modelos TensorFlow Lite).
        - `type` (str): El tipo de modelo cargado ("tf" para TensorFlow o "tflite" para TensorFlow Lite).

    Métodos:
        - `non_max_suppression_fast(boxes, classes, overlapThresh)`: Realiza la supresión de no máximos para eliminar detecciones duplicadas.
        - `predict(image)`: Realiza predicciones en una imagen y devuelve una imagen con las detecciones resaltadas y el conteo de objetos.

    """

    def __init__(self, model_path):
        """
        Inicializa la clase Counter cargando un modelo desde un archivo.

        Args:
            model_path (str): La ruta al archivo del modelo.
        """
        if model_path.endswith(".h5"):
            # Cargar un modelo TensorFlow desde un archivo ".h5"
            self.model = tf.keras.models.load_model(model_path)
            self.type = "tf"
        elif model_path.endswith(".tflite"):
            # Cargar un modelo TensorFlow Lite desde un archivo ".tflite"
            self.interpreter = tf.lite.Interpreter(model_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.type = "tflite"

    def non_max_suppression_fast(self, boxes, classes, overlapThresh=0.8):
        """
        Realiza la supresión de no máximos para eliminar detecciones duplicadas en cajas delimitadoras.

        Args:
            boxes (numpy.ndarray): Las cajas delimitadoras de objetos.
            classes (numpy.ndarray): Las clases asociadas a las cajas delimitadoras.
            overlapThresh (float): Umbral de superposición para determinar si dos cajas se superponen.

        Returns:
            boxes (numpy.ndarray): Cajas delimitadoras después de la supresión de no máximos.
            classes (numpy.ndarray): Clases asociadas a las cajas delimitadoras después de la supresión.
        """
        # Implementación de supresión de no máximos

    def predict(self, image):
        """
        Realiza predicciones en una imagen y devuelve una imagen con las detecciones resaltadas y el conteo de objetos.

        Args:
            image (numpy.ndarray): La imagen en la que se realizarán las predicciones.

        Returns:
            image (numpy.ndarray): La imagen original con las detecciones resaltadas.
            object_count (dict): Un diccionario con el conteo de objetos por clase.
        """
        # Implementación de la predicción

