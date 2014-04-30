from base import support
from itertools import combinations


def flat_set(sequences):
    itens = set()
    for sequence in sequences:
        for item in sequence:
            itens.add(item)
    return itens


def c1(sequences):
    return set((x,) for x in flat_set(sequences))


def generate_ck(fk_1, k):
    itens = set()
    for combination in combinations(flat_set(fk_1), k):
        scomb = sorted(combination)
        k_1 = scomb[-1]
        k_2 = scomb[-2]
        kcomb = scomb[:-2]
        if (tuple(kcomb + [k_1]) in fk_1 and
                tuple(kcomb + [k_2]) in fk_1 and
                tuple(scomb[1:]) in fk_1):
            itens.add(tuple(scomb))
    return itens


def frequent(sequences, itens, min_supp):
    result = set()
    for item in itens:
        if support(sequences, item) >= min_supp:
            result.add(item)
    return result


def apriori(sequences, min_supp=0.5):
    frequents = {1: frequent(sequences, c1(sequences), min_supp)}
    k = 1
    while frequents[k]:
        k += 1
        ck = generate_ck(frequents[k - 1], k)
        frequents[k] = frequent(sequences, ck, min_supp)

    del frequents[1]
    return reduce(lambda x, y: x.union(y), frequents.values(), set())
