from itertools import combinations


def count_set(sequences, tset):
    return sum(
        1.0 for s in sequences if len(tset.intersection(s)) == len(tset)
    )


def support(sequences, x, y=[]):
    union = set(x).union(y)
    count_xUy = count_set(sequences, union)
    return count_xUy / float(len(sequences))


def conf(sequences, x, y):
    union = set(x).union(y)
    x = set(x)
    count_xUy = count_set(sequences, union)
    count_x = count_set(sequences, x)
    return count_xUy / count_x


def rules(sequences, frequents, min_conf=0.6):
    result = {}
    for frequent in frequents:
        for i in range(1, len(frequent)):
            combs = combinations(frequent, i)
            for comb in combs:
                x = tuple(comb)
                y = tuple(a for a in frequent if a not in x)
                cf = conf(sequences, x, y)
                if cf >= min_conf:
                    result[(x, y)] = cf
    return result
