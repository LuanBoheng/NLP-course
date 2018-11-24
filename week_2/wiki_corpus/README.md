1. down load wiki data via:

```shell
mkdir big_files
bash download_wikipages.sh
```

all downloaded content and its decompression should be put into the folder **big_files**

2. clone wiki extractor:

```shell
git clone https://github.com/attardi/wikiextractor 
```

3. extract xml files to folder **wiki_ch** under current dir:

```bash extract_wikich.sh
bash extract_wikich.sh
```

4. then make a new folder **wiki_chs** to store simplified Chinese corpus:

```shell
mkdir wiki_chs
```

5. 繁简转换(single file):

   use **opencc** to convert corpus, **opencc** usage:

```shel
sudo apt-get install opencc
opencc -i input_file -o output_file -c t2s.json
```

or run following script convert all corpus:

```shell
bash traditional_to_simplified.sh
```

by the end all corpus in simplified Chinese are in the folder **wiki_chs**



following folders should be included in the **.gitignore**

* **big_files**

* **wiki_ch**

* **wiki_chs**