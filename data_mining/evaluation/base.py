def div_data(data, fold_indexes):
	datas = [{} for _ in range(len(fold_indexes))]

	test_data = {}
	training_data = {}
	for attr, values in data.items():
		for new_data in datas:
			new_data[attr] = []
		for i, value in enumerate(values):
			for fold_index, fold in enumerate(fold_indexes):
				if i in fold:
					datas[fold_index][attr].append(value)
	return datas

def matches(test_data, classifier, attributes, cls):
	ok = 0.0
	fail = 0.0
	for i, expected in enumerate(test_data[cls]):
		element = {attr:test_data[attr][i] for attr in attributes}
		if classifier.classify(element) == expected:
			ok += 1.0
		else:
		 	fail += 1.0
	return ok, fail