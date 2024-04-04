#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives using the function do_clean.
"""

from fabric.api import env, local, run
from os.path import exists

env.hosts = ['54.152.235.22', '35.175.64.89']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """
    Function to delete out-of-date archives
    """
    try:
        number = int(number)
        if number < 1:
            number = 1

        # Delete out-of-date archives in versions folder
        local("ls -1t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}"
              .format(number + 1))

        # Delete out-of-date archives in /data/web_static/releases folder
        run("ls -1t /data/web_static/releases | tail -n +{} | xargs -I {{}} "
            "rm -rf /data/web_static/releases/{{}}".format(number + 1))

    except Exception as e:
        print(e)
        return False
