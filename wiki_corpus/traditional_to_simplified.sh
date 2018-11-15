#!/bin/bash
path=$(pwd)
echo $path

for folder in $(ls wiki_ch) 
do 
	echo "folder: $folder"
	for file in $(ls "$path/wiki_ch/$folder")
	do
		echo "    file: $file"
	done
done
