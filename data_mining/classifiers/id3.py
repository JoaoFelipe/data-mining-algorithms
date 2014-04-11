# coding: utf-8

from collections import namedtuple, Counter
from functools import partial
from copy import deepcopy
from math import log
from data_mining.utils.attributes import continuous
from data_mining.classifiers.base import Classifier



Predominant = namedtuple('Predominant', 'value cls count')
Attribute = namedtuple('Attribute', 'name conditions')
Condition = namedtuple('Condition', 'name check')

class Leaf(object):
    def __init__(self, name, error, condition=None):
        self.name = name
        self.error = error
        self.condition = condition

    def show(self, ident=0):
        text = '.'*ident*4
        text += (str(self.condition.name) + ' ' if self.condition else '') + self.name + ' ' + str(self.error)
        print text

    def classify(self, item):
        return self.name

class Node(Classifier):

    def __init__(self, name="root"):
        self.children = []
        self.name = name
        self.condition = None

    def add(self, node):
        self.children.append(node)

    def show(self, ident=0):
        text = '.'*ident*4
        text += (str(self.condition.name) + ' ' if self.condition else '') + self.name 
        print text
        for child in self.children:
            child.show(ident=ident+1)

    def classify(self, item):
        value = item[self.name]
        for child in self.children:
            if child.condition.check(value):
                return child.classify(item)
        return 'Fail'


def all_equal(iterator):
      try:
         iterator = iter(iterator)
         first = next(iterator)
         return all(first == rest for rest in iterator)
      except StopIteration:
         return True

def predominant(data, cls):
    most_common = Counter(data[cls]).most_common(1)
    return Leaf(
        most_common[0][0], 
        1.0 - most_common[0][1] / float(len(data[cls]))
    )

def copy_data(original, index, new):
    for attribute, lis in original.items():
        if attribute not in new:
            new[attribute] = []
        new[attribute].append(lis[index])

def generate_conditions(data, attr, cls, default_conditions={}):
    if not data[attr]:
        return []
    if attr in default_conditions:
        return default_conditions[attr]
    if not continuous(data[attr][0]):
        return [Condition('=="%s"'%(value), partial((lambda v, x:x == v), value)) for value in set(data[attr])]
    result = {}
    for value in set(data[attr]):
        result[value] = {
            '<=': Counter(),
            '>': Counter(),
        }
    count = 0.0
    for i, value in enumerate(data[attr]):
        cls_value = data[cls][i]
        for base in result:
            if value <= base:
                result[base]['<='][cls_value] += 1
            else:
                result[base]['>'][cls_value] += 1
        count += 1.0
    for base in result:
        sv1 =  sum(result[base]['<='].values())
        sv2 =  sum(result[base]['>'].values())
        result[base]['<='] =sv1*entropy_from_counter(result[base]['<=']) / count
        result[base]['>'] = sv2*entropy_from_counter(result[base]['>']) / count
        result[base] = result[base]['<='] + result[base]['>']
    number = min(result, key=result.get)
    return [
        Condition('<=' + str(number), lambda x: x <= number),
        Condition('>' + str(number), lambda x: x > number)
    ]

def entropy_from_counter(counter):
    size = float(sum(counter.values()))
    return sum(
        -(quantity / size) * log(quantity / size, 2) 
        for value, quantity in counter.items()
    )

def entropy(data, cls):
    counter = Counter(data[cls])
    return entropy_from_counter(counter)


def best_attribute(data, attributes, cls, default_conditions={}):
    es = entropy(data, cls)
    s = float(len(data[cls]))
    conditions_by_attr = {}
    partitions_by_attr = {}
    entropies = {}
    for attribute in attributes:
        conditions_by_attr[attribute] = generate_conditions(data, attribute, cls, default_conditions=default_conditions)
        partitions_by_attr[attribute] = create_partitions(data, attribute, conditions_by_attr[attribute])
        esa = 0.0
        for name, part_data in partitions_by_attr[attribute].items():
            if part_data:
                sv = float(len(part_data[cls]))
                esv = entropy(part_data, cls)
                esa += esv * sv / s
        entropies[attribute] = esa
    result = max(entropies, key=lambda x: es - entropies[x])
    return Attribute(result, conditions_by_attr[result]), partitions_by_attr[result] 
    
def create_partitions(data, attribute, conditions):
    partitions = {}
    for condition in conditions:
        partitions[condition] = {}
    else_partition = Condition('else', lambda x: not any(c.check(x) for c in conditions))
    partitions[else_partition] = {}
    for i, value in enumerate(data[attribute]):
        found = False
        for condition in conditions:
            if condition.check(value):
                found = True
                copy_data(data, i, partitions[condition])
        if not found:
            copy_data(data, i, partitions[else_partition])
    return partitions


def build_id3(data, attributes, cls, node=None, condition=None, 
        default_conditions={}):
    if not all_equal(data[cls]): 
        if len(attributes) > 0:
            best, partitions = best_attribute(data, attributes, cls, 
                default_conditions=default_conditions)
            result = Node(best.name)
            new_attributes = deepcopy(attributes)
            new_attributes.remove(best.name)
            for part_condition, partition_data in partitions.items():
                if partition_data:
                    build_id3(partition_data, new_attributes, cls, 
                        node=result, condition=part_condition,
                        default_conditions=default_conditions)
        else:
            result = predominant(data, cls)
    else:
        result = Leaf(data[cls][0], 0.0)
    if node:
        result.condition = condition
        node.add(result)
    return result
