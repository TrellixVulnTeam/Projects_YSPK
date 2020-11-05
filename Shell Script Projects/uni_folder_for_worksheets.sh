#!/bin/bash

path_general=/home/philipp/Dokumente

cd $path_general

echo "Uni Folder For Worksheets Creator"
echo "-------------------------------------"
echo ""
echo "You are in the general Folder: " $path_general
echo ""

if [ ! -d "$path_general/$1" ]
then
	mkdir "$1"
else
	echo "Directory" "$1" "already exists"
fi

cd "$1"

if [ ! -d "$path_general/$1/$2" ]
then
	mkdir "$2"
	cd "$2"
	
	for((i=1;i<=15;i++))
	do
		mkdir blatt$i
	done
	
	ls
else
	echo "Directory" "$2" "already exists"
fi