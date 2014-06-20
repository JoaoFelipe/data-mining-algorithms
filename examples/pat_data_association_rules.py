
import sys
sys.path.append("..")

from data_mining.association_rule.base import rules, lift, support
from data_mining.association_rule.apriori import apriori
from data_mining.association_rule.liftmin import apriorilift


def load_data(fil):
    with open(fil, 'r') as f:
        reading = False
        result = []
        for line in f:
            if reading and line:
                result.append([x for x in line.strip().split(' ')[4:] if x])
            if 'ItemSets:' in line:
                reading = True
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


if __name__ == "__main__":
    data = load_data("t1.pat")
    print 'apriori'
    mine_rules(data, apriori, 0.01, 0)
    print "----------------"
    print 'apriorilift'
    mine_rules(data, apriorilift, 5.0, 0)
