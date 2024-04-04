#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import *
from datetime import datetime
import os


env.hosts = ['<IP web-01>', '<IP web-02>']  # Update with your server IPs
env.user = 'ubuntu'  # Update with your username
env.key_filename = ['/path/to/your/ssh/key']  # Update with your SSH key path


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder

    Returns:
        str: The path to the archive if it was generated successfully, otherwise None
    """
    try:
        # Create the versions folder if it doesn't exist
        local("mkdir -p versions")

        # Generate the filename for the archive
        now = datetime.now()
        time_format = now.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(time_format)

        # Create the .tgz archive
        local("tar -cvzf {} web_static".format(archive_path))

        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers

    Args:
        archive_path (str): The path to the archive to be deployed

    Returns:
        bool: True if all operations have been done correctly, otherwise False
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Get the filename without extension
        filename = os.path.basename(archive_path)
        filename_no_ext = os.path.splitext(filename)[0]

        # Create the release directory
        run('mkdir -p /data/web_static/releases/{}'.format(filename_no_ext))

        # Uncompress the archive to the release directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(filename, filename_no_ext))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(filename))

        # Move contents of the release directory to proper location
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'
            .format(filename_no_ext, filename_no_ext))

        # Remove redundant directory
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(filename_no_ext))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(filename_no_ext))

        print("New version deployed!")
        return True
    except Exception as e:
        print(e)
        return False


def deploy():
    """
    Deploys the web_static content to the web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
