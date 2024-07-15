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
    # env.key_filename = argv[5]
    # env.user = argv[7]
    # env.hosts = ['54.160.101.222', '100.25.205.48']

    if not os.path.exists(archive_path):
        print(f"Archive file {archive_path} does not exist.")
        return False
    
    try:
        archive_name = os.path.basename(archive_path)
        # Construct the release directory path
        release_dir = \
            f"/data/web_static/releases/{archive_name.replace('.tgz', '')}"
            # print(release_dir)

        for host in env.hosts:
            # Upload the archive to /tmp/ directory on the web servers
            print(f"Uploading {archive_path} to {host}...")
            put(archive_path, '/tmp/')

            # Create the release directory
            print(f"Creating directory {release_dir} on {host}...")
            run(f'mkdir -p {release_dir}')

            # Extract the archive contents to the release directory
            print(f"Extracting {archive_name} on {host}...")
            run(f'tar -xzf /tmp/{archive_name} -C {release_dir}')

            # Remove the archive from /tmp/ directory on the web servers
            print(f"Removing {archive_name} from {host}...")
            run(f'rm -rf /tmp/{archive_name}')

            # Move the contents of the web_static directory to release_dir
            print(f"Move {release_dir}/web_static* to {release_dir}...")
            run(f'mv {release_dir}/web_static/* {release_dir}')

            # Remove the old web_static directory from release_dir
            print(f"delete {release_dir}/web_static*...")
            run(f'rm -rf {release_dir}/web_static')

            # Remove the old release directory from the server
            print(f"Deleting current symlink on {host}...")
            run(f'rm -rf /data/web_static/current')

            # Create a new symlink to the new release directory on the server
            print(f"Creating new symlink on {host}...")
            run(f'ln -s {release_dir} /data/web_static/current')
            print("New Version deployed")
            return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
