import re
import Queue
import copy
import sys
import time
#TODO: represent terms/formulae using sets instead of lists


#Recursively copies the content of list and returns copied list
def copyList(l):
	return copy.deepcopy(l)


#Generates set of orthonormal terms, given a list of variables
#This method returns list of `n+1` ON terms for `n` unknowns
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


def findUnassignedVars(term, varList):
	return [x for x in varList if x not in term and -x not in term]


def evaluateQuotient(formula, assignment):
	#print "evaluateQuotient"
	#print "formula before", formula
	#print "assignment", assignment
	fIter=copyList(formula)
	for literal in assignment:
		for term in fIter:
			if literal in term:
				idx=formula.index(term)
				formula[idx].remove(literal)
	
			if (-1)*literal in term:
				formula.remove(term)
		fIter=copyList(formula)
	#print "new formula", formula
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

def checkSolution(formula, assignments):
	if len(evaluateQuotient(formula, assignments))==0:
		return True
	return False

q=Queue.Queue()


def applyUnitPropogation(formula, assignments, unknowns):
	fIter=copyList(formula)
	alreadyRemoved=[]
	for term in fIter:
		if len(term)==1:
			if abs(term[0]) in alreadyRemoved:
				continue
			alreadyRemoved.append(abs(term[0]))
			assignments+=term
			unknowns.remove(abs(term[0]))
			formula=evaluateQuotient(formula, [-1*term[0]])
	return formula, assignments, unknowns

def applyPureLiteral(formula, assignments, unknowns):
	for literal in unknowns:
		literalExists=False
		complementExists=False
		for term in formula:
			if literal in term:
				literalExists=True
				if complementExists:
					break
			if -1*literal in term:
				complementExists=True
				if literalExists:
					break
		if literalExists and not complementExists:
			#print "UnitLiteral"
			formula=evaluateQuotient(formula, [-1*literal])
			assignments.append(-1*literal)
			unknowns.remove(literal)
			
		if not literalExists and complementExists:
			#print "UnitComplement"
			formula=evaluateQuotient(formula, [literal])
			assignments.append(literal)
			unknowns.remove(literal)
	return formula, assignments, unknowns

def newAlgo(orig_formula, unknowns):
	global start_time
	FLAG=0
	start_time = time.time()
	formula=copyList(orig_formula)
	assignments=[]
	t=formula,assignments, unknowns
	q.put(t)
	while not q.empty():
		t=q.get()
		formula=t[0]
		assignments=t[1]
		unknowns=t[2]
				
		formula, assignments, unknowns = applyUnitPropogation(formula, assignments, unknowns)
		if checkUnsatisfiable(formula):
			continue
		#TODO:apply pure literal elimination
		formula, assignments, unknowns = applyPureLiteral(formula, assignments, unknowns)
		
		if len(formula)==0:
			#print checkSolution(copyList(orig_formula), assignments + onTerm) 
			FLAG=1
			print "Solution:",assignments
			print time.time() - start_time, "seconds"
			continue
			#sys.exit(0)
		onSet=generateONSet(unknowns)
		
		for onTerm in onSet:
			f=evaluateQuotient(copyList(formula), onTerm)
			if len(f)==0:
				#print checkSolution(copyList(orig_formula), assignments + onTerm) 
				FLAG=1
				print "Solution:",assignments+onTerm
				print time.time() - start_time, "seconds"
				#sys.exit(0)
			elif checkUnsatisfiable(f):
				continue
			else:
				new_assignments=assignments+onTerm
				new_unknowns=findUnassignedVars(onTerm, unknowns)
				f=trimFormula(f)
				t=f,new_assignments,new_unknowns
				q.put(t)
	return FLAG
