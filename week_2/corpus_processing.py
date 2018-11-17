# usd BFS search, return all corpus files as a list of string
import os
def get_corpus():
    corpus_path = '../wiki_corpus/wiki_chs'
    corpus_list = []
    need_visit = [corpus_path]
    while need_visit:
        path = need_visit.pop(0)
        if os.path.isdir(path):
            need_visit += [path + '/' + p for p in os.listdir(path)]
        elif '.DS_Store' not in path:
            corpus_list.append(path)
    return corpus_list

#------------------------------------------------------------------------------
# corpus processing functions
import re
import jieba
from collections import Counter
from functools import partial, reduce
stop_words = ['的', '在', '是', 'doc', '为', '和', '了', 'zh', 'id', 'org', 'https', 'wiki', 'wikipedia', 
              'title', 'url', 'curid', '与', '于', '中', '被', '也', '一个', '后', '并', '而', '以', '由', 
              '及', '但', '将', '时', '其', '到', '对', '位于', '至', '会', '或', '可以', '之', '该', '则', 
              '从', '这', '以及', '其中', '所', '就', '个', '曾', '又', '亦', '可', '它', '地', '来']
stop_words = set(stop_words)

def replace_nums(string):
    return '<num>' if string.isnumeric() else string
    
# modified tokenize function remove stop words
def tokenize_string(string):
    global gram_level # this could be changed outside
    clauses = [jieba.cut(c) for c in re.findall('[\w|\d]+', string)]
    tokens = [replace_nums(w) for c in clauses for w in list(c) if w not in stop_words]
    if gram_level == 'char': # do char counting
        tokens = ''.join(tokens)
    return tokens

def get_ngram(string, n):
    tokens = tokenize_string(string)
    ngrams = [tuple(tokens[i-n:i]) for i in range(len(tokens)+1) if i >= n]
    return ngrams
    
def count_ngram(string, n):
    return Counter(get_ngram(string, n))


def process_file(input_file, process_func):
    with open(input_file, 'r') as f:
        return process_func(f.read())

#------------------------------------------------------------------------------
#Multicore map reduce
import time
import multiprocessing
def multiprocess_count_ngram(batch_file, N):
    pool = multiprocessing.Pool()
    target_func = partial(process_file, process_func=partial(count_ngram, n=N))
    ngram_counts = pool.map(target_func, batch_file)
    pool.close()
    pool.join()
    result = reduce(lambda x, y : x + y, ngram_counts)
    result = Counter({k:v for k,v in result.items() if v > 1}) #saving memory
    return result

#------------------------------------------------------------------------------
# cut whole task in to chunck
from tqdm import tqdm

def cut_list(data, batch_size):
    return [data[x:x+batch_size] for x in range(0, len(data), batch_size)]

def wikichs_count_ngram(N, batch_size=16):
    word_count = Counter([])
    corpus_list = get_corpus()
    corpus_chuncks = cut_list(corpus_list, 16)

    for chunck in tqdm(corpus_chuncks):
        word_count += multiprocess_count_ngram(chunck, N)
    return word_count

#------------------------------------------------------------------------------
# save the results on distk
import pickle

def save_obj(obj, file_name):
    pickle.dump(obj, open(file_name, 'wb'))
    
def load_obj(file_name):
    obj = pickle.load(open(file_name, 'rb'))
    return obj


#------------------------------------------------------------------------------
if __name__ == '__main__':
    '''
    DEBUG
    INFO
    WARNING
    ERROR
    CRITICAL
    '''
    
    import logging
    jieba.setLogLevel(logging.WARNING)
    
    def save_ngram(n):
        global gram_level
        print('count_ngram', n, gram_level)
        count_ngram = wikichs_count_ngram(n)
        count_ngram = Counter({k:v for k,v in count_ngram.items() if v > 10}) #save memory
        save_obj(count_ngram, 'data/count_ngram'+str(n) + gram_level)
    
    gram_level = 'char'
    save_ngram(1)
    save_ngram(2)
    
    gram_level = 'word'
    save_ngram(1)
    save_ngram(2)

