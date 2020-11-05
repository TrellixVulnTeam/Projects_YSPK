#!/bin/bash

function jmp
{
	label=$1
	cmd=$(sed -n "/^:[[:blank:]][[:blank:]]*${label}/{:a;n;p;ba};" $0 | grep -v ':$')
    eval "$cmd"
    exit
}

function get_process_id()
{
	local name=$1
	ps ax | awk '! /awk/ && /file_explorer_jukebox/ { print $1 }'
}

function wait_process()
{
	while ps -p $1 > /dev/null
	do
		sleep 1
	done
}

function getGenreOfSong()
{
	local song="$1"
	genre=$(soxi $song | grep Genre= | sed -e 's/^Genre=*//')
	
	if [ "$genre" = "" ]
	then 
		echo "Unknown"
	else
		echo $genre
	fi
}

function play_music()
{
	local song="$1"
	
	if [ -x "$(command -v vlc)" ]
	then
		echo "Playing:" "$song"
		echo
		soxi -a "$song"
		echo "Duration: " $(soxi -d "$song")
		cvlc  --play-and-exit --quiet "$song" 2>/dev/null #cvlc --play-and-exit --start-time $start --stop-time $stop $file 2>/dev/null (2>/dev/null unterdrücken von vlc version beim start)
	else
		mkdir -p waves
		#sox "$file" "$(basename "$file" .mp3).wav"
		#aplay -D front test.wav
		#cat test.wav | /dev/pcsp
		#paplay -p $file #oder pacat
	fi
}

function play_folder()
{
	local folder=$1
	songs=("$folder"/*)
	
	echo
	echo "List of songs in $folder"
	echo "------------------------"
	
	for song_name in "${songs[@]}"
	do
		echo $song_name
	done
	
	echo "------------------------"
	echo
	
	for song in "${songs[@]}"
	do
		play_music "$folder/$song"	
	done
	
	jmp begin
}

function shuffle_songs()
{
	local folder=$1
	local playthroughs=$2
	songs=("$folder"/*)
	
	echo
	echo "List of songs in $folder"
	echo "------------------------"
	
	for song_name in "${songs[@]}"
	do
		echo $song_name
	done
	
	echo "------------------------"
	echo
	
	for (( i=0; i<$playthroughs; i++))
	do
		index=$((RANDOM % ${#songs[*]}))
		play_music ${songs[$index]}
	done
	
	jmp begin
}

function PlayListMenu()
{
: playListMenu # jump marker for the Playlist menu
	clear
	echo "JukeBox 1.0 Playlist Menu"
	echo
	
	echo "1: Play existing Playlist"
	echo "2: Create new Playlist"
	echo "3: Edit existing Playlist"
	echo "4: Return to Jukebox Main Menu"
	echo
	
	read choice
	
	case $choice in
		1) getAndPlayPlayList;;
		2) createPlayList;;
		3) editPlayList;;
		4) jmp begin;;
		*) jmp playListMenu;;
	esac
}

function getAndPlayPlayList()
{
	local playLists=("data/PlayLists"/*)
	
	for playList_name in "${playLists[@]}"
	do
		echo $playList_name
	done
	
	read chosenPlayList
	playPlayList $chosenPlayList
	
	jmp playListMenu
}

function playPlayList()
{
	local playList="$1"
	local songs=$(cat playList | tr "\n" " ")
	
	for song_name in "${songs[@]}"
	do
		echo $song_name
	done
	
	echo "------------------------"
	echo
	
	for song in "${songs[@]}"
	do
		play_music "$song"	
	done
}

function createPlayList()
{
	echo "Create new Playlist"
	echo
	
	read playListName
	playListName=$playListName".txt"
	touch "data/PlayLists/"$playListName
	
	echo "Created Playlist $playListName"
	echo
	
	read -p "Add a song to the Playlist [y]es|[n]o: " userContinue
	
	while [ "$userContinue" != "n" ] 
	do
		read -p "Song: " songFilePath
		echo "$songFilePath" >> "data/PlayLists/"$playListName
		read -p "Add a song to the Playlist [y]es|[n]o: " userContinue
	done
	
	jmp playListMenu
}

function editPlayList()
{
	local playLists=("data/PlayLists"/*)

	echo "Edit existing Playlist"
	echo
	
	for playList_name in "${playLists[@]}"
	do
		echo $playList_name
	done
	
	read chosenPlayList
	read -p "Add a song to the Playlist [y]es|[n]o: " userContinue
	
	while [ "$userContinue" != "n" ] 
	do
		
		read -p "Song: " songFilePath
		echo "$songFilePath" >> "data/PlayLists/"$chosenPlayList
		read -p "Add a song to the Playlist [y]es|[n]o: " userContinue
	done
	
	jmp playListMenu
}


pipe=./data/temp/com_pipe.txt
mkdir -p "data/PlayLists"

: begin #jump marker for start
clear
echo "Juke Box 1.0"
echo

if [ "$1" = "begin" ] || [ -z "$1" ]
then
	echo "1: Play Song"
	echo "2: Play Folder of Songs"
	echo "3: Play Folder of Songs (Shuffle)"
	echo "4: Playlist Menu"
	echo "5: Exit Program"
	echo

	read choice

	case $choice in
		1)	x-terminal-emulator -e "./data/resources/file_explorer_jukebox.sh"
			id=$(ps ax | awk '! /awk/ && /file_explorer_jukebox/ { print $1 }')
			wait_process $id
			song=$(cat $pipe)
			rm -R $pipe
			play_music $song
			jmp begin ;;
		2)	x-terminal-emulator -e "./data/resources/folder_explorer_jukebox.sh"
			id=$(ps ax | awk '! /awk/ && /folder_explorer_jukebox/ { print $1 }')
			wait_process $id
			folder=$(cat $pipe)
			rm -R $pipe
			play_folder $folder ;;
		3)	x-terminal-emulator -e "./data/resources/folder_explorer_jukebox.sh"
			id=$(ps ax | awk '! /awk/ && /folder_explorer_jukebox/ { print $1 }')
			wait_process $id
			folder=$(cat $pipe)
			rm -R $pipe
			shuffle_songs $folder 5;;
		4) PlayListMenu;;
		5)	exit ;;
		*)	echo "Error" ;;
	esac
else
	play_music "$1"
fi