import argparse
import piexif
from PIL import Image

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
