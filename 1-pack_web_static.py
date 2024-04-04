#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """Creates a .tgz archive from the contents of the web_static folder."""
    try:
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        filename = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(filename))
        return filename
    except Exception:
        return None
