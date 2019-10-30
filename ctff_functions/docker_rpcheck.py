import docker
import ctff_functions


def ctff_rp_check(client):
    client = ctff_functions.create_client()
    nginx_rp_check = 0
    nginx_rp_letsencrypt_check = 0
    container_list = client.containers.list(all)
    for container in container_list:
        if "nginx-proxy" in container.name:
            if "jwilder/nginx-proxy" in container.image:
                if "ctff-deployed" in container.exec_run("env"):
                    nginx_rp_check = 1
        if "nginx-proxy-letsencrypt" in container.name:
            if "jrcs/letsencrypt-nginx-proxy-companion" in container.image:
                if "ctff-deployed" in container.exec_run("env"):
                    nginx_rp_letsencrypt_check = 1
    if nginx_rp_check == 1 and nginx_rp_letsencrypt_check == 1:
        ctff_rp_deployed = 1
    else:
        ctff_rp_deployed = 0
    return ctff_rp_deployed
