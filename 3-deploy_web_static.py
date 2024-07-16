#!/usr/bin/env python
"""
Fabric Script to Update Version on webserver by importing functions
Highlights the use of fabric in script automation
"""

from fabric.api import env
from fabric.context_managers import settings

do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy

env.hosts = ['54.160.101.222', '100.25.205.48']
# env.user = 'ubuntu'
# env.key_filename = '/etc/ssh/ssh_config'


def deploy():
    """
    This function automates the deployment of a web static archive to multiple hosts using Fabric.
    It first calls the `do_pack` function to create a .tgz archive of the web static files.
    If the archive creation is successful, it proceeds to deploy the archive to each host in the `env.hosts` list.
    For each host, it uses Fabric's `settings` context manager to execute the `do_deploy` function.
    The function returns `True` if all deployments are successful, and `False` otherwise.

    Parameters:
    None

    Returns:
    bool: True if all deployments are successful, False otherwise
    """
    archive_path = do_pack()
    if not archive_path:
        raise Exception("Packing failed")

    successful_deploy = True

    for host in env.hosts:
        print(f"Deploying to host: {host}")
        with settings(host_string=host):
            result = do_deploy(archive_path)
            if not result:
                print(f"Deployment failed for host: {host}")
                successful_deploy = False
            else:
                print(f"Deployment successful for host: {host}")

    return successful_deploy
