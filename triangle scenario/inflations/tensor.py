def tensor(pattern):
    k = len(pattern)

    if k > 2:
        p = [tensor(pattern[0:int(k/2)]), tensor(pattern[int(k/2):k])]
    else:
        p = pattern

    return p
