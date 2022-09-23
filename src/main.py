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
        if(event in events):
            eventsCopy.remove(event)
    return eventsCopy
    
def createStatesSequence(sequence):
    firstState = state("0", marked=False)
    allStates = []

    allStates.append(firstState)
    
    for index in range(len(sequence)):
        index += 1
        if(index == (len(sequence))):
            allStates.append(state(str(index), marked=True))
        else:
            allStates.append(state(str(index), marked=False))
            
    return allStates

def createDnaSearcherAutomaton(sequence):
    automatonTransitions = []

    allStates = createStatesSequence(sequence)

    
    dnasList = list(sequence)
    repeatsFirstPosition = 0
    
    for index in range(len(dnasList)):
        if(dnasList[index] == dnasList[index + 1]):
            
            currentState = allStates[index]
            nextState = allStates[index + 1]
            
            currentEvent = getEvent(sequence[index])
            transition = getTransitionData(currentState, currentEvent, nextState)
            automatonTransitions.append(transition)
            
            automatonTransitions.extend(createTransitions(currentState, otherEvents([sequence[index], sequence[0]]), allStates[0]))
            # print("automatonTransitions", automatonTransitions)
        
            # dnasList.remove(dnasList[0])
            
            repeatsFirstPosition += 1
        else:
            break
    
    formattedSequence = "".join(dnasList)
    print("formattedSequence and dnasList", formattedSequence, dnasList)
    
    for index in range(len(formattedSequence) - repeatsFirstPosition):
        offSetIndex = index + repeatsFirstPosition
        print("offsetIndex", offSetIndex, repeatsFirstPosition, formattedSequence[offSetIndex])
        currentState = allStates[offSetIndex]
        nextState = allStates[offSetIndex + 1]
        
        currentEvent = getEvent(formattedSequence[offSetIndex])
        transition = getTransitionData(currentState, currentEvent, nextState)
        automatonTransitions.append(transition)
        
        # print(currentState, nextState, offSetIndex)
            

        if(offSetIndex == repeatsFirstPosition + 1):
            automatonTransitions.extend(createTransitions(currentState, otherEvents([formattedSequence[repeatsFirstPosition + 1], formattedSequence[repeatsFirstPosition]]), allStates[offSetIndex - 1]))
            automatonTransitions.append(getTransitionData(currentState, getEvent(formattedSequence[repeatsFirstPosition]), currentState))
        else:
            automatonTransitions.extend(createTransitions(currentState, otherEvents([formattedSequence[offSetIndex], formattedSequence[repeatsFirstPosition]]), allStates[repeatsFirstPosition]))
            automatonTransitions.append(getTransitionData(currentState, getEvent(formattedSequence[repeatsFirstPosition]), allStates[repeatsFirstPosition + 1]))
        
        # print("automatonTransitions", automatonTransitions)
            
    automatonTransitions.extend(createTransitions(allStates[len(allStates) - 1], otherEvents([formattedSequence[0], formattedSequence[len(formattedSequence) - 1]]), allStates[0]))
    automatonTransitions.append(getTransitionData(allStates[len(allStates) - 1], getEvent(formattedSequence[0]), allStates[1]))
    
    


    G1 = dfa(automatonTransitions, allStates[0], "G1")

    return G1

def createDNASequence(roleSequence):
    
    allStates = createStatesSequence(roleSequence)
    automatonTransitions = []
    
    for index in range(len(roleSequence)):
        currentState = allStates[index]
        nextState = allStates[index + 1]
        
        currentEvent = getEvent(roleSequence[index])
        transition = getTransitionData(currentState, currentEvent, nextState)
        automatonTransitions.append(transition)
        
    G2 = dfa(automatonTransitions, allStates[0], "G2")
     
    return G2

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

dnaToFind = "AACCT"
dna = "AAACCT" + dnaSample(5555) + "GAAACCTG"
  
print(dnaToFind, dna)

# formatedDNASequence = formatSequence(dnaToFind)

g1 = createDnaSearcherAutomaton(dnaToFind)
g2 = createDNASequence(dna)

gp = parallel_composition(g1,g2)

# print(gp)

def findMatch(automataResult: str):
    print("autromatonResult", automataResult)
    positinToBeginSearch = automataResult.find("node [shape = circle];")
    positionToFinishSearch = automataResult.find("node [shape = point ]")
    # print("splitResult", automataResult[positinToBeginSearch:positionToFinishSearch])
    filteredAutomataResult = automataResult[positinToBeginSearch:(positionToFinishSearch + 22)]
    cleanResult = filteredAutomataResult.split(" ")
    # print("cleanResult", cleanResult)
    
    statesWithDna = []
    for state in cleanResult:
        # print(state)
        
        positionOfSlash = state.find("|")
        lastNumberCharacter = len(state) - 1
        
        if(len(state) > 1 and state[1].isnumeric() and int(state[1]) == (len(dnaToFind))):
            statesWithDna.append(state[positionOfSlash + 1:lastNumberCharacter])
            # print("CHEGOUUU", state, statesWithDna[1:])
            
    return statesWithDna
    
        

automatonImage = show_automaton(gp)
print("Posições encontradas", findMatch(automatonImage.data))

# print(automatonImage.data)
