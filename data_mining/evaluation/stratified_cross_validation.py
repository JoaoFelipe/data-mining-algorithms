import random
from collections import defaultdict
from copy import copy

from .k_fold_cross_validation import cross_validation


def stratified_cross_validation(data, attributes, cls, k, build_classifier):
	# It may be biased
	i_cls = [(i, data[cls][i]) for i in range(len(data[cls]))]
	i_by_cls = defaultdict(list)
	for index, c in i_cls: 
		i_by_cls[c].append(index)

	fold_indexes = [[] for _ in range(k)]
	current = 0
	added = 0
	while added != len(i_cls):
		for cls_value in i_by_cls:
			indexes = i_by_cls[cls_value]
			random.shuffle(indexes)
			step = 0
			for index in copy(indexes):
				fold_indexes[current].append(index)
				indexes.remove(index)
				step += 1
				added += 1
				current = (current + 1) % k
				if step == k:
					break
			i_by_cls[cls_value] = indexes
			
	return cross_validation(data, attributes, cls, 
							fold_indexes, build_classifier)
