#!/bin/bash

mkfifo pipe

while :
do
	echo "test" > pipe
done