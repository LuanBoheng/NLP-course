import time
def debug_print(func):
    def wrapper(*args,**kwargs):
        func_name = func.__qualname__
        output = func(*args,**kwargs)
        print(func_name,(args,kwargs),'=>',output)
        return output
    return wrapper

def timer(func):
    def wrapper(*args,**kwargs):
        start_time = time.time()
        output = func(*args,**kwargs)
        running_time = time.time() - start_time
        print('total_time:',running_time,'s')
        return output
    return wrapper
#------------------------------------------------------------------------------
if __name__ == '__main__':
    #usage:@debug_print
    @debug_print
    def test_func(a, b, c):
        return a+b+c
    
    test_func(1,2,3)
    
    '''
    print out info:
    test_func ((1, 2, 3), {}) => 6
    '''
    
    @timer
    def test_func(a, b, c):
        return a+b+c
    
    test_func(1,2,3)
    
    '''
    print out info:
    total_time: 9.5367431640625e-07 s
    '''
