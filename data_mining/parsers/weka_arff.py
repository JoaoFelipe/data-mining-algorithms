# coding: utf-8

import arff

def parse(file_name):
	result = {}
	with open(file_name, 'rb') as f:
		data = arff.load(f)
		for i, attr in enumerate(data[u'attributes']):
			result[attr[0]] = [row[i] for row in data[u'data']]
	return result