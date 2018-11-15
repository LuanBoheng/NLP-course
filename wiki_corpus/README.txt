down load wiki data via:
bash download_wikipages.sh

clone wiki extractor:
git clone https://github.com/attardi/wikiextractor 


extract xml files to folder ‘wiki_ch’:
bash extract_wikich.sh

繁简转换(single file):
install: sudo apt-get install opencc
command: opencc -i input_file -o output_file -c t2s.json

or run following script convert all corpus:
bash traditional_to_simplified.sh