#!/bin/bash

function print_array()
{
	local array=("$@")
	
	echo -n "| "
	
	for item in "${array[@]}"
	do
		echo -n "$item" "| "
	done
}

function create_random_array()
{
	local range=$1
	local random_range=$2
	declare -a array
	
	for (( i=0; i < $range; i++))
	do
		array[i]=$(( RANDOM % $random_range ))
	done
	
	echo "${array[@]}"
}

function bubblesort
{	
	local arr=("$@")
	
	for (( i=0; i < ${#arr[@]}; i++))
	do
		for (( j=0; j < $(( ${#arr[@]} - $i - 1 )); j++ )) 
		do
			if [ ${arr[j]} -gt ${arr[$(( j + 1 ))]} ]
			then
				temp=${arr[j]}
				((arr[j]= ${arr[$(( $j + 1 ))]}))
				((arr[$(( $j + 1 ))]=$temp))
			fi
		done
	done
	
	echo "${arr[@]}"
}

function selectionsort()
{
	local arr=("$@")
	
	for (( i=0; i < $(( ${#arr[@]} - 1 )); i++ ))
	do
		min_idx=$i
		for (( j=$(( $i + 1)); j < ${#arr[@]}; j++))
		do
			if [ ${arr[j]} -lt ${arr[min_idx]} ]
			then
				min_idx=$j
			fi
			
			temp=${arr[min_idx]}
			((arr[min_idx]= ${arr[i]}))
			((arr[i]=$temp))
		done
	done
	
	echo "${arr[@]}"
}

function insertionsort()
{
	local arr=("$@")
	
	for (( i=0; i < ${#arr[@]}; i++ ))
	do
		key=${arr[i]}
		j=$(( $i - 1 ))
		
		while [ $j -ge 0 ] && [ ${arr[j]} -gt $key ]
		do
			((arr[$(( $j + 1 ))] = ${arr[j]}))
			j=$(( $j - 1))
		done
		
		((arr[$(( $j + 1 ))] = $key))
	done
	
	echo "${arr[@]}"		
}

function mergesort()
{
	local arr=("$@")
}
	
test_array=$(create_random_array 10 11)

echo "Bubblesort"
echo "----------"
echo
print_array $test_array
bubble_sorted=$(bubblesort $test_array)
echo
print_array $bubble_sorted
echo
echo

echo "Selectionsort"
echo "-------------"
echo
print_array $test_array
sel_sorted=$(selectionsort $test_array)
echo
print_array $sel_sorted
echo
echo

echo "Insertionsort"
echo "-------------"
echo
print_array $test_array
ins_sorted=$(insertionsort $test_array)
echo
print_array $ins_sorted
echo
echo




	