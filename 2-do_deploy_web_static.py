#!/usr/bin/python3
""" Fabric Script to Update Version on webserver """

from fabric.api import env, run, put
import os
from sys import argv

# archive_path = argv[1]
env.key_filename = argv[5]
env.user = argv[7]
env.hosts = ['54.160.101.222', '100.25.205.48']


def do_deploy(archive_path):
    """
    Script to Deploy and update newer version to server
    """
    if not os.path.basename(archive_path):
        print(f"Archive file {archive_path} does not exist.")
        return False
    else:
        try:
            archive_name = os.path.basename(archive_path)
            print(archive_name)
            release_dir = \
                f"/data/web_static/releases/{archive_name.replace('.tgz', '')}"
            print(release_dir)

            for host in env.host:
                print(f"Uploading {archive_path} to {host}...")
                put(archive_name, '/tmp/')

                print(f"Extracting {archive_name} on {host}...")
                run(f'tar -xzf /tmp/{archive_name} -C {release_dir}')

                print(f"Removing {archive_name} from {host}...")
                run(f'rm -rf /tmp/{archive_name}')

                print(f"Deleting current symlink on {host}...")
                run(f'rm -rf /data/web_static/current')

                print(f"Creating new symlink on {host}...")
                run(f'ln -s {release_dir} /data/web_static/current')
            print("New Version deployed")
            return True

        except Exception as e:
            print(f"Deployment failed: {e}")
            return False
