from .k_fold_cross_validation import k_fold_cross_validation

def leave_one_out(data, attributes, cls, build_classifier):
	return k_fold_cross_validation(data, attributes, cls, len(data[cls]),
								   build_classifier)
