#!/usr/bin/env bash

sudo systemctl daemon-reload  # Reload the systemd manager configuration

# Start the service
sudo systemctl start sanic.service

sudo systemctl enable sanic.service  # Enable the service to start on boot