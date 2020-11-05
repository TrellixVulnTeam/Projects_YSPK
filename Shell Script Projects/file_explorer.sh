#!/bin/bash

function jmp
{
	label=$1
	cmd=$(sed -n "/^:[[:blank:]][[:blank:]]*${label}/{:a;n;p;ba};" $0 | grep -v ':$')
    eval "$cmd"
    exit
}

function file_properties()
{
	local file=$1
	
	echo "File Properties Viewer 1.0"
	echo 
	stat $file
	echo
	
	echo -n "Return? y or n: "
	read end
	
	if [ $end = "y" ] 
	then
		clear
		jmp main
	fi
}

function make_directory()
{
	local dir_name=$1
	mkdir $dir_name
	clear
	jmp main
}

function delete_file()
{
	local file_name=$1
	
	echo "Delete File Terminal"
	echo
	
	echo -n "Files can't be restored. Are you sure you want do delete $file_name? y or n: "
	read choice
	
	if [ $choice = "y" ]
	then
		rm -f -r $file_name
		clear
		jmp main
	else
		clear
		jmp main
	fi
}

function create_file()
{
	local file_name=$1
	: > $file_name
	jmp main
}
	
directory=$HOME


: main

files=("$directory"/*)

echo
echo "List of Files in $directory"
echo "------------------------"
	
for file in "${files[@]}"
do
	if [ -d "$file" ]
	then
		echo -e "\e[1m\e[34m${file/$directory"/"/""}"
	elif [ -x "$file" ]
	then
		echo -e "\e[1m\e[35m${file/$directory"/"/""}"
	else
		echo -e "\e[0m${file/$directory"/"/""}"
	fi
done
	
echo -e "\e[0m------------------------"
echo

echo ".. = Go one Directory back"
echo "P: filename = list properties of file"
echo "Del: filename = delete file"
echo "Mdir: foldername = create new folder"
echo "Mfile: filename = create empty file"
echo "exit = end Program"
echo

echo -n "Type Filename to choose File or Directoryname to go further: "
read filedir

if [ $filedir = ".." ]
then
	clear
	OLD_IFS="$IFS"
	IFS="/"
	substring=( $directory )
	IFS="$OLD_IFS"
	directory=${directory/"/"${substring[$(( ${#substring[@]} - 1 ))]}/""}
	jmp main
elif [ $filedir = "exit" ]
then
	exit
elif [[ $filedir == "P: "* ]]
then
	filedir=${filedir/"P: "/""}
	clear
	file_properties "$directory/$filedir"
elif [[ $filedir == "Del: "* ]]
then
	filedir=${filedir/"Del: "/""}
	clear
	delete_file "$directory/$filedir"
elif [[ $filedir == "Mdir: "* ]]
then
	filedir=${filedir/"Mdir: "/""}
	make_directory "$directory/$filedir"
elif [[ $filedir == "Mfile: "* ]]
then
	filedir=${filedir/"Mfile: "/""}
	clear
	create_file "$directory/$filedir"
elif [ -d "$directory/$filedir" ]
then
	directory=$directory/$filedir
	clear
	jmp main
elif [ -e "$directory/$filedir" ]
then
	echo "$directory/$filedir" #xdg-open
else
	echo "Error"
fi
