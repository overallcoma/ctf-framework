import argparse
from PIL import ImageDraw, Image, ImageFont
from pydub import AudioSegment
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--flag", dest="flag", help="Flag to Use")
parser.add_argument("-m", "--merge", dest="merge_audio", help="File to Merge Spectrogram With (WAV file")
parser.add_argument("-o", "--output", dest="output_audio", help="Output Audio File Name")
args = parser.parse_args()
flag = args.flag

if args.flag is None:
    print("Please specify a flag with -f")
    exit(1)
else:
    flag = args.flag
    flag = flag.upper()
try:
    if args.merge_audio is None:
        do_merge = 0
    elif args.merge_audio:
        do_merge = 1
        merge_audio_file = args.merge_audio
except:
    print("Error handling the input audio")
    exit(1)
try:
    if args.output_audio:
        outputfilename = args.output_audio
    else:
        outputfilename = "./output.wav"
except:
    outputfilename = "./output.wav"

font_file_name = "./freemon.ttf"
spectrology_location = "./spectrology.py"
temporary_image_filename = "./temp_image.bmp"


def write_text_on_image(image_output, font, text, color):
    image_image = Image.new('RGB', (700, 100), (255, 255, 255))
    image_font = ImageFont.truetype(font, 40)
    image_text = text
    if color == "black":
        image_color = (0, 0, 0)
    elif color == "blue":
        image_color = (0, 0, 255)
    elif color == "green":
        image_color = (0, 255, 0)
    else:  # make it red
        image_color = (255, 0, 0)
    image_draw = ImageDraw.Draw(image_image)
    image_draw.text((10, 10), image_text, font=image_font, fill=image_color)
    image_image.save(image_output)


def merge_spectro_with_audio(spectro_audio, input_audio):
    spectro_audio = AudioSegment.from_file(spectro_audio, format="wav")
    input_audio = AudioSegment.from_file(input_audio, format="wav")
    silence_length = ((int(input_audio.duration_seconds) - int(spectro_audio.duration_seconds)) / 2)
    silent_audio = AudioSegment.silent(duration=(silence_length * 1000))
    buffered_spectro = silent_audio.append(spectro_audio)
    buffered_spectro = buffered_spectro.append(silent_audio)
    combined_audio = input_audio.overlay(buffered_spectro)
    return combined_audio


    # spectro_audio_length = spectro_audio.duration_seconds
    # input_audio_length = input_audio.duration_seconds
    # spectro_audio_half = int(spectro_audio_length / 2)
    # input_audio_half = int(input_audio_length / 2)
    # spectro_audio_start = int(input_audio_half - spectro_audio_half)
    # combined_audio = spectro_audio.overlay(input_audio, position=(spectro_audio_start / 1000))
    # return combined_audio


write_text_on_image(temporary_image_filename, font_file_name, flag, "black")
subprocess.call(['python', spectrology_location, '-i', temporary_image_filename, '-o', outputfilename, '-b', '15000', '-t', '20000'])
if do_merge == 1:
    print("Merging Audio")
    merged_audio = merge_spectro_with_audio(outputfilename, merge_audio_file)
    merged_audio.export(outputfilename, format="wav")


# Cleanup
os.remove(temporary_image_filename)
