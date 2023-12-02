#!/bin/bash

echo Welcome to the PyEdit installer! Please run as root
echo Installing Dependencies...
apt-get install python3 pip git
echo Done
echo Setting up file tree...
cd ~
mkdir .PyEdit
cd .PyEdit
echo Done
echo Downloading PyEdit...
git clone https://github.com/caarfken/PyEdit.git
echo Done
echo Installing PyEdit
cd PyEdit/PyEdit
echo alias pyedit "python3 ~/.PyEdit/PyEdit/main.py" >> .bashrc
pwd
mv PyEdit.desktop ~/.local/share/applications

