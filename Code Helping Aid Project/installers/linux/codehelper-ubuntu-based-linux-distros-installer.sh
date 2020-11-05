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
	libs=(requests sys os beautifulsoup4 numpy sklearn2 scikit-learn scipy)
	sudo apt-get install python3-pip 
	for lib in ${libs[@]}
	do
		python3 -m pip install $lib
		echo "Installing Python Library $lib"
	done
	echo "Installing Python Library nltk"
	sudo apt install python3-nltk
}

function installNeededNltkData()
{
	data=(stopwords averaged_perceptron_tagger)
	for package in ${data[@]}
	do
		echo "Installing $package Data"
		python3 -m nltk.downloader $package
	done
}

function installVsCode()
{
	cd vscode
	sudo dpkg -i "code_1.42.0-1580986622_amd64.deb"
	cd ..
}

function installNodeJs()
{
	sudo apt-get install curl
	curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -
	sudo apt-get install nodejs
}

function installVsCodeExtenstion()
{
	code --install-extension codehelper/codehelper-0.0.1.vsix
	code
}

function movingFilesFromInstallDirToLocalExtenstionDir()
{
	cp "" "$HOME/.vscode/codehelper"
}

echo "Bot Docs B 'CodeHelper' Installer Ubuntu-based Linux"
echo

sudo apt-get update

echo "Installing Python3..."
installPython3
echo

echo "Installing Python3 Libraries..."
installPythonLibraries
echo "Installed all Python3 Libraries"
echo

echo "Installing needed Nltk Data"
installNeededNltkData
echo "Installed all needed Nltk Data"
echo

echo "Installing VS Code..."
installVsCode
echo "Installed VS code"
echo

echo "Installing Node JS..."
installNodeJs
echo "Installed Node JS"

echo "Installing VS Code Extenstion 'CodeHelper'..."
installVsCodeExtenstion
echo "Installed VS Code Extenstion 'CodeHelper'"
echo

pause 'Press [Enter] key to exit...'
