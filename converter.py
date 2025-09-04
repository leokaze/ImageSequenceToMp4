
print("********************************Start of the converter************************")

import sys
import os
import re
import ffmpeg

args = ' '.join(sys.argv[1:])
filename_with_extension = os.path.basename(args)
filename, extension = os.path.splitext(filename_with_extension)

print(args)
print(filename)

# Buscar todos los dígitos al final del nombre del archivo
match = re.search(r'\d+$', filename)

if match:
    num_digits = len(match.group())
    start_frame = int(match.group())
    # convertir la secuencia de imágenes en un video mp4
    input_filename = filename[0:-num_digits]
    video_filename = input_filename
    if(video_filename[-1] == '_'):
        video_filename = video_filename[0:-1]
    input_path = os.path.dirname(args) + '/' + input_filename + '%0' + str(num_digits) + 'd' + extension
    output_path = os.path.dirname(args).split('\\')
    output_path = '/'.join(output_path[0:-1]) + '/' + video_filename + '.mp4'
    (
        ffmpeg
        .input(input_path, framerate=24, start_number=start_frame)
        .output(output_path, vcodec='libx264', pix_fmt='yuv420p', vb='2500k', preset='slow')
        .run()
    )
    print("MP4 file created successfully")
else:
    print("The filename does not end with any digits.")

print("End of the converter")
