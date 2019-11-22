import argparse
import subprocess
import os

image_name = "ctf/advancedweb-02"
container_name = "ctf-advancedweb-02"
flagpagename = "flag.txt"

# Parse the flag argument
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--flag", dest="flag", help="Flag to Use")
args = parser.parse_args()
flag = args.flag
if flag == None:
    print("please specify a flag with -f")
    exit(1)


# Compile the binaries
def gpp_build(input_cpp, output_name):
    with_path_input = "./files-replacements/" + input_cpp
    with_path_output = "./files-replacements/" + output_name
    subprocess.call(["g++", with_path_input, "-o", with_path_output])


programs_to_compile = [
    "awk",
    "cat",
    "echo",
    "grep",
    "head",
    "sed",
    "tac",
    "tail",
    "tee"
]
for program in programs_to_compile:
    with_cpp_extension = program + ".cpp"
    gpp_build(with_cpp_extension, program)


# Write the flag target file
file = open(flagpagename, 'w+')
file.write(flag)
file.close()

# Create the Docker Container
subprocess.call(["docker", "build", "-t", image_name, "."])
subprocess.call(["docker", "run", "-d", "--restart", "unless-stopped", "--name", container_name, image_name])

# File Clean-up
files_to_remove = ["./files-replacements/awk",
                   "./files-replacements/cat",
                   "./files-replacements/grep",
                   "./files-replacements/head",
                   "./files-replacements/sed",
                   "./files-replacements/tail",
                   "./files-replacements/tac",
                   "./files-replacements/tee",
                   "./files-replacements/echo",
                   "./flag.txt"]
for file in files_to_remove:
    print("Deleting {0}".format(file))
    os.remove(file)
