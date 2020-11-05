#!/bin/bash

function genrateRandomCard()
{
	local -n cardsA=$1
	local -n cardCounterA=$2
	index=$(( RANDOM % ${#cardsA[*]} ))
	
	while [ ${cardCounterA[${cardsA[$index]}]} -eq 0 ]
	do
		index=$(( RANDOM % ${#cardsA[*]} ))
	done
	
	((cardCounterA[cardsA[index]]--))
	
	echo ${cardsA[$index]}
}

function calculateAssValue()
{
	local currentCardCount=$1
	if [ $(( $currentCardCount + 11 )) -gt 21 ]
	then
		echo 1
	else
		echo 11
	fi
}

function botcheckCardsLogic()
{
	local index=$1
	local -n cardsD=$2
	local -n cardsValueD=$3
	local simulatedCardValue=$4
	
	if [ ${cardsD[$index]} = "Ass" ]
	then
		simulatedCardValue=$(( simulatedCardValue + $(calculateAssValue $simulatedCardValue) ))
	else
		simulatedCardValue=$(( simulatedCardValue + ${cardsValueD[${cardsD[$index]}]} ))
	fi
	
	if [ $simulatedCardValue -gt 21 ]
	then
		echo 1
	else
		echo 0
	fi
}

function botTurn()
{
	local -n cardsB=$1
	local -n cardsValueB=$2
	local -n cardCounterB=$3
	local cardValue=0
	
	while [ $cardValue -lt 21 ]
	do
		randomIndex=$(genrateRandomCard cardsB cardCounterB)
		logicCheckerResult=$(botcheckCardsLogic $randomIndex cardsB cardsValueB $cardValue)
		if [ $logicCheckerResult -eq 1 ]
		then
			break
		fi
		
		if [ ${cardsB[$randomIndex]} = "Ass" ]
		then
			cardValue=$(( $cardValue + $(calculateAssValue $cardValue) ))
		else
			cardValue=$(( $cardValue + ${cardsValueB[${cardsB[$randomIndex]}]} ))
		fi
	done
	
	echo $cardValue
}

function playerTurn()
{
	local -n cardsC=$1
	local -n cardsValueC=$2
	local -n cardCounterC=$3
	local cardValue=0
	
	while [ $cardValue -lt 21 ]
	do
		randomIndex=$(genrateRandomCard cardsC cardCounterC)
		if [ ${cardsC[$randomIndex]} = "Ass" ]
		then
			cardValue=$(( $cardValue + $(calculateAssValue $cardValue) ))
		else
			cardValue=$(( $cardValue + ${cardsValueC[${cardsC[$randomIndex]}]} ))
		fi
		
		echo "your current Cardcount is: $cardValue"
		
		read -p "Stop? [y|n]: " choice
		if [ $choice = "y" ]
		then
			clear
			break
		fi
		clear
	done
	
	return $cardValue
}

function calculateWinner()
{
	local botCardValue=$1
	local playerCardValue=$2
	
	if [ $botCardValue -eq $playerCardValue ]
	then
		echo "it is a draw"
	elif [ $botCardValue -gt $playerCardValue ] && [ $botCardValue -lt 22 ] || [  $playerCardValue -gt 21 ]
	then
		echo "Winner Winner Chicken Dinner"
		echo "Bot is the winner"
	elif [ $playerCardValue -lt 22 ]
	then
		echo "Winner Winner Chicken Dinner"
		echo "Player is the winner"
	else
		echo "No one Wins"
	fi
}

while [ true ]
do
	declare -A cardValues=( ["2"]=2 ["3"]=3 ["4"]=4 ["5"]=5 ["6"]=6 ["7"]=7 ["8"]=8 ["9"]=9 ["10"]=10 ["Bube"]=10 ["Dame"]=10 ["Koenig"]=10 ["Ass"]="NOTSET" )
	declare -A cardCounter=( ["2"]=4 ["3"]=4 ["4"]=4 ["5"]=4 ["6"]=4 ["7"]=4 ["8"]=4 ["9"]=4 ["10"]=4 ["Bube"]=4 ["Dame"]=4 ["Koenig"]=4 ["Ass"]=4 )
	cards=( "${!cardValues[@]}" )
	botCardValue=$(botTurn cards cardValues cardCounter)
	playerTurn cards cardValues cardCounter
	playerCardValue=$?
	
	echo "Bot: $botCardValue"
	echo "Player: $playerCardValue"
	echo
	
	calculateWinner $botCardValue $playerCardValue
	read -p "Stop? [y|n]: " choice
	if [ $choice = "y" ]
	then
		break
	fi
	clear
done