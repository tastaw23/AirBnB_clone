#!/usr/bin/env bash
# This script sets up the web servers for deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a fake HTML file for testing
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link and update ownership
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_file="/etc/nginx/sites-available/default"
if grep -q "hbnb_static" "$config_file"; then
    sed -i '/hbnb_static/ s|$|/|' "$config_file"
else
    sed -i '/server_name _;/a\\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' "$config_file"
fi

# Restart Nginx
sudo service nginx restart
