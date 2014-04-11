import random

from .base import div_data, matches

def cross_validation(data, attributes, cls, fold_indexes, build_classifier):
	ok = 0.0
	fail = 0.0
	for test_indexes in fold_indexes:
		training_indexes = sum(
			[d for d in fold_indexes if d != test_indexes], [])
		test_data, training_data = div_data(data, 
			[test_indexes, training_indexes])
		classifier = build_classifier(training_data, attributes, cls)
		c_ok, c_fail = matches(test_data, classifier, attributes, cls)
		ok += c_ok
		fail += c_fail

	return {
		'accuracy': ok / len(data[cls]), 
		'error_rate': fail / len(data[cls])
	}

def k_fold_cross_validation(data, attributes, cls, k, build_classifier):
	indexes = range(len(data[cls]))
	random.shuffle(indexes)
	fold_indexes = [[] for _ in range(k)]
	for position, index in enumerate(indexes):
		fold_indexes[position % k].append(index)

	return cross_validation(data, attributes, cls, 
							fold_indexes, build_classifier)
