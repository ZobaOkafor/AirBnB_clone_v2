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


def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory
        put(archive_path, "/tmp/")

        # Extract archive to /data/web_static/releases/
        filename = archive_path.split('/')[-1]
        foldername = "/data/web_static/releases/" + filename.split('.')[0]
        run("mkdir -p {}".format(foldername))
        run("tar -xzf /tmp/{} -C {}".format(filename, foldername))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Move contents of extracted folder to its parent folder
        run("mv {}/web_static/* {}".format(foldername, foldername))

        # Remove extracted folder
        run("rm -rf {}/web_static".format(foldername))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s {} /data/web_static/current".format(foldername))

        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False
