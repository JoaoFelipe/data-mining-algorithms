from data_mining.evaluation.hold_out import hold_out
from data_mining.evaluation.random_subsampling import random_subsampling
from data_mining.evaluation.k_fold_cross_validation import k_fold_cross_validation
from data_mining.evaluation.stratified_cross_validation import stratified_cross_validation
from data_mining.evaluation.leave_one_out import leave_one_out

def evaluate(data, attributes, cls, k_fold, build_classifier):
	print("-> Hold out")
	print(hold_out(data, attributes, cls, build_classifier))
	print("-> Random Subsampling")
	print(random_subsampling(data, attributes, cls, build_classifier))
	print("-> k(%d) fold cross validation" % (k_fold))
	print(k_fold_cross_validation(data, attributes, cls, k_fold, 
								  build_classifier))
	print("-> stratified(%d) cross validation" % (k_fold))
	print(stratified_cross_validation(data, attributes, cls, k_fold, 
									  build_classifier))
	print("-> leave-one-out")
	print(leave_one_out(data, attributes, cls, build_classifier))

