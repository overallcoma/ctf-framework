import subprocess
import time

print("starting subprocesses")
print("starting WebSetup")
subprocess.Popen(['python3', '/app/CTF-MultiFactorNumberCruncher-WebSetup.py'])
print("staring PythonLoop")
subprocess.Popen(['python3', '/app/CTF-MultiFactorNumberCruncher-PythonLoop.py'])
print("startup done")
while True:
    time.sleep(1000)
