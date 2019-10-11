import argparse
from subprocess import call

parser = argparse.ArgumentParser()
parser.add_argument("-cn", "--container-name", dest="containername", help="Name of container to create")
parser.add_argument("-nn", "--net-name", dest="netname", help="Name of network to create")
args = parser.parse_args()

if args.containername is None:
    print("Please specify a name for the container with -cn")
    exit(1)
if args.netname is None:
    print("Please specify a name for the network to create with -nn")
    exit(1)

container_name = args.containername
net_name = args.netname

call(["docker", "run", "--name", container_name, "-d", "-p", "9001:9001", "-v", "/var/run/docker.sock:/tmp/docker.sock:ro", "jheretic/onionboat"])
call(["docker", "network", "create", "-o", "com.docker.network.bridge.enable_ip_masquerade=false", net_name])
call(["docker", "network", "connect", net_name, container_name])
