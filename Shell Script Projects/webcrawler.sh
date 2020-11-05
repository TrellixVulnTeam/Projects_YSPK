#!/bin/bash

function getFiles()
{
	local saveFolder="$1"
	local website=$2
	local formats=jpg,jpeg,png,gif,bmp,webp,mp4,avi,mpeg,webm,flv,mkv,vob,mov,wmv
	wget -q -nd -H -p -r -l 2 -P "$saveFolder" -A $formats -e robots=off $website
}

function getFilesWithCurl()
{
	local saveFolder="$1"
	local website=$2
	local formats="jpg|png|gif|jpeg,bmp|webp|mp4|avi|mpeg|webm|flv|mkv|vob|mov|wmv"
	curl --silent $website | grep -E "(http?:)?//[^/\s]+/\S+\.($formats)" -o | sed "s/^(http?)?\/\//http\:\/\//g" -r > urls.txt
	wget -q -P "$saveFolder" -i urls.txt
	rm -r urls.txt
}

function checkIfDirExistIfNotMkdir()
{
	local dir="$1"
	if [ ! -d "$dir" ]
	then
		mkdir "$dir"
	fi
}

function checkIfDirIsNotEmptyIfNotDelete()
{
	local dir="$1"
	if [ ! "$(ls -A $dir)" ]
	then 
		rm -R "$dir"
	fi
}

function cleanEmptyDirsInRootFolder()
{
	local rootFolder="$1"
	local files=("$rootFolder"/*)
	
	for file in "${files[@]}"
	do
		if [ -d "$file" ]
		then
			checkIfDirIsNotEmptyIfNotDelete "$file"
		fi
	done
}

function countFiles()
{
	local saveFolder="$1"
	local images=0 videos=0 other=0 documents=0 archives=0
	local files=("$saveFolder"/*)
	
	for file in "${files[@]}"
	do
		case $(checkFileExtensionForSorting "$file") in
		"image")
			((images++));;
		"video")
			((videos++));;
		"document")
			((documents++));;
		"archive")
			((archives++));;
		"other")
			((other++));;
		*)
			echo "error";;
		esac
	done
	
	echo "Images: $images"
	echo "Videos: $videos"
	echo "Documents: $documents"
	echo "Archives: $archives"
	echo "Other: $other"
	echo "----------------------------------------------"
	echo "Total: $(($images+$videos+$other+$documents+$archives))"
}

function checkFileExtensionForSorting()
{
	local file="$1"
	case "$file" in
	*.jpg | *.jpeg | *.png | *.gif | *.bmp | *.webp )
        echo "image";;
	*.mp4 | *.avi | *.mpeg | *.webm | *.flv | *.mkv | *.vob | *.mov | *.wmv )
		echo "video";;
	*.txt | *.pdf | *.docx | *.xlsx )
		echo "document";;
	*.zip | *.rar | *7z | *tar | *.dep | *.rpm )
		echo "archive";;
	*)
        echo "other";;
	esac	
}

function sortFilesPerType()
{
	local saveFolder="$1"
	local imageFolder="$saveFolder/Images" videoFolder="$saveFolder/Videos" otherFolder="$saveFolder/Other" documentFolder="$saveFolder/Documents" archiveFolder="$saveFolder/Archives"
	local files=("$saveFolder"/*)
	
	mkdir "$imageFolder"
	mkdir "$videoFolder"
	mkdir "$otherFolder"
	mkdir "$documentFolder"
	mkdir "$archiveFolder"
	
	for file in "${files[@]}"
	do
		case $(checkFileExtensionForSorting "$file") in
		"image")
			mv "$file" "$imageFolder";;
		"video")
			mv "$file" "$videoFolder";;
		"documents")
			mv "$file" "$documentFolder";;
		"archive")
			mv "$file" "$archiveFolder";;
		"other")
			mv "$file" "$otherFolder";;
		*)
			echo "error";;
		esac
	done
}
	

echo "------------------"
echo "|Bash Web Crawler|"
echo "------------------"
echo

echo "URL = $2 "
echo "Save Folder = $1"
echo

checkIfDirExistIfNotMkdir "$1"
getFilesWithCurl "$1" $2

echo "Files Dowloaded from $2"
echo "----------------------------------------------"
countFiles "$1"

echo
read -p "Sort Files per Filetype? yes|no: " choiceSort
if [ "$choiceSort" = "yes" ]
then
	sortFilesPerType "$1"
	cleanEmptyDirsInRootFolder "$1"
fi

echo
read -p "Open output Directory? yes|no: " choiceOpen
if [ "$choiceOpen" = "yes" ]
then
	xdg-open "$1"
fi
echo