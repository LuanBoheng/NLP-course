down load wiki data via:
```shell
bash download_wikipages.sh
```

clone wiki extractor:
```shell
git clone https://github.com/attardi/wikiextractor 
```

extract xml files to folder ‘wiki_ch’ under current dir:

```bash extract_wikich.sh
bash extract_wikich.sh
```

then make a new folder ‘wiki_chs’ to store simplified Chinese corpus:

```shell
mkdir wiki_chs
```

繁简转换(single file):
install:

```shel
sudo apt-get install opencc
```

command: 

```shell
opencc -i input_file -o output_file -c t2s.json
```

or run following script convert all corpus:

```shell
bash traditional_to_simplified.sh
```

by the end all corpus in simplified Chinese are in the folder wiki_chs

