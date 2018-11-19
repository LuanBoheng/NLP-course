import corpus_processing as cp
import debug_tools

count_ngram1word = cp.load_obj('data/count_ngram1word')
count_ngram2word = cp.load_obj('data/count_ngram2word')
count_ngram1char = cp.load_obj('data/count_ngram1char')
count_ngram2char = cp.load_obj('data/count_ngram2char')

#------------------------------------------------------------------------------
from functools import reduce, partial
import logging
import jieba
jieba.setLogLevel(logging.WARNING)

def get_MLE_prob_from_count(count):
    total_count = sum(count.values())
    @debug_tools.debug_print
    def get_prob(w):
        return count[w]/total_count
    return get_prob

def string_ngram_prob(string, prob_func, gram_level, n):
    cp.gram_level = gram_level # this will effect the behavior of 'tokenize_string'
    probs = [prob_func(tuple(token)) for token in cp.get_ngram(string, n)]
    
    if not probs: 
        probs = [0]
    return reduce(lambda x, y: x*y , probs)

get_1gram_prob_char = partial(string_ngram_prob, 
                              prob_func=get_MLE_prob_from_count(count_ngram1char), 
                              gram_level='char', n=1)

get_1gram_prob_word = partial(string_ngram_prob, 
                              prob_func=get_MLE_prob_from_count(count_ngram1word), 
                              gram_level='word', n=1)
#------------------------------------------------------------------------------
def get_conditional_prob(numerator_func, denominator_func):
    @debug_tools.debug_print
    def get_prob(token):
        condition_token = token[:-1]
        return numerator_func(token)/denominator_func(condition_token)
    return get_prob

conditional_prob_char = get_conditional_prob(get_MLE_prob_from_count(count_ngram2char), 
                                             get_MLE_prob_from_count(count_ngram1char))

conditional_prob_word = get_conditional_prob(get_MLE_prob_from_count(count_ngram2word), 
                                             get_MLE_prob_from_count(count_ngram1word))

get_2gram_prob_char = partial(string_ngram_prob, 
                              prob_func=conditional_prob_char, 
                              gram_level='char', n=2)

get_2gram_prob_word = partial(string_ngram_prob, 
                              prob_func=conditional_prob_word, 
                              gram_level='word', n=2)
#------------------------------------------------------------------------------
from collections import defaultdict, Counter
import numpy as np

def count_Nc_from_gram_count(count):
#     def get_Nc_from_c(c, count):
#         selected_grams = list(filter(lambda x:x[1] == c, count.items()))
#         return len(selected_grams)
#     c_max = count.most_common(1)[0][1]
#     N_c = [get_Nc_from_c(c, count) for c in range(c_max+1)] #too complex
# use sorting technics solve this question

    c = count.most_common(1)[0][1]
    N_c = 0
    Nc_pairs = []
    for gram, f in count.most_common():
        if f != c:
            Nc_pairs.append((c, N_c))
            c, N_c = f, 1
        else:
            N_c += 1
    return defaultdict(int, Nc_pairs)

c_to_Nc_ngram1char = count_Nc_from_gram_count(count_ngram1char)
c_to_Nc_ngram2char = count_Nc_from_gram_count(count_ngram2char)
c_to_Nc_ngram1word = count_Nc_from_gram_count(count_ngram1word)
c_to_Nc_ngram2word = count_Nc_from_gram_count(count_ngram2word)
#------------------------------------------------------------------------------
def Turing_smooth(c, c_to_Nc):
    return (c + 1)*(c_to_Nc[c] + 1)/(c_to_Nc[c+1] + 1) #here the smooth function S(N) = N + 1

legend = []
def Turing_estimation_from_count(count, name):
    global legend
    legend.append(name)
    
    c_to_Nc = count_Nc_from_gram_count(count)
    result = {gram: Turing_smooth(c, c_to_Nc) for gram, c in count.items()}
    return defaultdict(lambda :1,result)
    
    
count_ngram1char_Turing = Turing_estimation_from_count(count_ngram1char, 'count_ngram1char')
count_ngram2char_Turing = Turing_estimation_from_count(count_ngram2char, 'count_ngram2char')
count_ngram1word_Turing = Turing_estimation_from_count(count_ngram1word, 'count_ngram1word')
count_ngram2word_Turing = Turing_estimation_from_count(count_ngram2word, 'count_ngram2word')

#------------------------------------------------------------------------------
#unigram
get_1gram_prob_char_Turing = partial(string_ngram_prob, 
                              prob_func=get_MLE_prob_from_count(count_ngram1char_Turing), 
                              gram_level='char', n=1)

get_1gram_prob_word_Turing = partial(string_ngram_prob, 
                              prob_func=get_MLE_prob_from_count(count_ngram1word_Turing), 
                              gram_level='word', n=1)

#bigram
conditional_prob_char_Turing = get_conditional_prob(get_MLE_prob_from_count(count_ngram2char_Turing), 
                                                    get_MLE_prob_from_count(count_ngram1char_Turing))

conditional_prob_word_Turing = get_conditional_prob(get_MLE_prob_from_count(count_ngram2word_Turing), 
                                                    get_MLE_prob_from_count(count_ngram1word_Turing))

get_2gram_prob_char_Turing = partial(string_ngram_prob, 
                                     prob_func=conditional_prob_char_Turing, 
                                     gram_level='char', n=2)

get_2gram_prob_word_Turing = partial(string_ngram_prob, 
                                     prob_func=conditional_prob_word_Turing, 
                                     gram_level='word', n=2)
#------------------------------------------------------------------------------

pair = """前天晚上吃晚饭的时候
前天晚上吃早饭的时候""".split('\n')

pair2 = """正是一个好看的小猫
真是一个好看的小猫""".split('\n')

pair3 = """我无言以对，简直
我简直无言以对""".split('\n')

pairs = [pair, pair2, pair3, ['广州有一个地方叫做沥窖', '杭州有一个地方叫做西湖'], ['这是一个比较常见测试用例','这是一个比较罕见的测试用例']]

def test_pair(pairs, prob_func, name_func):
    print('test function:', name_func)
    for pair in pairs:
        print('===================================')
        for sent in pair:
            print(sent, prob_func(sent))
    print('\n')
#------------------------------------------------------------------------------
if __name__ == '__main__':
    debug_tools.is_debug = True
    pairs = [pairs[1]]

    test_pair(pairs, get_1gram_prob_char, 'get_1gram_prob_char')
    test_pair(pairs, get_1gram_prob_word, 'get_1gram_prob_word')
    test_pair(pairs, get_2gram_prob_char, 'get_2gram_prob_char')
    test_pair(pairs, get_2gram_prob_word, 'get_2gram_prob_word')

    test_pair(pairs, get_1gram_prob_char_Turing, 'get_1gram_prob_char_Turing')
    test_pair(pairs, get_1gram_prob_word_Turing, 'get_1gram_prob_word_Turing')
    test_pair(pairs, get_2gram_prob_char_Turing, 'get_2gram_prob_char_Turing')
    test_pair(pairs, get_2gram_prob_word_Turing, 'get_2gram_prob_word_Turing')