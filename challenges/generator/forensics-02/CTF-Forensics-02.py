import argparse
import subprocess


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
            subprocess.call(["python3-pip", "install", "piexif"])
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
            subprocess.call(["python3-pip", "install", "Pillow"])
    except Exception as e:
        print("Unable to install required module")
        print(e)
        exit()

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--source", dest="source_pic", help="Source picture to use")
parser.add_argument("-f", "--flag", dest="flag", help="Flag to Use")

args = parser.parse_args()

source_pic = args.source_pic
flag = args.flag

if source_pic is None:
    print("please supply an input jpg picture (1920x1080 preferred)")

if flag is None:
    print("please specify a flag with -f")
    exit(1)

source_pic_content = open(source_pic, "rb")
source_pic_content = source_pic_content.read()
output_file = "./output.jpg"
file_object = open(output_file, "wb+")
file_object.writelines(source_pic_content)

im = Image.open(output_file)
exif_dict = piexif.load(im.info["exif"])
exif_dict["0th"][piexif.ImageIFD.ProcessingSoftware] = bytearray(flag, 'utf-8')
exif_bytes = piexif.dump(exif_dict)
im.save(output_file, "jpeg", exif=exif_bytes)
print("I drew you a picture")
