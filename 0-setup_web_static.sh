#!/usr/bin/env bash
# This script sets up web servers for deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    apt-get -y update
    apt-get -y install nginx
fi

# Create necessary folders if they don't exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# Set ownership
chown -R ubuntu:ubuntu /data/
chgrp -R ubuntu:ubuntu /data/

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
