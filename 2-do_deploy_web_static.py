#!/usr/bin/python3
""" Fabric Script to Update Version on webserver """

from fabric.api import env, run, put
import os
from sys import argv

if len(argv) < 4:
    print("Usage: ./deploy.py <archive_path> <key_filename> <user>")
    exit(1)

# archive_path = argv[1]
env.key_filename = argv[2]
env.user = argv[3]
env.hosts = ['54.160.101.222', '100.25.205.48']
print(argv[0], argv[1], argv[2], argv[3], argv[4], argv[5])


def do_deploy(archive_path):
    """
    Script to Deploy and update newer version to server
    """

    if not os.path.basename(archive_path):
        print(f"Archive file {archive_path} does not exist.")
        return False
    else:
        if not argv[1:]:
            print("archive_path:argv[0], ssh_path:argv[2], user:argv[4]")
        else:
            try:
                archive_name = os.path.basename(archive_path)
                release_dir = \
                    f"/data/web_static/releases/{archive_name.replace('.tgz', '')}"
                for host in env.host:
                    print(argv[4])
                    print(argv[2])

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
