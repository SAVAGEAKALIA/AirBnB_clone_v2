#!/usr/bin/python3
""" Fabric Script to Deploy and Update Version on Web Server """

from fabric.api import env, run, put
import os
from sys import argv

# Set Fabric environment variables from command line arguments
env.key_filename = argv[5]
env.user = argv[7]
env.hosts = ['54.160.101.222', '100.25.205.48']


def do_deploy(archive_path):
    """ Function to Deploy and update a newer version of website release"""
    # Check if the archive file exists
    if not os.path.exists(archive_path):
        print(f"Archive file {archive_path} does not exist.")
        return False

    try:
        """ try exception handling to catch errors"""
        archive_name = os.path.basename(archive_path)
        # Construct the release directory path
        release_dir = \
            f"/data/web_static/releases/{archive_name.replace('.tgz', '')}"

        # Iterate over each host defined in Fabric's env.hosts
        for host in env.hosts:
            # Upload the archive to /tmp/ directory on the web server
            print(f"Uploading {archive_path} to {host}...")
            put(archive_path, '/tmp/')

            # Create the release directory
            print(f"Creating directory {release_dir} on {host}...")
            run(f'rm -rf /data/web_static/releases/*')
            run(f'mkdir -p {release_dir}')

            # Extract the archive contents to the release directory
            print(f"Extracting {archive_name} on {host}...")
            run(f'tar -xzf /tmp/{archive_name} -C {release_dir}')

            # Remove the archive from /tmp/ directory on the web server
            print(f"Removing {archive_name} from {host}...")
            run(f'rm -rf /tmp/{archive_name}')

            # Move the contents of the web_static directory to release_dir
            print(f"Move {release_dir}/web_static* to {release_dir}...")
            run(f'mv {release_dir}/web_static/* {release_dir}')

            # Remove the old web_static directory from release_dir
            print(f"Deleting {release_dir}/web_static*...")
            run(f'rm -rf {release_dir}/web_static')

            # Remove the old release directory from the server
            print(f"Deleting current symlink on {host}...")
            run(f'rm -rf /data/web_static/current')

            # Create a new symlink to the new release directory on the server
            print(f"Creating new symlink on {host}...")
            run(f'ln -s {release_dir} /data/web_static/current')

            print("New Version deployed successfully.")
            return True

    except Exception as e:
        # Handle any exceptions that occur during deployment
        print(f"Deployment failed: {e}")
        return False
