#!/bin/bash

function spaces_to_c_style()
{
	local string=$1
	echo ${string//" "/"\ "}
}

function c_style_to_spaces()
{
	local string=$1
	echo ${string//"\ "/" "}
}

files=(/home/philipp/Dokumente/"1. Semester"/*) 

#IFS=' ' read -r -a files <<< $(ls /home/philipp/Musik/test_folder/)

for file in "${files[@]}"
do
	echo "$file"
done

echo ${#files[@]}

string="/Home/test/gibber/2. Semester/"

OLD_IFS="$IFS"
IFS="/"
STR_ARRAY=( $string )
IFS="$OLD_IFS"

for s in "${STR_ARRAY[@]}"
do
	echo "$s"
done

echo ${STR_ARRAY[$(( ${#STR_ARRAY[@]} - 1 ))]}

read test

if [ $test = "exit" ]
then
	echo "passed"
else
	echo "wrong"
fi