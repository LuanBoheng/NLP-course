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
import re
import jieba
from collections import Counter
from functools import partial, reduce

def tokenize_string(string):
    clauses = [jieba.cut(c) for c in re.findall('[\w|\d]+', string)]
    tokens = [w for c in clauses for w in list(c)]
    return tokens
    
def count_ngram(string, n):
    tokens = tokenize_string(string)
    ngrams = [tuple(tokens[i-n:i]) for i in range(len(tokens)) if i > n]
    return Counter(ngrams)


def process_file(input_file, process_func):
    with open(input_file, 'r') as f:
        return process_func(f.read())

#------------------------------------------------------------------------------

import time
import multiprocessing
def multiprocess_count_ngram(batch_file, N):
    pool = multiprocessing.Pool()
    target_func = partial(process_file, process_func=partial(count_ngram, n=N))
    ngram_counts = pool.map(target_func, batch_file)
    pool.close()
    pool.join()
    return reduce(lambda x, y : x + y, ngram_counts)

#------------------------------------------------------------------------------

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
if __name__ == '__main__':
    word_count = wikichs_count_ngram(2)
    