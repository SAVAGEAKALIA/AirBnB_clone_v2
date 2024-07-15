#!/usr/bin/python3
""" Fabric Script to generate an archive tgz file"""

from fabric.api import local
import os
from datetime import datetime


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

    if os.path.exists('versions'):
        print(f'web_static packed: '
              f'{output_path} -> {os.path.getsize(output_path)}Bytes')
        # print(f'{os.path.join("versions", output_file)}')
        return os.path.join('versions', output_file)
    else:
        return None
