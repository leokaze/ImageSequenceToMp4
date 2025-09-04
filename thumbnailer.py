print("start of the thumbnailer")

import sys
import os
import re
import ffmpeg
# import time
import time
import subprocess
from PIL import Image, ImageOps

args = ' '.join(sys.argv[1:])
filename_with_extension = os.path.basename(args)
filename, extension = os.path.splitext(filename_with_extension)
filepath = os.path.dirname(args)

print("ARGS: ", args)
print("Filename: ", filename)
print("Filepath: ", filepath)

# obtener la duración del video
duration = ffmpeg.probe(args)['format']['duration']
print("Duration: ", duration)

num_thumbnails_rows = 3
num_thumbnails_columns = 2
thumbnail_width = 1080

num_thumbnails = num_thumbnails_rows * num_thumbnails_columns

# crear un array con los tiempos de los thumbnails en formato HH:MM:SS
times=[]
for i in range(num_thumbnails):
    second = i * (float(duration) / num_thumbnails)
    # convertir el tiempo en segundos a formato HH:MM:SS
    t = time.strftime('%H:%M:%S', time.gmtime(second))
    times.append(t)

print("Times: ", times)

def get_frame(video_path, _time):
    """
    Obtiene una instantánea de un frame específico de un video.

    :param video_path: Ruta al archivo de video.
    :param output_image_path: Ruta donde se guardará la imagen.
    :param time: Tiempo en el video del frame deseado (formato: "HH:MM:SS").
    """
    # quitar los dos puntos de la cadena de tiempo
    t = _time.replace(':', '_')
    output_image_path = filepath + '/' + filename + '_thumbnail_' + t + '.jpg'
    command = [
        'ffmpeg',
        '-ss', _time,           # Especifica el tiempo del frame deseado
        '-i', video_path,      # Especifica el archivo de video de entrada
        '-vframes', '1',       # Extrae solo un frame
        '-q:v', '2',           # Establece la calidad de la imagen (1 es la mejor calidad, 31 es la peor)
        output_image_path      # Especifica el archivo de imagen de salida
    ]
    
    # Ejecuta el comando
    subprocess.run(command, check=True)

    return output_image_path
    

# Crear los thumbnails
image_paths = []
for t in times:
    image_path = get_frame(args, t)
    image_paths.append(image_path)

print("Image paths: ", image_paths)

# UNIR LAS IMÁGENES EN UNA SOLA IMAGEN

def join_thumbnails(image_paths, output_image_path, total_width=1080, separation=5, background_color=(128, 128, 128), num_columns=2, num_rows=2):
    """
    Une varias imágenes en una cuadrícula con una separación específica y un fondo de color,
    y ajusta la imagen resultante a un ancho específico.

    :param image_paths: Lista de rutas de las imágenes a unir.
    :param output_image_path: Ruta donde se guardará la imagen unida.
    :param total_width: Ancho total de la imagen resultante.
    :param separation: Espacio en píxeles entre las imágenes.
    :param background_color: Color de fondo (RGB).
    :param num_columns: Número de imágenes en cada fila.
    :param num_rows: Número de imágenes en cada columna.
    """
    # Verificar que haya suficientes imágenes
    if len(image_paths) < num_columns * num_rows:
        raise ValueError("No hay suficientes imágenes para llenar la cuadrícula.")

    # Abrir las imágenes
    images = [Image.open(path) for path in image_paths[:num_columns * num_rows]]

    # Calcular el ancho y alto individual para las imágenes
    total_separation_width = separation * (num_columns - 1)
    available_width = total_width - total_separation_width
    individual_width = available_width // num_columns

    # Calcular el alto individual en función de la relación de aspecto de la primera imagen
    aspect_ratio = images[0].height / images[0].width
    individual_height = int(individual_width * aspect_ratio)

    # Redimensionar las imágenes manteniendo la relación de aspecto
    resized_images = [img.resize((individual_width, individual_height)) for img in images]

    # Calcular el alto total de la imagen de salida
    total_separation_height = separation * (num_rows - 1)
    total_height = (individual_height * num_rows) + total_separation_height

    # Crear imagen de fondo
    combined_image = Image.new('RGB', (total_width, total_height), background_color)

    # Pegar imágenes en una cuadrícula
    for row in range(num_rows):
        for col in range(num_columns):
            img = resized_images[row * num_columns + col]
            x_offset = col * (individual_width + separation)
            y_offset = row * (individual_height + separation)
            combined_image.paste(img, (x_offset, y_offset))

    # Guardar la imagen de salida
    combined_image.save(output_image_path)


# Unir las imágenes en una sola imagen
thumbnail_path = filepath + '/' + filename + '_thumbnails.jpg'
join_thumbnails(image_paths, thumbnail_path, num_columns=num_thumbnails_columns, num_rows=num_thumbnails_rows, total_width=thumbnail_width)

# eliminar las imágenes individuales
for image_path in image_paths:
    os.remove(image_path)