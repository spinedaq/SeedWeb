#!/usr/bin/python3
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import cv2

def mask2categorical(Mask: tf.Tensor, labels: dict) -> tf.Tensor:
    """
    Convierte una máscara RGB (3 canales) en una imagen de clases ordinales.

    Parámetros:
    - Mask: Un tensor de TensorFlow que representa la máscara de entrada.
    - labels: Un diccionario que asigna etiquetas a colores RGB.

    Retorna:
    - Un tensor de TensorFlow que representa la imagen de clases ordinales.
    """
    assert type(labels) == dict, "labels variable should be a dictionary"

    X = Mask

    if X.dtype == "float32":
        X = tf.cast(X*255, dtype="uint8")

    Y = tf.zeros(X.shape[0:2], dtype="float32")
    for i, key in enumerate(labels):
        Y = tf.where(np.all(X == labels[key], axis=-1), i, Y)
    Y = tf.cast(Y, dtype="uint8")
    return Y

def draw_boxes(img, boxes, color):
    """
    Dibuja cajas delimitadoras alrededor de objetos en una imagen.

    Parámetros:
    - img: La imagen de entrada en la que se dibujarán las cajas.
    - boxes: Una lista de coordenadas de cajas delimitadoras.
    - color: El color de las cajas.

    Retorna:
    - Una nueva imagen con las cajas delimitadoras dibujadas.
    """
    X = img.copy()
    
    for i, box in enumerate(boxes):
        pt1 = box[:2]
        pt2 = pt1 + box[2:4] 
        pt1 = tuple(pt1.tolist())
        pt2 = tuple(pt2.tolist())
        X = cv2.rectangle(X, pt1, pt2, color, 2)

    return X

def filter_boxes(stats):
    """
    Filtra las cajas delimitadoras en función de ciertas estadísticas.

    Parámetros:
    - stats: Una lista de estadísticas de cajas delimitadoras.

    Retorna:
    - Un arreglo NumPy que contiene las cajas delimitadoras filtradas.
    """
    boxes = []
    for i, stat in enumerate(stats):
        if stat[-1] > 1200 and i != 0:
            boxes.append(stat[:-1])
    return np.array(boxes)

def display(display_list):
    """
    Muestra una lista de imágenes en una ventana gráfica.

    Parámetros:
    - display_list: Una lista de imágenes para mostrar.

    No retorna ningún valor; muestra las imágenes en una ventana gráfica.
    """
    plt.figure(figsize=(15, 15))

    title = ['Input Image', 'Predicted Mask']

    for i in range(len(display_list)):
        plt.subplot(1, len(display_list), i+1)
        plt.title(title[i])
        plt.imshow(tf.keras.preprocessing.image.array_to_img(display_list[i]))
        plt.axis('off')
    plt.show()

def categorical2mask(X, labels):
    """
    Convierte una imagen de clases ordinales en una máscara RGB.

    Parámetros:
    - X: Una imagen de clases ordinales.
    - labels: Un diccionario que asigna etiquetas a colores RGB.

    Retorna:
    - Una máscara RGB que representa la imagen de clases ordinales.
    """
    Y = np.zeros(X.shape[0:2] + [3], dtype="uint8")
    for i, key in enumerate(labels):
        Y[..., 0] = np.where(X == i, labels[key][0], Y[..., 0])
        Y[..., 1] = np.where(X == i, labels[key][1], Y[..., 1])
        Y[..., 2] = np.where(X == i, labels[key][2], Y[..., 2])
    return Y

def count(img_path, out_path, model_path, img_size=224, classes=3):
    """
    Realiza el conteo de objetos en una imagen y devuelve un resultado visual.

    Parámetros:
    - img_path: La ruta de la imagen de entrada.
    - out_path: La ruta para guardar la máscara predicha.
    - model_path: La ruta del modelo de clasificación previamente entrenado.
    - img_size: El tamaño al que se redimensiona la imagen.
    - classes: El número de clases en la clasificación.

    Retorna:
    - Una imagen con cajas delimitadoras dibujadas alrededor de los objetos y un diccionario con el recuento de cada clase.
    """
    labels = {'background': np.array([0, 0, 0]), 
              'germinated': np.array([255, 0, 0]), 
              'no_germinated': np.array([255, 255, 0])}

    img = plt.imread(img_path) / 255
    X = tf.convert_to_tensor(img)
    X = tf.image.resize(X, (img_size, img_size))
    X = tf.expand_dims(X, 0)

    model = tf.keras.models.load_model(model_path)

    Y = model.predict(X)
    Y_classes = Y[0].copy()
    Y_classes = np.where(Y_classes > 0.5, 1, 0)
    Y_classes = np.array(cv2.resize(Y_classes, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST))
    Y_classes = (Y_classes * 255).astype('uint8')

    Y = tf.argmax(Y, axis=-1)
    Y = categorical2mask(Y[0], labels)
    Y = cv2.resize(Y, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)

    mask = mask2categorical(Y, labels).numpy()

    count_s, n_img, stats_n, centroids = cv2.connectedComponentsWithStats(Y_classes[:, :, 2])
    count_n, n_img, stats_s, centroids = cv2.connectedComponentsWithStats(Y_classes[:, :, 1])

    boxes_s = filter_boxes(stats_s)
    boxes_n = filter_boxes(stats_n)

    result = draw_boxes((img * 255).astype("uint8"), boxes_s, tuple([0, 255, 0]))
    result = draw_boxes(result, boxes_n, tuple([255, 0, 0]))

    print("Cantidad de semillas germinadas: ", boxes_s.shape[0])
    print("Cantidad de semillas no germinadas: ", boxes_n.shape[0])

    return result, {'germinadas': boxes_s.shape[0], 'no_germinadas': boxes_n.shape[0]}

# Uso de la función count:
result_img, counts = count("input_image.jpg", "predicted_mask.png", "model.h5", img_size=224, classes=3)
print(counts)
