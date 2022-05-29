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
    eventsCopy = ["A", "C", "G", "T"]
    for event in ["A", "C", "G", "T"]:
        print(events, event, eventsCopy)
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

    
    # print(len(allStates))
    
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
            
    automatonTransitions.extend(createTransitions(allStates[len(allStates) - 1], otherEvents([sequence[0], sequence[len(sequence) - 1]]), allStates[0]))


    G1 = dfa(automatonTransitions, firstState, "G1")

    return G1

def formatSequence(originalSequence: str):
    dnasList = list(originalSequence)
    
    for index in range(len(dnasList)):
        if(dnasList[0] == dnasList[1]):
            dnasList.remove(dnasList[0])
    
    return "".join(dnasList)

def dnaSample(length):
    DNA = ""
    for count in range(length):
        DNA += choice ("CGTA")
    return DNA

# dnaForTest = dnaSample(4)

dnaForTest = "AACCGATTCCGA"
  
print(dnaForTest)

formatedDNASequence = formatSequence(dnaForTest)

print(formatedDNASequence)
g = createDnaSearcherAutomaton(formatedDNASequence)


automatonImage = show_automaton(g)

print(automatonImage.data)
