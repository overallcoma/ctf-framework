import os
import time
import subprocess

path = os.path.abspath(__file__)
directory = os.path.dirname(path)
os.chdir(directory)

environment_file_name = "./.env"

environment_file = open(environment_file_name, "r")
environment_data = environment_file.readlines()
environment_file.close()
dictionary = {}
for line in environment_data:
    line = line.replace("\n", "")
    key_value = {line.split("=", 1)[0]: line.split("=", 1)[1]}
    dictionary.update(key_value)

for key, value in dictionary.items():
    key_value = {key: value}
    print("")
    new_value = input("Please select a value for " + key + " (" + value + "):")
    if new_value == '':
        new_value = value
    key_value = {key: new_value}
    dictionary.update(key_value)

os.remove(environment_file_name)
environment_file = open(environment_file_name, "w+")

for key, value in dictionary.items():
    out_string = key + "=" + value + "\n"
    environment_file.write(out_string)

environment_file.close()

print("Deploying theraven-001")
subprocess.run(["docker-compose", "up", "-d"])
print("Returning to menu")
time.sleep(3)
