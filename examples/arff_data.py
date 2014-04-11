import sys
sys.path.append("..")

from functools import partial

from data_mining.parsers.weka_arff import parse
from data_mining.classifiers.id3 import build_id3, Condition
from data_mining.classifiers.knn import build_knn, manhattan
from data_mining.classifiers.naive_bayes import build_naive_bayes
from data_mining.helpers import evaluate

ES, EI, EA = 'Self', 'Industry', 'Academia'
GA, GB, GC = 'A', 'B', 'C'

data = parse('weather.nominal.arff')

attr = [u'outlook', u'temperature', u'humidity', u'windy',]
cls = u'play'


new_element = {
    'outlook': 'sunny',
    'temperature': 'mild',
    'humidity': 'high',
    'windy': 'TRUE',
}

conditions = {
 
}

k_fold = 5

print("id3")
tree = build_id3(data, attr, cls, default_conditions=conditions)
tree.show()
print(tree.classify(new_element))

evaluate(data, attr, cls, k_fold,
    partial(build_id3, default_conditions=conditions))


print("\n\nknn")
w = {
    
}

knn = build_knn(data, attr, cls, k=7, w=w, comp_func=manhattan)
print(knn.classify(new_element))

evaluate(data, attr, cls, k_fold,
    partial(build_knn, k=7, w=w, comp_func=manhattan))


print("\n\nnaive_bayes")
naive_bayes = build_naive_bayes(data, attr, cls, adjust=True)
print(naive_bayes.classify(new_element))

evaluate(data, attr, cls, k_fold,
    partial(build_naive_bayes, adjust=True))



