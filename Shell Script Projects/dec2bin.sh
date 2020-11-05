#!/bin/bash

function convertIntvalToBase() 
{
   val=$1
   base=$2
   result=""
   while [ $val -ne 0 ] ; do
        result=$(( $val % $base ))$result 
        val=$(( $val / $base ))
   done
   echo -n $result
   echo
}

function convertIntegerToBinValue()
{
   val=$1
   result=""
   while [ $val -ne 0 ] ; do
        result=$(( $val % 2 ))$result 
        val=$(( $val / $base ))
   done
   echo -n $result
   echo
}

convertIntvalToBase $1 2
convertIntegerToBinValue $1
