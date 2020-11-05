#!/bin/bash

function getGenre()
{
	local song="$1"
	local genre=$(soxi drumsolomono.mp3 | grep Genre= | sed -e "s/^Genre=//")
	echo $genre
}

function makeGenreDir()
{
	local musicFolder="$1"
	local genreDir="genres"
	if [ ! -d "$genreDir" ]
	then
		mkdir "$genreDir"
	fi

function makeGenreFile()
{
	local genre=$1
	local folderPath="$2/genres"
	touch "$folderpath/$genre.txt"
}

function writeSongToGenreFile()
{
	local song="$1"
	local folderPath="$2"
	local genre=$3
	local genreFile="$folderpath/genres/$genre.txt"
	$song >> $genreFile
}

function getFolderDataAndSort()
{
	local folderPath="$1"
	local files=("$folderPath"/*)
	
	makeGenreDir "$folderPath"
	
	for file in "${files[@]}"
	do
		local genre=$(getGenre "$file")
		makeGenreFile $genre "$folderPath"
		writeSongToGenreFile "$file" "$folderPath" $genre
	done
}

getgetFolderDataAndSort "$1"