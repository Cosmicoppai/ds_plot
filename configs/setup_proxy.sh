#!/usr/bin/env bash

# move the sanic.conf file to /etc/nginx/sites-available
sudo cp /home/sanic-www/log-helper/configs/sanic.conf /etc/nginx/sites-available

# create a symbolic link to /etc/nginx/sites-enabled
sudo ln -s /etc/nginx/sites-available/sanic.conf /etc/nginx/sites-enabled

sudo rm /etc/nginx/sites-enabled/default

sudo systemctl restart nginx