#!/bin/bash
# This runs on the production server: fetches new code,
# Installs needed packages, and restarts the server.

touch rebuild
echo "Rebuilding"

echo "Pulling code from master"
git fetch origin master
git reset --hard FETCH_HEAD

echo "Installing packages"
pip install -r requirements.txt

echo "Going to reboot the webserver"
pa_reload_webapp.py NiravGolyalla.pythonanywhere.com

touch reboot
echo "Finished rebuild."