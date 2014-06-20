
import sys
sys.path.append("..")

import re
pattern = re.compile(r'\s+')

from data_mining.association_rule.base import rules, lift, support
from data_mining.association_rule.apriori import apriori
from data_mining.association_rule.liftmin import apriorilift


def load_data(fil):
    with open(fil, 'r') as f:
        result = []
        for line in f:
            line = re.sub(pattern, ' ', line).strip().split(' ')
            tid = int(line[0]) - 1
            if tid >= len(result):
                result.append([])
            result[tid].append(line[-1])
            
    return result


def mine_rules(data, fn, mini, conf):
    d = fn(data, mini)
    print "Conjuntos: ", len(d)
    if not d:
        return
    r = rules(data, d, conf)
    keys = sorted(
        r,
        reverse=True,
        key=lambda rule: lift(data, rule[0], rule[1])
    )
    x = max(len(str(rule)) for rule in keys)
    i = 0

    print("ID \t Regra %s Lift \t\t Conf \t\t Sup" % (" "*(x - len("Regra"))))


    for rule in keys:
        print("%d \t %s %s %f \t %f \t %f" % (
            i,
            str(rule), 
            " "*(x - len(str(rule))),
            lift(data, rule[0], rule[1]), 
            r[rule], 
            support(data, rule[0], rule[1])
        ))
        i += 1

def compare(data, supmin, liftmin, confmin):
    print 'apriori'
    mine_rules(data, apriori, supmin, confmin)
    print "----------------"
    print 'apriorilift'
    mine_rules(data, apriorilift, liftmin, confmin)

if __name__ == "__main__":
    data = load_data("t1.data")
    compare(data, 0.000000001, 5.0, 0)
