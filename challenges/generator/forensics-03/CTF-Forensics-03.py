import argparse
from PIL import ImageDraw, Image, ImageFont
import zipfile
from shutil import copy
import os

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--flag", dest="flag", help="Flag Value")
parser.add_argument("-s", "--source_image", dest="source_image", help="Source Image to Use")
parser.add_argument("-rh", "--redherring", dest="redherring_flag", help="Red Herring Flag Value")
args = parser.parse_args()
flag = args.flag
if args.flag is None:
    print("Please specify a flag with -f")
    exit(1)
else:
    flag = args.flag
if args.source_image is None:
    print("Please specify an input source image with -s")
    exit(1)
else:
        source_image = args.source_image
if args.redherring_flag is None:
    print("This challenge requires a Fake Flag/Red Herring")
    print("Please specify a Red Herring with -rh")
    exit(1)
else:
    redherring_flag = args.redherring_flag


def write_text_on_image(image_input, image_output, font, text, color):
    image_image = Image.new('RGBA', (700, 100), (255, 255, 255, 0))
    image_font = ImageFont.truetype(font, 40)
    image_text = text
    if color == "blue":
        image_color = (0, 0, 255)
    elif color == "green":
        image_color = (0, 255, 0)
    else:  # make it red
        image_color = (255, 0, 0)
    image_draw = ImageDraw.Draw(image_image)
    image_draw.text((10, 10), image_text, font=image_font, fill=image_color)
    image_image.save(image_output)
    image_background = Image.open(image_input)
    image_foreground = Image.open(image_output)
    image_background.paste(image_foreground, (0, 0), image_foreground)
    image_background.save(image_output)


def hide_zip_in_image(outer_image, outer_image_output, inner_image, inner_image_output, zip_name):
    copy(inner_image, inner_image_output)
    zipfile.ZipFile(zip_name, mode='w').write(inner_image_output)
    system_command = "cat {0} {1} > {2}".format(outer_image, zip_name, outer_image_output)
    os.system(system_command)


flag_image_name = "./flag_image.png"
redherring_image_name = "./fake_image.png"
font_file_name = "./freemon.ttf"
outer_image_filename = "./redfish.png"
inner_image_filename = "./secrets.png"
hidden_zip_filename = "./bluefish.zip"

background_image_name = source_image

write_text_on_image(background_image_name, redherring_image_name, font_file_name, redherring_flag, "red")
write_text_on_image(background_image_name, flag_image_name, font_file_name, flag, "blue")

hide_zip_in_image(redherring_image_name, outer_image_filename, flag_image_name, inner_image_filename, hidden_zip_filename)

os.remove(flag_image_name)
os.remove(redherring_image_name)
os.remove(inner_image_filename)
os.remove(hidden_zip_filename)

print("I made a secret picture for you")
