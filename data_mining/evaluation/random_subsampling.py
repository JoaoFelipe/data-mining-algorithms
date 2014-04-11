from .hold_out import hold_out


def random_subsampling(data, attributes, cls, build_classifier, k=5):
	accuracy_sum, error_rate_sum = 0.0, 0.0
	for i in range(k):
		ho = hold_out(data, attributes, cls, build_classifier)
		accuracy_sum += ho['accuracy']
		error_rate_sum += ho['error_rate']
	return {
		'accuracy': accuracy_sum / k, 
		'error_rate': error_rate_sum / k
	}
