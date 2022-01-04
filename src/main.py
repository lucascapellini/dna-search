import os
import sys

sys.path.append(os.path.dirname('C:\\Users\\mrluc\\anaconda3\\Lib\\site-packages\\ultrades'))
import ultrades

sys.path.append(os.path.dirname(ultrades.__file__))
import re
from random import choice

from ultrades.automata import *

def getEvent(eventName):
    if eventName == "A":
            return event("A", controllable=True)
    if eventName == "T":
        return event("T", controllable=True)
    if eventName == "C":
        return event("C", controllable=True)
    if eventName == "G":
        return event("G", controllable=True)
    else:
        return

def createTransition(prevState, event, nextState):
    return (prevState, event, nextState)


def createDnaSearcherAutomaton(sequence):
    automatonTransitions = []

    firstState = state("0", marked=False)
    lastState = state(str(len(sequence) + 1), marked=True)
    allStates = []

    allStates.append(firstState)
    
    for index in range(len(sequence)):
        allStates.append(state(str(index + 1), marked=False))

    allStates.append(lastState)
    
    for index in range(len(sequence)):
        transition = createTransition(allStates[index], getEvent(sequence[index]), allStates[index + 1])
        automatonTransitions.append(transition)
        # print(transition, sequence[index])

    G1 = dfa(automatonTransitions, firstState, "G1")
    print(transitions(G1))
    return G1



def dnaSample(length):
    DNA = ""
    for count in range(length):
        DNA += choice ("CGTA")
    return DNA

dnaForTest = dnaSample(500)
# print(dnaForTest)

s1 = state("s1", marked = True)
s2 = state("s2", marked = False)

e1 = event("e1", controllable = True)
e2 = event("e2", controllable = False)
e3 = event("e3", controllable = True)
e4 = event("e4", controllable = False)

G1 = dfa(
[
    (s1, e1, s2), 
    (s2, e2, s1)
], s1, "G1")
  
G2 = dfa(
[
    (s1, e3, s2), 
    (s2, e4, s1)
], s1, "G2")

Gp = parallel_composition(G1, G2)

show_automaton(Gp)

print(createDnaSearcherAutomaton(dnaSample(5)))
