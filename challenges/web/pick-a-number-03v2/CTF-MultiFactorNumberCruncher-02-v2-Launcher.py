import subprocess

print("starting subprocesses")
print("starting WebSetup")
subprocess.Popen(['python3', '/app/CTF-MultiFactorNumberCruncher-02-v2-WebSetup.py'])
print("staring PythonLoop")
subprocess.Popen(['python3', '/app/CTF-MultiFactorNumberCruncher-02-v2-PythonLoop.py'])
print("startup done")
subprocess.run(['httpd', '-D', 'FOREGROUND'])
