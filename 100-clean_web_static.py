#!/usr/bin/env python
"""
Fabric Script to Clean up old Version on webserver
by importing functions
Highlights the use of fabric in script automation
"""

from fabric.api import local, run, env
import os

env.hosts = ['54.160.101.222', '100.25.205.48']


def do_clean(number=0):
    """
    Fabric script to clean up old version archives.

    Args:
        number (int): Number of recent versions to keep. Defaults to 0.
                    If 0 or 1, only keep the most recent version.
                    If 2, keep the two most recent versions, and so on.
    """
    version_dir = os.path.join('version', '')
    version_file = os.listdir(version_dir)
    file_date = []
    for file in version_file:
        file_path = os.path.join(version_dir, file)
        modification_data = os.path.getmtime(file_path)
        file_date[file] = modification_data

    file_date = file_date.sort(key=file_date.get)

    if number == 0 or number == 1:
        local(f'rm os.path.join("versions", {file_date[:-1]}')
        run(f'rm -rf/data/web_static/releases/{file_date[:-1]}')
    elif number == 2:
        local(f'rm os.path.join("versions" {file_date[:-2]}')
        run(f'rm -rf/data/web_static/releases/{file_date[:2]}')
    else:
        pass
