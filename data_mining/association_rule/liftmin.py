from base import support
from itertools import combinations
from collections import Counter


def flat_set(sequences):
    itens = set()
    for sequence in sequences:
        for item in sequence:
            itens.add(item)
    return itens


def generate_ck(fk_1, vertical, k):
    itens = set()
    vertical[k] = {}
    for combination in combinations(flat_set(fk_1), k):
        scomb = sorted(combination)
        k_1 = scomb[-1]
        k_2 = scomb[-2]
        kcomb = scomb[:-2]
        tk_1 = tuple(kcomb + [k_1])
        tk_2 = tuple(kcomb + [k_2])
        tk_0 = tuple(scomb[1:])
        if (tk_1 in fk_1 and tk_2 in fk_1 and tk_0 in fk_1):
            new_tuple = tuple(scomb) 
            intersection = vertical[k - 1][tk_1].intersection(
                vertical[k - 1][tk_2])
            if intersection:
                vertical[k][new_tuple] = intersection
                itens.add(new_tuple)
    return itens


def frequent_lift(sequences, itens, vertical, independent, lift_min):
    result = set()
    for item in itens:
        min_independent = min(independent[i] for i in vertical[item])
        min_supp = lift_min * min_independent
        if support(sequences, item) >= min_supp:
            result.add(item)
    return result


def preprocess(sequences):
    supp = Counter()
    vertical = {1: {}}
    independent = {}
    c1 = set()
    for i, sequence in enumerate(sequences):
        independent[i] = 1.0
        for item in sequence:
            supp[item] += 1.0
            if (item,) not in vertical[1]:
                vertical[1][(item,)] = set()
            vertical[1][(item,)].add(i)
            c1.add((item,))
    size = float(len(sequences))
    for item in supp:
        supp[item] /= size
    for i, sequence in enumerate(sequences):
        for item in sequence:
            independent[i] *= supp[item]
    return supp, vertical, independent, c1 


def apriorilift(sequences, lift_min=2):
    supp, vertical, independent, c1 = preprocess(sequences)

    frequents = {
        1: frequent_lift(sequences, c1, vertical[1], independent, lift_min)
    }
    k = 1
    while frequents[k]:
        k += 1
        ck = generate_ck(frequents[k - 1], vertical, k)
        frequents[k] = frequent_lift(
            sequences, ck, vertical[k], independent, lift_min
        )

    del frequents[1]
    return reduce(lambda x, y: x.union(y), frequents.values(), set())
