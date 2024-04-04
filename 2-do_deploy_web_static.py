#!/usr/bin/python3
""" Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy: """

from fabric.api import *
from datetime import datetime
from os.path import exists, basename, splitext


env.hosts = ['35.237.166.125', '54.167.61.201']  # <IP web-01>, <IP web-02>
# ^ All remote commands must be executed on your both web servers
# (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder
    """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(filename))
    if result.succeeded:
        return filename
    else:
        return None


def do_deploy(archive_path):
    """ distributes an archive to my web servers
    """
    if not exists(archive_path):
        return False  # Returns False if the file at archive_path doesn't exist
    
    filename = basename(archive_path)
    no_tgz = '/data/web_static/releases/' + splitext(filename)[0]
    tmp = "/tmp/" + filename

    try:
        put(archive_path, "/tmp/")
        run("mkdir -p {}/".format(no_tgz))
        run("tar -xzf {} -C {}/".format(tmp, no_tgz))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(no_tgz, no_tgz))
        run("rm -rf {}/web_static".format(no_tgz))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(no_tgz))
        return True
    except Exception as e:
        print("Exception:", e)
        return False


def deploy():
    """ creates and distributes an archive to your web servers
    """
    new_archive_path = do_pack()
    if not new_archive_path:
        return False
    result = do_deploy(new_archive_path)
    return result
