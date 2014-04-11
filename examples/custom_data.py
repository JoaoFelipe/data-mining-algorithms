
import sys
sys.path.append("..")

from functools import partial

from data_mining.classifiers.id3 import build_id3, Condition
from data_mining.classifiers.knn import build_knn, manhattan
from data_mining.classifiers.naive_bayes import build_naive_bayes
from data_mining.helpers import evaluate

ES, EI, EA = 'Self', 'Industry', 'Academia'
GA, GB, GC = 'A', 'B', 'C'

data = {
    'salary':     [30, 40, 70, 60, 70, 60, 60, 70, 40, 70, 60, 70, 60,],
    'age':        [30, 35, 50, 45, 30, 35, 35, 30, 45, 35, 35, 30, 30,],
    'employment': [ES, EI, EA, ES, EA, EI, ES, ES, EI, ES, EI, EI, EI,],
    'group':      [GB, GB, GC, GC, GB, GB, GA, GA, GB, GB, GB, GB, GA,],
}


data2 = {
    'salary':     [30, 40, 70, 60, 70, 60, 60, 70, 40,],
    'age':        [30, 35, 50, 45, 30, 35, 35, 30, 45,],
    'employment': [ES, EI, EA, ES, EA, EI, ES, ES, EI,],
    'group':      [GB, GB, GC, GC, GB, GB, GA, GA, GB,],
}


attr = ['salary', 'age', 'employment']
cls = 'group'


new_element = {
    'salary': 40,
    'age': 35,
    'employment': EI,
}

k_fold = 5


conditions = {
   #'age': [Condition('<=40', lambda x: x<=40), Condition('>40', lambda x: x>40),],
   #'salary': [Condition('<=50', lambda x: x<=50), Condition('>50', lambda x: x>50),]
       
}


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
