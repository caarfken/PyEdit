#!/bin/bash

echo Welcome to the PyEdit installer! Please run as root
echo Installing Dependencies...
apt-get install python3 git
echo Done
echo Setting up file tree...
cd /home/$SUDO_USER
mkdir .PyEdit
cd .PyEdit
echo Done
echo Downloading PyEdit...
rm -rd PyEdit
git clone https://github.com/caarfken/PyEdit.git
echo Done
echo Installing PyEdit
cd PyEdit/PyEdit
echo alias pyedit=\"python3 /home/$SUDO_USER/.PyEdit/PyEdit/PyEdit/main.py\" >> /home/$SUDO_USER/.bashrc
pwd
mv PyEdit.desktop /home/$SUDO_USER/.local/share/applications

