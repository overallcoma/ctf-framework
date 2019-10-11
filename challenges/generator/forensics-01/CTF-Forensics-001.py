import argparse

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
source_pic_length = len(source_pic_content)
source_pic_length_90 = round(source_pic_length * 0.9)
pic_output_bytes_1 = source_pic_content[0:source_pic_length_90]
pic_output_bytes_2 = str.encode(flag)
pic_output_bytes_3 = source_pic_content[source_pic_length_90:source_pic_length]
pic_output_final = pic_output_bytes_1 + pic_output_bytes_2 + pic_output_bytes_3
file_object = open(output_file, "wb+")
file_object.write(pic_output_final)

print("I drew you a picture")
