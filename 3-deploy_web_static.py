#!/usr/bin/python3
""" Fabric Script to Update Version on webserver """

import os
from fabric.api import env

do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy

# env.hosts = ['54.160.101.222', '100.25.205.48']
# env.user = 'ubuntu'
# env.key_filename = '/etc/ssh/ssh_config'


def deploy():
    """
    A script that deploys to both webservers
    calls the do_pack function to compress to tgz (moved outside the loop)
    calls the do_deploy function to send to the webserver
    and uncompress files
    """

    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)


if __name__ == '__main__':
    deploy()
