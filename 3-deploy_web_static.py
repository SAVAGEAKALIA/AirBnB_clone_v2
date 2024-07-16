#!/usr/bin/python3
"""
Fabric Script to Update Version on webserver by importing functions
Highlights the use of fabric in script automation
"""

from fabric.api import env, run, put, local, execute
import os
from datetime import datetime

# do_pack = __import__('1-pack_web_static').do_pack
# do_deploy = __import__('2-do_deploy_web_static').do_deploy

# env.hosts = ['54.160.101.222', '100.25.205.48']
# env.user = 'ubuntu'
# env.key_filename = '/etc/ssh/ssh_config'

archive_path = None


def do_pack():
    """ Function to implement generation of tgz files"""
    current_time = datetime.now()
    output_file = \
        f"web_static_{current_time.strftime('%Y%m%d%H%M%S')}.tgz"
    if not os.path.exists('versions'):
        os.makedirs(os.path.join('versions', ''))
    output_path = os.path.join('versions', output_file)
    # print("Packing web_static to {}".format(output_path))
    local(f'tar -cvzf {output_path} web_static')

    print(f'web_static packed: '
          f'{output_path} -> {os.path.getsize(output_path)}Bytes')
    if os.path.exists(output_path):
        print(output_path)
        return output_path
    else:
        return None


def do_deploy(archive_path: str) -> bool:
    """
    Deploys a specified archive to remote hosts.

    This function automates the deployment process by
    uploading an archive file to multiple hosts,
    extracting it, and updating symbolic links on the servers.

    Parameters:
    - archive_path (str): Path to the archive file to deploy.
    The file must exist.

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
        # print(f'current {host}\n')
        # with settings(host_string=hosts):
        # Upload the archive to /tmp/ directory on the web server
        print(f"Uploading {archive_path} to {hosts}...")
        put(archive_path, '/tmp/')

        # Create the release directory
        print(f"Creating directory {release_dir} on {hosts}...")
        #run(f'rm -rf /data/web_static/releases/*')
        run(f'mkdir -p {release_dir}')

        # Extract the archive contents to the release directory
        print(f"Extracting {archive_name} on {hosts}...")
        run(f'tar -xzf /tmp/{archive_name} -C {release_dir}')

        # Remove the archive from /tmp/ directory on the web server
        print(f"Removing {archive_name} from {hosts}...")
        run(f'rm -rf /tmp/{archive_name}')

        # Move the contents of the web_static directory to release_dir
        print(f"Move {release_dir}/web_static* to {release_dir}...")
        run(f'mv {release_dir}/web_static/* {release_dir}')

        # Remove the old web_static directory from release_dir
        print(f"Deleting {release_dir}/web_static*...")
        run(f'rm -rf {release_dir}/web_static')

        # Remove the old release directory from the server
        print(f"Deleting current symlink on {hosts}...")
        run(f'rm -rf /data/web_static/current')

        # Create a new symlink to the new release directory on the server
        print(f"Creating new symlink on {hosts}...")
        run(f'ln -s {release_dir} /data/web_static/current')

        print("New Version deployed successfully.")
        print(f'{hosts}\n')
        return True

    except Exception as e:
        """ Handle any exceptions that occur during deployment """
        print(f"Deployment failed: {e}")
        return False


def deploy():
    """
    This function automates the deployment of a web
    static archive to multiple hosts using Fabric.
    It first calls the `do_pack` function to create
    .tgz archive of the web static files.
    If the archive creation is successful, it proceeds to
    deploy the archive to each host in the `env.hosts` list.
    For each host, it uses Fabric's `settings` context
    manager to execute the `do_deploy` function.
    The function returns `True` if all deployments
    are successful, and `False` otherwise.

    Parameters:
    None

    Returns:
    bool: True if all deployments are successful, False otherwise
    """
    env.hosts = ['54.160.101.222', '100.25.205.48']
    global archive_path
    if archive_path is None:
        archive_path = do_pack()
        if not archive_path:
            raise Exception("Packing failed")

    return all(execute(do_deploy, archive_path))


if __name__ == "__main__":
    deploy()
