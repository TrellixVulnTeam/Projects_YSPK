#!/bin/bash

function crawlHtml()
{
	local url=$1
	local savePath=$2
	
	curl $url > $savePAth
}

