#!/usr/bin/python3
""" Fabric Script to Update Version on webserver """

from fabric import Connection, task, env
import os
from sys import argv

archive_path = argv[1]
env.host = ['54.160.101.222', '100.25.205.48']
env.user = argv[4]
env.key_filename = argv[2]


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
                    with Connection(
                            host=host,
                            user=env.user,
                            connect_kwargs={"key_filename": env.key_filename}) as c:

                        print(f"Uploading {archive_path} to {host}...")
                        c.put(archive_name, '/tmp/')

                        print(f"Extracting {archive_name} on {host}...")
                        # c.run(f'tar -xzf /tmp/{archive_path} -C /data/web_static/releases/')
                        c.run(f'tar -xzf /tmp/{archive_name} -C {release_dir}')

                        print(f"Removing {archive_name} from {host}...")
                        c.run(f'rm -rf /tmp/{archive_name}')

                        print(f"Deleting current symlink on {host}...")
                        c.run(f'rm -fs /data/web_static/current')

                        print(f"Creating new symlink on {host}...")
                        c.run(f'ln -s {release_dir} /data/web_static/current')
                print("New Version deployed")
                return True

            except Exception as e:
                print(f"Deployment failed: {e}")
                return False
