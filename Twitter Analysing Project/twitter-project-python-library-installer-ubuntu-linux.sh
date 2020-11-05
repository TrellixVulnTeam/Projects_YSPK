#!/bin/bash

function pause()
{
   read -p "$*"
}

function installPython3()
{
	if [ -x "$(command -v python3)" ]
	then
		echo "python3 allready installed"
	else
		sudo apt-get install python3
	fi
}

function installPythonLibraries()
{
	libs=(json os requests calendar mysql-connector-python re datetime matplotlib csv requests_oauthlib selenium time webdriver_manager)
	sudo apt-get install python3-pip 
	for lib in ${libs[@]}
	do
		echo "Installing Python Library $lib"
		python3 -m pip install $lib
	done
	echo "Installing Python Library tkinter"
	sudo apt-get install python3-tk
}

echo "Twitter Project Python3 and Python Library Installer for Ubuntu-based Linux Systems"
echo

sudo apt-get update

echo "Installing Python3..."
installPython3
echo

echo "Installing Python3 Libraries..."
installPythonLibraries
echo "Installed all Python3 Libraries"
echo

pause 'Press [Enter] key to exit...'
