import docker

connect_url = "unix://var/run/docker.sock"


def create_client():
    client = docker.DockerClient(base_url=connect_url)
    return client
