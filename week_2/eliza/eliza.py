import re, debug_tools
from collections import defaultdict

# @debug_tools.debug_print
def parenthesis_parser(string):
    string = [s.strip() for s in re.split('([\(\)\ ])', string) if s not in ('', ' ', '\'')]
#     print(string)
    stack_level = 0
    result = defaultdict(list)
    
    for s in string:
        if s == '(': 
            stack_level += 1         
        elif s == ')':
            result[stack_level-1].append(tuple(result.pop(stack_level)))
            stack_level -= 1          
        elif s!='': result[stack_level].append(s)
#         print(result)
            
    return result[0]

#------------------------------------------------------------------------------

import functools
import debug_tools

def variable_p(x:str):
    return type(x)==str and x[0] == '?'


def get_binding(var:str, bindings:dict):
    if var in bindings:
        return (var, bindings[var])
    else:
        return False

def binding_val(binding:tuple):
    return binding[1]

def lookup(var:str, bindings:dict):
    return binding_val(get_binding(var, bindings))

def extend_bindings(var:str, val:str, bindings:dict):
    bindings[var] = val
    return bindings
    

def consp(x:tuple):
    return type(x) == tuple

# @debug_tools.debug_print
def match_variable(var:str, _input:tuple, bindings:dict):
    binding = get_binding(var, bindings)
    
#     print(_input, binding_val(binding))
    
    if not binding:
        extend_bindings(var, _input, bindings=bindings)
        return bindings

    elif _input == binding_val(binding):
        return bindings
    
    else:
        return False

#------------------------------------------------------------------------------

# @debug_tools.debug_print
def pat_match(pattern:tuple, _input:tuple, bindings=dict()):
    #"Does pattern match input? Any variable can match anything."
    if bindings == False:
        return False
    
    elif variable_p(pattern):
        return match_variable(pattern, _input, bindings=bindings)
    
    elif (pattern == _input):
        return bindings
    
    elif segment_pattern_p(pattern):
        return segment_match(pattern, _input, bindings)
    
    elif consp(pattern) and consp(_input):
        return pat_match(pattern[1:], _input[1:], bindings=pat_match(pattern[0], _input[0], bindings=bindings))
    
    else:
        return False
    
def segment_pattern_p(pattern:tuple):
    return consp(pattern) and start_with(pattern[0], '?*')

def start_with(pattern:tuple, symb:str):
    if consp(pattern):
        return pattern[0] == symb
    else:
        return pattern == symb

# @debug_tools.debug_print
def position(var:str, lst:tuple, start:int):
    lst = lst[start:]
    if var in lst:
        return lst.index(var) + start
    else: 
        return None
    
#@debug_tools.debug_print
def segment_match(pattern:tuple, _input:tuple, bindings:dict, start=0):
    var = pattern[0][1]
    pat = pattern[1:]

    if not pat:
        return match_variable(var, _input, bindings=bindings)
    else:
        pos = position(pat[0], _input, start)
#         print(pos, pat[0], _input)
        if pos == None:
            return False
        else:
            b2 = pat_match(pat, _input[pos:], bindings=bindings)
            if b2 == False:
                return segment_match(pattern, _input, bindings=bindings, start=pos+1)
            else:
                return match_variable(var, tuple(_input[0:pos]), bindings=b2)


#------------------------------------------------------------------------------
import random

def use_eliza_rule(_input:list):
    global eliza_rules  
    _input = tuple(_input.split(' '))
    for pattern in eliza_rules:    
        result = pat_match(pattern, _input, bindings=dict())
        if result != False:
            return sublis(switch_viewpoint(result), random.choice(eliza_rules[pattern]))    
    return '#No pattern detected#'
        
def switch_viewpoint(bindings:dict):
    def switch(words:tuple):
        switch_words = {'i':'you', 'you':'i', 'me':'you', 'am':'are'}
        return [switch_words[w] if w in switch_words else w for w in words]  
    return {pattern: switch(value) for pattern, value in bindings.items()}

#@debug_tools.debug_print
def sublis(bindings:dict, pattern:tuple):
    if type(pattern)==str:
        if pattern in bindings:
            return ' '.join(bindings[pattern])
        else:
            return pattern
    else: 
        return ' '.join([sublis(bindings, e) for e in pattern if e!='?*'])

rules = '''
  '(((?* ?x) hello (?* ?y))
     (how do you do. Please state your problem.))
    (((?* ?x) i want (?* ?y))
     (what would it mean if you got ?y)
     (why do you want ?y))
    (((?* ?x) if (?* ?y))
     (do you really think its likely that ?y)
     (what do you think about ?y)
     (really-- if ?y))
    (((?* ?x) no (?* ?y))
     (why not?)
     (you are being a bit negative)
     (are you saying "NO" just to be negative?))
    (((?* ?x) i feel (?* ?y))
     (do you often feel ?y ?))
    (((?* ?x) i felt (?* ?y))
     (what other feelings do you have?))
'''

def get_eliza_rules(rules):
    eliza_rules = dict()
    for e in parenthesis_parser(rules):
        pattern = e[0]
        responses = e[1:]
        eliza_rules[pattern] = responses
    return eliza_rules
    
eliza_rules = get_eliza_rules(rules)
#------------------------------------------------------------------------------
def eliza():
    print('ELIZA PROGRAM')
    _input = ''
    while _input != 'exit':
        _input = input('input:\t')
        print('eliza:\t', use_eliza_rule(_input))
#------------------------------------------------------------------------------
if __name__ == '__main__':
    eliza()