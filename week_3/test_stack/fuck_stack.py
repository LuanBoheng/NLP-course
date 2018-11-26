def fuck_stack(n=0):
    #a = range(100000)
    if n % 100 == 0: print(n)
    return fuck_stack(n+1)

fuck_stack()
