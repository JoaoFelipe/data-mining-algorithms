
import sys
sys.path.append("..")

from data_mining.association_rule.base import rules
from data_mining.association_rule.apriori import apriori


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

print rules(data["itens"], apriori(data["itens"], 0.3), 0.8)
