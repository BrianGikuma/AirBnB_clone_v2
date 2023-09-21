#!/usr/bin/python3
"""Script generates a .tgz archive from the contents of web_static folder"""

import os
from os import path
from fabric.api import local
from datetime import datetime


def do_pack():
    """packs contents of web_static folder"""
    if not path.exists('versions'):
        local('mkdir versions')

    archive_path = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime('%Y%m%d%H%M%S'))
    src_path = 'web_static'
    print('Packing web_static to {}'.format(archive_path))
    result = local('tar -cvzf {} {}'.format(archive_path, src_path))

    if result.succeeded:
        print('{} packed: {} -> {}Bytes'.format(
            src_path, archive_path, os.stat(archive_path).st_size))
        return archive_path

    return None
