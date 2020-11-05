#!/bin/bash

function read_file_generic()
{
	while read line
	do
		echo $line
	done < $1
}

function read_mask_password()
{
	unset password
	charcount=0
	
	stty -echo
	
	while IFS= read -p "$prompt" -r -s -n 1 ch
	do
    	if [[ $ch == $'\0' ]]
		then
        	break
    	fi
		
    	if [[ $ch == $'\177' ]] 
		then
        	if [ $charcount -gt 0 ] 
			then
            	charcount=$((charcount-1))
            	prompt=$'\b \b'
            	password="${password%?}"
        	else
            	PROMPT=''
        	fi
    	else
        	charcount=$((charcount+1))
        	prompt='*'
        	password+="$ch"
    	fi
	done

	stty echo
	echo $password
}

function encrypt_password()
{
	local password=$1
	
	for (( i=0; i<${#password}; i++))
	do
		p=$(LC_CTYPE=C printf "%d" "'${password:$i:1}")
		constNum=$(LC_CTYPE=C printf "%d" "'?")
		p=$((p*constNum*100))
		echo $p
	done
}

file="/home/philipp/Schreibtisch/test.txt"

if [ -f $file ]
then
	rm $file
fi

for (( i=1; i<=3; i++ ))
do
	echo "test$i" >> $file 
done

read_file_generic $file 

echo
echo "QWERTZ" >> $file

read_file_generic $file

echo -n "Enter password : "
pass=$(read_mask_password)
echo
echo "password:" $pass >> $file
echo

read_file_generic $file

echo
encrypt_password $pass
