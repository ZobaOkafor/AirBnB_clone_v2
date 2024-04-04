#!/usr/bin/env bash
# This script sets up web servers for deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Create necessary folders if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Set ownership
sudo chown -R ubuntu:ubuntu /data/
sudo chgrp -R ubuntu:ubuntu /data/

# Update Nginx configuration
config_block="
server {
    listen 80;
    listen [::]:80;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
    }
}
"

sudo sed -i "/server {/a $config_block" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0
