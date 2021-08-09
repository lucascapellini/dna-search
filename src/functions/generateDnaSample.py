from random import choice

def dnaSample(length):
    DNA = ""
    for count in range(length):
        DNA += choice ("CGTA")
    return DNA