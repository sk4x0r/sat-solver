import re
import Queue
import copy
import sys
import time

GLOBAL_DEBUG=False
def debug(*s):
    if(GLOBAL_DEBUG):
        print s

def copyList(l):
    return copy.deepcopy(l)

    
#Generates set of orthonormal terms, given a list of variables
def generateONSet(unknowns):
    ONSet=[]
    minCount=min(unknowns)
    
    for count in unknowns:
        term=[]
        for count2 in range(minCount,count):
            term.append((-1)*count2)
        term.append(count)
        ONSet.append(term)
    lastTerm=[ -x for x in unknowns]
    ONSet.append(lastTerm)
    return ONSet

def evaluate(formula, assignment, varList, prevAssignment):
    fIter=copyList(formula)
    
    for literal in assignment:
        for term in fIter:
            if literal in term:
                idx=formula.index(term)
                formula[idx].remove(literal)
    
            if (-1)*literal in term:
                formula.remove(term)
        fIter=copyList(formula)
    
    if len(formula)==0:
        print "Solution:",prevAssignment+assignment
        print time.time() - start_time, "seconds"
        sys.exit(0)
        return

    if formula==[[]]:
        return
    if varList:
        onSet=generateONSet(varList)
        for onTerm in onSet:
            f=copyList(formula)    
            freeVars=findFreeVars(onTerm,varList)
            evaluate(f,onTerm,freeVars,prevAssignment+assignment)

def findFreeVars(term, varList):
    return [x for x in varList if x not in term and -x not in term]

def newAlgo(formula, unknowns):
    global start_time
    start_time = time.time() 
    OnSet=generateONSet(unknowns)
    
    for OnTerm in OnSet:
        f=copyList(formula)
        freeVars=findFreeVars(OnTerm, unknowns)
        assignments=[]
        evaluate(f,OnTerm,freeVars,assignments)
    

#This function prints SOP formula on console
def printSopFormula(formula): #input: List object
    sopString=''
    fLen=len(formula)
    termCount=0
    for term in formula:
        termCount+=1
        for literal in term:
            if(literal<0):
                suffix=str(-1*literal)+"'"
            else:
                suffix=str(literal)
            sopString+="X"+suffix
        if(termCount<fLen):
            sopString+=" + "
    print sopString
