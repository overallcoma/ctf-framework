import argparse
import random
import subprocess
import os

image_name = "ctf/pick-a-number-01"
container_name = "pick-a-number-01"

randomnumber = random.randint(1, 10000)
randomnumber = str(randomnumber)
flagpagename = randomnumber + ".html"

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--flag", dest="flag", help="Flag to Use")
args = parser.parse_args()

flag = args.flag

if flag == None:
    print("please specify a flag with -f")
    exit(1)


def replace_string_in_file(targetfile, newstring, newfile):
    filecontent = open(targetfile, 'r')
    filecontent = filecontent.read()
    newfilecontent = filecontent.replace('---STRINGREPLACE---', newstring)
    newfile_write = open(newfile, 'w+')
    newfile_write(newfilecontent)
    newfile_write.close()


target_page_tempname = "targetpage-withflag.html"
replace_string_in_file('./pages/targetpage.html', flag, "targetpage-withflag.html")

subprocess.call(["docker", "build", "-t", image_name, "."])
container_name = container_name + "-" + str(randomnumber)
subprocess.call(["docker", "run", "-d", "--restart", "unless-stopped", "--name", container_name, image_name])

os.remove(target_page_tempname)
