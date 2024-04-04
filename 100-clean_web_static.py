#!/usr/bin/python3
"""Fabric script that deletes out-of-date archives using function do_clean"""

from fabric.api import *
from os import listdir
from os.path import isfile, join
from datetime import datetime


env.hosts = ['35.237.166.125', '54.167.61.201']  # <IP web-01>, <IP web-02>


def do_clean(number=0):
    """Deletes out-of-date archives"""

    number = int(number)
    if number < 1:
        number = 1
    number += 1

    # Delete unnecessary archives in versions folder
    with lcd('versions'):
        local("ls -t | tail -n +{} | xargs -I {{}} rm -- {{}}".format(number))

    # Delete unnecessary archives in /data/web_static/releases folder
    with cd('/data/web_static/releases'):
        releases = run("ls -t").split()
        to_delete = releases[number:]
        if len(to_delete) > 0:
            run("rm -rf {}".format(" ".join(to_delete)))
