#!/usr/bin/python3
"""Script generates a .tgz archive from the contents of web_static folder"""

from os import path, stat
from fabric.api import local, run, put, env, cd
from datetime import datetime


server_1 = '18.206.192.187'
server_2 = '100.26.53.46'
env.hosts = [server_1, server_2]


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
            src_path, archive_path, stat(archive_path).st_size))
        return archive_path

    return None


def do_deploy(archive_path):
    """Deploys archive to web servers"""
    if not path.exists(archive_path):
        return False

    put(archive_path, '/tmp/')
    with cd('/data/web_static/releases/'):
        if run('mkdir -p {}'.format(
               archive_path.split('/')[1].split('.')[0])).failed:
            return False
        if run('tar -xzf /tmp/{} -C {}/'.format(
                archive_path.partition('/')[2],
                archive_path.split('/')[1].split('.')[0])).failed:
            return False
        if run('mv {}/web_static/* {}/'.format(
                archive_path.split('/')[1].split('.')[0],
                archive_path.split('/')[1].split('.')[0])).failed:
            return False
    if run('rm /tmp/{}'.format(archive_path.split('/')[1])).failed:
        return False
    if run('rm /data/web_static/current').failed:
        return False
    if run(
        'ln -sf /data/web_static/releases/{} /data/web_static/current'.format(
            archive_path.split('/')[1].split('.')[0])).failed:
        return False

    return True
