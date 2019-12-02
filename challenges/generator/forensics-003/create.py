import subprocess
import pathlib
import os
import time
import zipfile
from shutil import copy


def yes_no_input(prompt_string):
    response_error = "Invalid Selection"
    while response_error == "Invalid Selection":
        prompt_string_yn = prompt_string + " (Y/N):"
        response = input(prompt_string_yn)
        response = response.lower().strip()
        if response[0] == "y":
            return 1
        if response[0] == "n":
            return 0
    print(response_error)


try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    try:
        print("")
        import_piexif = yes_no_input("Pillow is not present.  Would you like to install this module?")
        if import_piexif == 1:
            subprocess.call(["pip3", "install", "Pillow"])
    except Exception as e:
        print("Unable to install required module")
        print(e)
        exit()

challenge_name = "forensics-003"
output_file = "output.png"

print("")
source_pic = input("Please enter the file path for the picture to be altered: ")
print("")
output_path = os.path.join(str(pathlib.Path.home()), challenge_name, output_file)
print("")
change_output_path = input("Please select output path ({})".format(output_path))
if change_output_path:
    output_path = change_output_path
if os.path.exists(source_pic):
    print("")
    flag = input("Please enter the flag to be injected: ")
    redherring_flag = input("Please enter the red herring flag to be injected: ")
    try:
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
        outer_image_filename = output_path
        inner_image_filename = "./secrets.png"
        hidden_zip_filename = "./bluefish.zip"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        background_image_name = source_pic

        write_text_on_image(background_image_name, redherring_image_name, font_file_name, redherring_flag, "red")
        write_text_on_image(background_image_name, flag_image_name, font_file_name, flag, "blue")

        hide_zip_in_image(redherring_image_name, outer_image_filename, flag_image_name, inner_image_filename, hidden_zip_filename)

        os.remove(flag_image_name)
        os.remove(redherring_image_name)
        os.remove(inner_image_filename)
        os.remove(hidden_zip_filename)
        print("")
        print("I drew you a picture")
        print("")
        print("File with flag {} place in {}".format(flag, output_path))
        print("")
        print("Returning to menu in 5 seconds")
        time.sleep(5)
    except Exception as e:
        print("")
        print("Error creating image")
        print("")
        print(e)
        print("")
        print("Returning to menu in 5 seconds")
        time.sleep(5)
