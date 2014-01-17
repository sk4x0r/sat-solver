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

def findUnassignedVars(term, varList):
	return [x for x in varList if x not in term and -x not in term]
'''
def newAlgo(formula, unknowns):
	global start_time
	start_time = time.time() 
	OnSet=generateONSet(unknowns)
	
	for OnTerm in OnSet:
		f=copyList(formula)
		unassignedVars=findUnassignedVars(OnTerm, unknowns)
		assignments=[]
		evaluate(f,OnTerm,unassignedVars,assignments)
'''

def evaluateQuotient(formula, assignment):
	
	fIter=copyList(formula)
	for literal in assignment:
		for term in fIter:
			if literal in term:
				idx=formula.index(term)
				formula[idx].remove(literal)
	
			if (-1)*literal in term:
				formula.remove(term)
		fIter=copyList(formula)
	return formula


def checkUnsatisfiable(f):
	for t in f:
		if len(t)==0:
			return True
	return False


def trimFormula(f):
	formula=[]
	for t in f:
		if len(t)!=0:
			formula.append(t)
	return formula

FLAG=0
q=Queue.Queue()
def checkSolution(formula, assignments):
	if len(evaluateQuotient(formula, assignments))==0:
		return True
	return False
	
def newAlgo(orig_formula, unknowns):
	global start_time
	start_time = time.time() 
	#print "formula=", printSopFormula(formula)
	#print formula
	formula=copyList(orig_formula)
	assignments=[]
	t=formula,assignments, unknowns
	#print"Inserting t", t
	q.put(t)
	while not q.empty():
		t=q.get()
		#print "tuple=",t
		formula=t[0]
		assignments=t[1]
		unknowns=t[2]
		onSet=generateONSet(unknowns)
		for onTerm in onSet:
			#print "formula=",formula
			#print "assignments",assignments
			#print "onTerm=", onTerm
			#print "unknowns",unknowns 
			f=evaluateQuotient(copyList(formula), onTerm)
			#print "f=", f
			if len(f)==0:
				print checkSolution(copyList(orig_formula), assignments + onTerm) 
				FLAG=1
				print "Solution:",assignments+onTerm
				print time.time() - start_time, "seconds"
				#sys.exit(0)
			elif checkUnsatisfiable(f):
				#print "Not satisfiable, continuing.."
				continue
			else:
				#print "inserting into queue"
				new_assignments=assignments+onTerm
				new_unknowns=findUnassignedVars(onTerm, unknowns)
				f=trimFormula(f)
				t=f,new_assignments,new_unknowns
				#print t
				q.put(t)
	return FLAG



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
