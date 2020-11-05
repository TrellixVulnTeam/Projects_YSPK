#!/bin/bash

function mp3ToWav()
{
	local file="$1"
	local outputDir="$2"
	local outputFile="$outputDir/$(basename "$file" .mp3).wav"
	echo "Converting $file to $outputFile"
	sox "$file" "$outputFile"
}

function folderToWaves()
{
	local folder="$1"
	local outputDir="$2"
	local files=("$folder"/*)
	
	for file in "${files[@]}"
	do
		mp3ToWav "$file" "$outputDir"
	done
}

echo "-----------------------"
echo "|MP3 to Wave Converter|"
echo "-----------------------"
echo

if [ ! -d "output" ]
then
	mkdir output
	echo "Created output Directory"
	echo
fi

if [ -d "$1" ]
then
	folderToWaves "$1" "output"
else
	mp3ToWav "$1" "output"
fi

echo
read -p "Open output Directory? yes|no: " choice
if [ "$choice" = "yes" ]
then
	xdg-open "output"
fi