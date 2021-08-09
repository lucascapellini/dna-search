import sys, ultrades, os
sys.path.append(os.path.dirname(ultrades.__file__))
from ultrades.automata import *

import re
from random import choice

def dnaSample(length):
    DNA = ""
    for count in range(length):
        DNA += choice ("CGTA")
    return DNA

print(dnaSample(52))