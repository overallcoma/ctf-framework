import subprocess
import pathlib
import os
import time


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
    import piexif
except ImportError as e:
    try:
        print("")
        import_piexif = yes_no_input("Piexif is not present.  Would you like to install this module?")
        if import_piexif == 1:
            subprocess.call(["pip3", "install", "piexif"])
    except Exception as e:
        print("Unable to install required module")
        print(e)
        exit()

try:
    from PIL import Image
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

challenge_name = "forensics-002"
output_file = "output.jpg"

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
    try:
        source_pic_content = open(source_pic, "rb")
        source_pic_content = source_pic_content.read()
        file_object = open(output_path, "wb+")
        file_object.writelines(source_pic_content)

        im = Image.open(output_path)
        exif_dict = piexif.load(im.info["exif"])
        exif_dict["0th"][piexif.ImageIFD.ProcessingSoftware] = bytearray(flag, 'utf-8')
        exif_bytes = piexif.dump(exif_dict)
        im.save(output_path, "jpeg", exif=exif_bytes)
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
