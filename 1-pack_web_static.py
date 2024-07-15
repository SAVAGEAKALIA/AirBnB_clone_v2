#!/usr/bin/python3
""" Fabric Script to generate an archive tgz file"""

from fabric.api import local
import os
from datetime import datetime


def do_pack():
    """ Function to implement generation of tgz files"""
    # c = Connection('localhost')
    current_time = datetime.now()
    output_file = f"web_static_{current_time.strftime('%Y%m%d%H%M%S')}.tgz"
    if not os.path.exists('version'):
        os.makedirs(os.path.join('version', ''))
        output_path = os.path.join('version', output_file)
        print("Packing web_static to {}".format(output_path))
        local(f'tar -czf {output_path} web_static', capture=False)

    if os.path.exists('version'):
        print("web_static packed: {} -> {}Bytes".format(output_path, os.path.getsize(output_path)))
        print(f'{os.path.join("version", output_file)}')
        return os.path.join('version', output_file)
    else:
        return None
