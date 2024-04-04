#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers,
using the function do_deploy.
"""

from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['54.152.235.22', '35.175.64.89']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa.pub'


def do_deploy(archive_path):
    """
    Function that distributes an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Extract file name and directory name from archive_path
        filename = archive_path.split('/')[-1]
        directory_name = filename.split('.')[0]

        # Remote paths
        remote_tmp_path = "/tmp/"
        remote_release_path = (
                "/data/web_static/releases/{}/".format(directory_name))

        # Upload the archive to /tmp/ directory
        put(archive_path, remote_tmp_path)

        # Create necessary directories
        run("mkdir -p {}".format(remote_release_path))

        # Extract archive to /data/web_static/releases/
        run("tar -xzf {}{} -C {}"
            .format(remote_tmp_path, filename, remote_release_path))

        # Remove the uploaded archive from the web server
        run("rm {}{}".format(remote_tmp_path, filename))

        # Move contents of extracted folder to its parent folder
        run("mv {}web_static/* {}"
            .format(remote_release_path, remote_release_path))

        # Remove extracted folder
        run("rm -rf {}web_static".format(remote_release_path))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(remote_release_path))

        return True
    except Exception as e:
        print(e)
        return False
