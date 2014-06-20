
import sys
sys.path.append("..")

from data_mining.association_rule.base import rules, lift, support
from data_mining.association_rule.apriori import apriori
from data_mining.association_rule.liftmin import apriorilift
from pat_data_association_rules import compare

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

data = [[CA, PA, MA], [LE, CE, PA, MA], [CA, PA, MA], [LE, CA, PA, MA],
        [CE], [MA], [PA], [FE], [AR, FE], [AR]]

compare(data, 0.0000000001, 5.0, 0)
