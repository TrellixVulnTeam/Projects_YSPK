#!/bin/bash

function test()
{
	libs=(requests sys os beautifulsoup4 numpy sklearn2 scikit-learn scipy nltk)
	sudo apt-get install python3-pip 
	for lib in ${libs[@]}
	do
		python3 -m pip install $lib
		echo "Installing Python Library $lib"
	done
}

test