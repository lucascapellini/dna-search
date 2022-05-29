import os
import sys

sys.path.append(os.path.dirname('C:\\Users\\mrluc\\anaconda3\\Lib\\site-packages\\ultrades'))
import ultrades

sys.path.append(os.path.dirname(ultrades.__file__))
import re
from random import choice

from ultrades.automata import *

possibleEvents = ["A", "T", "C", "G"]

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

def getTransitionData(prevState, event, nextState):
    return (prevState, event, nextState)

def createTransitions(prevState, events, nextState):
    transitions = []
    for event in events:
        transitions.append(getTransitionData(prevState, getEvent(event), nextState))
    
    return transitions

def otherEvents(events):
    eventsCopy = possibleEvents
    for event in eventsCopy:
        if(event in events):
            eventsCopy.remove(event)
    return eventsCopy
    

def createDnaSearcherAutomaton(sequence):
    automatonTransitions = []

    firstState = state("0", marked=False)
    # lastState = state(str(len(sequence)), marked=True)
    allStates = []

    allStates.append(firstState)
    
    for index in range(len(sequence)):
        index += 1
        if(index == (len(sequence))):
            allStates.append(state(str(index), marked=True))
        else:
            allStates.append(state(str(index), marked=False))

    
    print(len(allStates))
    
    for index in range(len(sequence)):
        currentState = allStates[index]
        nextState = allStates[index + 1]
        
        currentEvent = getEvent(sequence[index])
        transition = getTransitionData(currentState, currentEvent, nextState)
        automatonTransitions.append(transition)
        
        print(currentState, nextState, index)
        

        if(index == 1):
            automatonTransitions.extend(createTransitions(currentState, otherEvents([sequence[1], sequence[0]]), allStates[index - 1]))
            automatonTransitions.append(getTransitionData(currentState, getEvent(sequence[0]), currentState))
        else:
            automatonTransitions.extend(createTransitions(currentState, otherEvents([sequence[index], sequence[0]]), allStates[0]))
            automatonTransitions.append(getTransitionData(currentState, getEvent(sequence[0]), allStates[1]))
            
            


    G1 = dfa(automatonTransitions, firstState, "G1")

    return G1



def dnaSample(length):
    DNA = ""
    for count in range(length):
        DNA += choice ("CGTA")
    return DNA

dnaForTest = dnaSample(4)

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

g = createDnaSearcherAutomaton(dnaForTest)
# write_xml(g, r"C:\Users\mrluc\Downloads")
automatonImage = show_automaton(g)

print(dnaForTest)
print(automatonImage.data)
