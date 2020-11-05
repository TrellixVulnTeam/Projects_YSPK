#!/bin/bash

function nodeJs()
{
	sudo apt-get install curl
	curl -sL https://deb.nodesource.com/setup_13.x | sudo -E bash -
	sudo apt-get install nodejs
}

nodeJs