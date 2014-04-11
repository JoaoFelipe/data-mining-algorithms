import random

from .base import div_data, matches

def hold_out(data, attributes, cls, build_classifier):
	indexes = range(len(data[cls]))
	test_indexes = random.sample(indexes, len(indexes) // 3)
	training_indexes = [i for i in indexes if i not in test_indexes]
	test_data, training_data = div_data(data, [test_indexes, training_indexes])
	classifier = build_classifier(training_data, attributes, cls)
	ok, fail = matches(test_data, classifier, attributes, cls)
	return {
		'accuracy': ok / len(test_indexes), 
		'error_rate': fail / len(test_indexes)
	}
