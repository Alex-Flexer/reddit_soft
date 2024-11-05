from PIL import Image
from moviepy.editor import VideoFileClip
import os


def convert_to_png(input_path, output_folder='output'):
    filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_folder, f"{filename}.png")

    with Image.open(input_path) as img:
        img.save(output_path, 'PNG')
        print(f"Converted '{input_path}' to '{output_path}'")


def convert_to_mp4(input_path, output_folder='output'):
    filename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_folder, f"{filename}.mp4")

    with VideoFileClip(input_path) as video:
        video.write_videofile(output_path, codec='libx264')
        print(f"Converted '{input_path}' to '{output_path}'")
