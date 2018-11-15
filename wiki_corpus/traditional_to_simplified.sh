#!/bin/bash
path=$(pwd)
echo $path

for folder in $(ls wiki_ch) 
do 
    echo "folder: $folder"
    mkdir wiki_chs/$folder
    for file in $(ls "$path/wiki_ch/$folder")
    do
        input_file="wiki_ch/$folder/$file"
        output_file="wiki_chs/$folder/$file"
        opencc -i $input_file -o $output_file -c t2s.json
	done
done
