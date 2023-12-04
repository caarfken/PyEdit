#!/bin/bash

echo Welcome to the PyEdit installer! Please run as root
echo Installing Dependencies...
apt-get install python3 git
echo Done
echo Downloading PyEdit...
rm -rd PyEdit
git clone https://github.com/caarfken/PyEdit.git
chmod go+rw PyEdit
echo Done
echo Installing PyEdit
cd PyEdit/PyEdit
ls | mv /usr/local/bin
echo Done



