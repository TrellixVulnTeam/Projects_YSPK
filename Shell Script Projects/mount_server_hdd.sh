#!/bin/bash

ssid=$(iwgetid -r)

if [ $ssid == "BEWICO_HOME_2.4G" ]
then
	echo $ssid
	echo "Succes"
fi