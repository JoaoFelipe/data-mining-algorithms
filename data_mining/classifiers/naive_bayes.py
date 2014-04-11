from collections import Counter
from math import sqrt, exp, pi
from functools import partial
from data_mining.utils.attributes import continuous
from data_mining.classifiers.base import Classifier

def average(lis):
	return float(sum(lis)) / len(lis)


def variance(lis, avg=None):
	if avg is None:
		avg = average(lis)
	return average([(x - avg) ** 2 for x in lis])


def stddv(lis, avg=None):
	return sqrt(variance(lis, avg=avg))


def gauss(x, a, dv):
	if not dv:
		return 1.0 if x == a else 0.0
	return exp(-((x - a) ** 2) / (2 * dv ** 2)) / sqrt(2 * pi * dv)


def filter_x_given_y(data_x, data_y, y):
	for i in range(len(data_x)):
		if data_y[i] == y:
			yield data_x[i] 
	

def count_x_and_y(data_x, data_y, x, y):
	return sum(
		1.0 for i, _ in enumerate(data_x)
		if data_x[i] == x and data_y[i] == y
	)


def p_categorical(data_x, data_y, x, y, count_y, base_x):
	countx_ci = count_x_and_y(data_x, data_y, x, y)
	px_ci = (countx_ci + base_x) / float(count_y + base_x)
	return px_ci


def p_continuous(data_x, data_y, x, y, count_y, base_x):
	x_given_y = list(filter_x_given_y(data_x, data_y, y))
	avg = average(x_given_y)
	dv = stddv(x_given_y, avg=avg)
	g = gauss(x, avg, dv)
	if not g:
		return (base_x) / float(count_y + base_x)
	return g


def naive_bayes(data, cls, new_tup, adjust=False):
	counter = Counter(data[cls])
	result = Counter()
	for ci, count in counter.items():
		pci = float(count) / float(len(data[cls]))
		mult = 1.0

		base = {x:0.0 for x in new_tup}
		p = {}
		for x, x_value in new_tup.items():
			countx_ci = count_x_and_y(data[x], data[cls], x_value, ci)
			p[x] = p_continuous if continuous(x_value) else p_categorical
			if adjust and not countx_ci:
				base[x] = 1.0

		for x, x_value in new_tup.items():
			px_ci = p[x](data[x], data[cls], x_value, ci, count, base[x])
			mult *= px_ci
		result[ci] = mult * pci
	return result.most_common(1)[0][0]


class NaiveBayesClassifier(Classifier):

    def __init__(self, data, attributes, cls, 
            adjust=False):
        self.data = data
        self.attributes = attributes
        self.cls = cls
        self.adjust = False

    def classify(self, element):
        return naive_bayes(self.data, self.cls, element, self.adjust)


def build_naive_bayes(*args, **kwargs):
    return NaiveBayesClassifier(*args, **kwargs)
