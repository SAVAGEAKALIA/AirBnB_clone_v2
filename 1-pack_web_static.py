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
        result = local(f'tar -czf {output_path} web_static')

    if result:
        return result
    else:
        return None
