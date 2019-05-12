#!/bin/bash
INPUT=amazon_data.csv
OLDIFS=$IFS
logfolder=$(date +%Y_%m_%d) 
mkdir $logfolder 
mv *.log $logfolder 
IFS=,
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read cat url prm pgnum
do
	echo "cat : $cat"
	echo "url : $url"
	echo "prm : $prm"
	echo "pgnum : $pgnum"
	nohup  scrapy crawl amazonitem -a category="$cat" -a url="$url" -a prm="$prm" -a pgnum="$pgnum" -s LOG_FILE=${cat}_amz.log &
	echo ""
done < $INPUT
IFS=$OLDIFS
