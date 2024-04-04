#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers,
using the function deploy.
"""

from fabric.api import env, run, put
from datetime import datetime
from os.path import exists

env.hosts = ['54.152.235.22', '35.175.64.89']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """
    Function to generate a tgz archive from the contents of the
    web_static folder
    """
    try:
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        archive_name = 'web_static_{}.tgz'.format(current_time)
        local('mkdir -p versions')
        local('tar -cvzf versions/{} web_static'.format(archive_name))
        return 'versions/{}'.format(archive_name)
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Function to distribute an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        filename = archive_path.split('/')[-1]
        directory_name = filename.split('.')[0]

        remote_tmp_path = "/tmp/"
        remote_release_path = "/data/web_static/releases/{}/"
        .format(directory_name)

        put(archive_path, remote_tmp_path)
        run("mkdir -p {}".format(remote_release_path))
        run("tar -xzf {}{} -C {}"
            .format(remote_tmp_path, filename, remote_release_path))
        run("rm {}{}".format(remote_tmp_path, filename))
        run("mv {}web_static/* {}"
            .format(remote_release_path, remote_release_path))
        run("rm -rf {}web_static".format(remote_release_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(remote_release_path))

        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """
    Function to create and distribute an archive to web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
