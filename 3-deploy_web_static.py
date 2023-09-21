#!/usr/bin/python3
"""
    Script generates a tgz archive from the contents of web_static folder
    and deploys to my servers
"""
import datetime
from os import path, stat, scandir
from fabric.api import local, run, put, env, cd
from datetime import datetime as date_time

server_1 = '52.6.235.201'
server_2 = '54.83.130.114'
env.hosts = [server_1, server_2]


def do_pack():
    """
        Packs contents of web_static folder
        Returns:
            archive path or None if archive did not succeed
    """
    if not path.exists('versions'):
        local('mkdir versions')

    diff = datetime.timedelta(minutes=2)
    now = date_time.now()
    directory = scandir('versions')
    entries = list(directory)

    for entry in entries:
        time = date_time.strptime(entry.name[11:-4], '%Y%m%d%H%M%S')
        if now - time <= diff:
            archive_path = 'versions/{}'.format(entry.name)
            return archive_path
    archive_path = 'versions/web_static_{}.tgz'.format(
            now.strftime('%Y%m%d%H%M%S'))

    src_path = 'web_static'
    print('Packing web_static to {}'.format(archive_path))
    result = local('tar -cvzf {} {}'.format(archive_path, src_path))

    if result.succeeded:
        print('{} packed: {} -> {}Bytes'.format(
            src_path, archive_path, stat(archive_path).st_size))
        return archive_path
    return None


def do_deploy(archive_path):
    """
        Deploys the pre-packed archive to the web servers
        Arguments:
            archive_path: path to the archive to be deployed
        Returns:
            True if deployement succeed or False otherwise
    """
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
    print('New version deployed!')
    return True


def deploy():
    """
        Creates and distributes archive to my web servers
        Returns:
            True if deployement succeeds else False if otherwise
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    ret_val = do_deploy(archive_path)
    return ret_val
