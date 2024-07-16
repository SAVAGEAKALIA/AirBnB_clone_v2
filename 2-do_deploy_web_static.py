#!/usr/bin/python3
"""
Fabric Script to Deploy and Update Version on Web Server. This script automates the deployment process by uploading
 a specified archive
to multiple hosts, extracting it, and updating symbolic links on the servers.
Usage:
    python3 do_deploy.py <archive_path> <key_filename> <username>
Arguments:
    archive_path (str): Path to the archive file to deploy.
    key_filename (str): Path to the SSH private key file for authentication.
    username (str): Username used to connect to the remote servers.
Environment variables:
    This script expects the Fabric environment variables 'env.hosts' to be set
    with a list of host IP addresses or hostnames.
Functions:
    - do_deploy(archive_path):
        Deploys the specified archive to remote hosts:
        - Uploads the archive.
        - Creates necessary directories.
        - Extracts the archive.
        - Moves files to the correct directory structure.
        - Updates symbolic links.
"""

from fabric.api import env, run, put
import os
from sys import argv
from fabric.context_managers import settings

# Set Fabric environment variables from command line arguments
if len(argv) > 3:
    env.key_filename = argv[5]
    env.user = argv[7]
    env.hosts = ['54.160.101.222', '100.25.205.48']


def do_deploy(archive_path: str) -> bool:
    """
    Deploys a specified archive to remote hosts.

    This function automates the deployment process by uploading an archive file to multiple hosts,
    extracting it, and updating symbolic links on the servers.

    Parameters:
    - archive_path (str): Path to the archive file to deploy. The file must exist.

    Returns:
    - bool: True if the deployment is successful, False otherwise.
    """
    # Check if the archive file exists
    if not os.path.isfile(archive_path):
        print(f"Archive file {archive_path} does not exist.")
        return False

    try:
        """ try and raise exception to catch any errors during Deployment"""
        archive_name = os.path.basename(archive_path)
        # Construct the release directory path
        release_dir = \
            f"/data/web_static/releases/{archive_name.replace('.tgz', '')}"

        # Iterate over each host defined in Fabric's env.hosts
        hosts = env.hosts
        print(hosts)
        # for host in hosts:
        print(f'current {host}\n')
        with settings(host_string=host):
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
            print(f'{host}\n')
        return True

    except Exception as e:
        """ Handle any exceptions that occur during deployment """
        print(f"Deployment failed: {e}")
        return False
