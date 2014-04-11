from collections import Counter
from data_mining.utils.attributes import continuous
from data_mining.classifiers.base import Classifier


def diff(x1, x2, comp=None):
    if not comp:
        return x1 - x2
    return comp(x1, x2)

def minkowski(X1, X2, q, COMP=None, W=None):
    if not W:
        W = [1.0 for _ in X1]
    return sum(W[i]*abs(diff(X1[i], X2[i], comp=COMP[i] if COMP else None))**q 
        for i in range(len(X1)))**(1.0/q)

def manhattan(X1, X2, COMP=None, W=None):
    return minkowski(X1, X2, 1, COMP=COMP, W=W)

def euclidian(X1, X2, COMP=None, W=None):
    return minkowski(X1, X2, 2, COMP=COMP, W=W)

def extract_comp(tup):
    result = []
    for element in tup:
        if not continuous(element):
            result.append(lambda x,y: 0 if x == y else 1)
        else:
            result.append(lambda x,y: x - y)
    return result

def extract_normalizer(data, cls):
    result = {}
    for attr, values in data.items():
        if attr == cls:
            continue
        if not continuous(values[0]):
            result[attr] = (lambda x: x)
        else:
            mi, ma = min(values), max(values)
            mi, ma = float(mi), float(ma)
            result[attr] = (lambda x: (float(x) - mi) / ma)
    return result

def knn(data, k, cls, new_element, comp_func=euclidian, w=None):
    if not w:
        w = {}
    dists = {}
    attributes = [attr for attr in data if attr != cls]
    normalizer = extract_normalizer(data, cls)
    for i in range(len(data[cls])):
        tup = tuple([normalizer[attr](data[attr][i]) for attr in attributes])
        dists[tup] = data[cls][i]
    comp = extract_comp(dists.keys()[0])
    new_tup = [normalizer[attr](new_element[attr]) for attr in attributes]
    W = [float(w[attr]) if attr in w else 1.0 for attr in attributes]
    sorted_k_dists = sorted(dists.keys(), reverse=False,
        cmp=(lambda x, y: cmp(comp_func(x, new_tup, COMP=comp, W=W),
                              comp_func(y, new_tup, COMP=comp, W=W))))[0:k]
    counter = Counter()
    for tup in sorted_k_dists:
        counter[dists[tup]] += 1
    return counter.most_common(1)[0][0]


class KnnClassifier(Classifier):

    def __init__(self, data, attributes, cls, 
            k=5, comp_func=euclidian, w=None):
        self.data = data
        self.attributes = attributes
        self.cls = cls
        self.k = k
        self.comp_func = comp_func
        self.w = w

    def classify(self, element):
        return knn(self.data, self.k, self.cls, element, 
            self.comp_func, self.w)


def build_knn(*args, **kwargs):
    return KnnClassifier(*args, **kwargs)