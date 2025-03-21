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
		sudo dnf install python3
	fi
}

function installPythonLibraries()
{
	libs=(requests sys os beautifulsoup4 numpy sklearn2 scikit-learn scipy nltk)
	sudo dnf install python3-pip
	for lib in ${libs[@]}
	do
		sudo python3 -m pip install $lib
		echo "Installing Python Library $lib"
	done
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
	sudo rpm -i "code-1.42.0-1580986751.el7.x86_64.rpm"
	cd ..
}

function installNodeJs()
{
	sudo dnf install curl
	curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -
	sudo dnf install nodejs

function installVsCodeExtenstion()
{
	cp -r "codehelper" "$HOME"
	cd "$HOME/codehelper"
	code .
}

echo "Bot Docs B 'CodeHelper' Installer Fedora-based Linux"
echo

sudo dnf update

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