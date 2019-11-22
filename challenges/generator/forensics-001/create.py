import os
import pathlib
import time

challenge_name = "forensics-001"
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
        source_pic_length = len(source_pic_content)
        source_pic_length_90 = round(source_pic_length * 0.9)
        pic_output_bytes_1 = source_pic_content[0:source_pic_length_90]
        pic_output_bytes_2 = str.encode(flag)
        pic_output_bytes_3 = source_pic_content[source_pic_length_90:source_pic_length]
        pic_output_final = pic_output_bytes_1 + pic_output_bytes_2 + pic_output_bytes_3
        print(os.path.dirname(output_path))
        if not os.path.dirname(output_path):
            os.makedirs(os.path.dirname(output_path))
        file_object = open(output_path, "wb+")
        file_object.write(pic_output_final)
        print("I drew you a picture")
        print("")
        print("File with flag {} place in {}".format(flag, output_path))
        print("")
        print("Returning to menu in 5 seconds")
        time.sleep(5)
    except Exception as e:
        print("Error encoutnered")
        print("")
        print(e)
        print("")
        print("Returning to menu in 5 seconds")
        time.sleep(5)
