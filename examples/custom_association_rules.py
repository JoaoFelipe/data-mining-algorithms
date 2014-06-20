
import sys
sys.path.append("..")

from data_mining.association_rule.base import rules, lift, support
from data_mining.association_rule.apriori import apriori
from data_mining.association_rule.liftmin import apriorilift


LE = "leite"
PA = "pao"
SU = "suco"
OV = "ovos"
CA = "cafe"
BI = "biscoito"
AR = "arroz"
FE = "feijao"
CE = "cerveja"
MA = "manteiga"

data = {
    "tid": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "itens": [[CA, PA, MA], [LE, CE, PA, MA], [CA, PA, MA], [LE, CA, PA, MA],
              [CE], [MA], [PA], [FE], [AR, FE], [AR]]
}

r = rules(data["itens"], apriori(data["itens"], 0.00000000000000000000001), 0)
keys = sorted(
    r,
    reverse=True,
    key=lambda rule: lift(data["itens"], rule[0], rule[1])
)
x = max(len(str(rule)) for rule in keys)
i = 0

print("ID \t Regra %s Lift \t\t Conf \t\t Sup" % (" "*(x - len("Regra"))))


for rule in keys:
    print("%d \t %s %s %f \t %f \t %f" % (
        i,
        str(rule), 
        " "*(x - len(str(rule))),
        lift(data["itens"], rule[0], rule[1]), 
        r[rule], 
        support(data["itens"], rule[0], rule[1])
    ))
    i += 1
print "----------------"
print len(apriori(data["itens"], 0.00000000000001))
print "----------------"
print len(apriorilift(data["itens"], 5.0))

print "----------------"
r = rules(data["itens"], apriorilift(data["itens"], 5.0), 0)
keys = sorted(
    r,
    reverse=True,
    key=lambda rule: lift(data["itens"], rule[0], rule[1])
)
x = max(len(str(rule)) for rule in keys)
i = 0

print("ID \t Regra %s Lift \t\t Conf \t\t Sup" % (" "*(x - len("Regra"))))


for rule in keys:
    print("%d \t %s %s %f \t %f \t %f" % (
        i,
        str(rule), 
        " "*(x - len(str(rule))),
        lift(data["itens"], rule[0], rule[1]), 
        r[rule], 
        support(data["itens"], rule[0], rule[1])
    ))
    i += 1