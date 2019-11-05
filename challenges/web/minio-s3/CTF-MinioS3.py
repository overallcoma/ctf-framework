import argparse
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
import os
from shutil import copyfile

parser = argparse.ArgumentParser()
parser.add_argument("-cn", "--container-name", dest="containername", help="Name of container to create")
parser.add_argument("-p", "--port", dest="port", help="External Port to attach to")
parser.add_argument("-nn", "--net-name", dest="netname", help="Name of network to attach to")
parser.add_argument("-ak", "--accesskey", dest="accesskey", help="Optional - Specify your Access Key for Minio")
parser.add_argument("-sk", "--secretkey", dest="secretkey", help="Optional - Specify your Secret Key for Minio")
parser.add_argument("-bu", "--bucket", dest="bucket", help="Optional - Create a bucket in Minio")
parser.add_argument("-files", "--files", dest="files", help="specify files to add to bucket - requires -bu/--bucket be specified")
parser.add_argument("-ts", "--torservice", dest="torservice", help="Name of service if attaching to Tor Proxy")
parser.add_argument("-tp", "--torproxy", dest="torproxy", help="Name of the Tor Proxy to Use")
args = parser.parse_args()

if args.containername is None:
    print("Please specify a name for the container with -cn")
    exit(1)
if args.port is None:
    print("You can specify an external port to attach to the required port 9000")
    print("If you do not specify a port here, you can manually attach set up a port later")
    print(" ")
if args.netname is None:
    print("You can specify the network to attach this container to with -nn")
    print("If you do not specify the network name, it will use your default network")
    print(" ")
if args.accesskey is None:
    print("You can specify and Access Key to use in Minio with -ak")
    print("If you do not specify an access key, one will be automatically generated for you")
    print(" ")
if args.secretkey is None:
    print("You can specify a Secret Key for use in Minio with -sk")
    print("If you do not specify a secret key, one will be automatically generated for you")
    print(" ")
if args.bucket is None:
    print("You can create a bucket automatically by using -bu")
    print("If you do not specify a bucket name, no buckets will be created automatically")
if args.files is None:
    print("You can specify files to upload by using -files")
    print("This requires you also use the --bucket command and create a default bucket")
    print('Please specify multiple files in format "file1.ext file2.ext file3.ext"')
    print(" ")
if args.torservice is None:
    print("You can specify a tor service name if attaching to a Tor Network using -ts")
    print("If you do not specify this, no tor parameter will be used")
    print(" ")
    if args.torservice is not None:
        if args.torproxy is None:
            print("You must specify the name of the Tor Container when using a Tor Proxy.  Please do this with -tp")
            print(" ")
            exit(1)

container_name = " "
minio_port = " "
network_attach = " "
accesskey = " "
secretkey = " "
bucket_create = " "
files_add = []
torenable = False
torport = " "

container_name = args.containername
if args.port is not None:
    minio_port = args.port
if args.netname is not None:
    network_attach = args.netname
if args.accesskey is not None:
    accesskey = args.accesskey
if args.secretkey is not None:
    secretkey = args.secretkey
if args.bucket is not None:
    bucket_create = args.bucket
    if args.files is not None:
        files_list = args.files
if args.torservice is not None:
    torenable = True
    tor_service_name = args.torservice
    tor_proxy_name = args.torproxy

docker_run_list = ["docker", "run", "-d", "--name", container_name, "-v", "/minio/data:/data", "-v", "/minio/config:/root/.minio"]
if args.port is not None:
    docker_run_list.append("-p")
    minio_port = minio_port + ":9000"
    docker_run_list.append(minio_port)
if args.netname is not None:
    docker_run_list.append("--net")
    docker_run_list.append(network_attach)
if args.accesskey is not None:
    docker_run_list.append("-e")
    docker_run_list.append(accesskey)
if args.secretkey is not None:
    docker_run_list.append("-e")
    docker_run_list.append(secretkey)
if args.torservice is not None:
    docker_run_list.append("-e")
    hiddenservicestring = "HIDDENSERVICE_NAME=" + tor_service_name
    docker_run_list.append(hiddenservicestring)
    docker_run_list.append("-e")
    hiddenserviceportstring = "HIDDENSERVICE_PORT=9000"
    docker_run_list.append(hiddenserviceportstring)

docker_run_list.append("minio/minio")
docker_run_list.append("server")
docker_run_list.append("/data")

call(docker_run_list)

if args.bucket is not None:
    print("Copying files")
    bucket_path = '/minio/data/' + bucket_create
    if not os.path.exists(bucket_path):
        os.makedirs(bucket_path)
    if args.files is not None:
        print(files_list)
        files_list = files_list.split()
        for file in files_list:
            file_destination = bucket_path + "/" + file
            copyfile(file, file_destination)

if args.torservice is not None:
    config_location = "/var/lib/tor/hidden_services/" + tor_service_name + "/hostname"
    collect_tor_name_string = Popen(["docker", "exec", tor_proxy_name, "cat", config_location], stdout=PIPE)
    tor_onion_address = collect_tor_name_string.stdout.read()
    tor_onion_address = tor_onion_address.decode("utf-8")
    output_string = "Your Tor Address is -- " + tor_onion_address
    print(output_string)