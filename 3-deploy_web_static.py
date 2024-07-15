#!/usr/bin/python
"""
Fabric Script to Update Version on webserver by importing functions
Highlights the use of fabric in script automation
"""

from fabric.api import env

do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy

env.hosts = ['54.160.101.222', '100.25.205.48']
# env.user = 'ubuntu'
# env.key_filename = '/etc/ssh/ssh_config'


def deploy():
    """ A script that deploys to both webservers calls the do_pack
    function to compress to tgz (moved outside the loop)
    calls the do_deploy function to send to the webserver
    and uncompress files
    """
    archive_path = do_pack()
    if not archive_path:
        raise Exception("Packing failed")

    successful_deploy = True

    for host in env.hosts:
        print(f"Deploying to host: {host}")
        env.host_string = host
        result = do_deploy(archive_path)
        if not result:
            print(f"Deployment failed for host: {host}")
            successful_deploy = False
        else:
            print(f"Deployment successful for host: {host}")

    return successful_deploy
