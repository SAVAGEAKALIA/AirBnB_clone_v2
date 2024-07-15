#!/usr/bin/env bash
# A script to create the directory and sub folders
sudo apt-get -y update
sudo apt-get -y install nginx

# create dir /data/ if it does not exist
if [ ! -d "/data/" ]; then
  mkdir -p /data/
fi

if [ $? -ne 0 ]; then
  echo "/data/ failed"
  exit 1
fi

# create directory /data/web_static/ if it does not exist
if [ ! -d "/data/web_static/" ]; then
  mkdir -p /data/web_static/
fi

if [ $? -ne 0 ]; then
  echo "/data/web_static/ failed to create"
  exit 1
fi


# create directory /data/web_static/releases/ if it does not exist
if [ ! -d "/data/web_static/releases/" ]; then
  mkdir -p /data/web_static/releases/
fi
if [ $? -ne 0 ]; then
  echo "/data/web_static/releases failed to create"
  exit 1
fi

# create directory /data/web_static/shared/ if it does not exist
if [ ! -d "/data/web_static/shared/" ]; then
  mkdir -p /data/web_static/shared/
fi

if [ $? -ne 0 ]; then
  echo "/data/web_static/shared/ failed to create"
  exit 1
fi

# create directory /data/web_static/releases/test/ if it doesn't exist
if [ ! -d "/data/web_static/releases/test/" ]; then
  mkdir -p /data/web_static/releases/test/
fi
if [ $? -ne 0 ]; then
  echo "/data/web_static/releases/test failed to create"
  exit 1
fi
# Create a fake HTML file /data/web_static/releases/test/index.html (with simple content, to test your Nginx configuration)
echo "HELLO SAVIOUR" >  /data/web_static/releases/test/index.html

# Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder.
# If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
if [ ! -f "/etc/nginx/sites-available/default.backup" ]; then
  sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup
fi

if ! grep -q "hbnb_static" /etc/nginx/sites-available/default; then
  sudo sed -i '/server_name _;/a \\t\t location \/hbnb_static {\n\t\t\talias \/data\/web_static\/current\/;\n\t\t}' /etc/nginx/sites-available/default
fi

if [ $? -ne 0 ]; then
  echo "grep command failed"
  exit 1
fi

# Restart Nginx to apply changes
nginx -s reload
service nginx start
service nginx status
echo "Deployment completed successfully."