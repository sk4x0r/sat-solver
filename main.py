import gbl
import re
import sys

if len(sys.argv)!=2:
	print "Invalid number of arguments"
	sys.exit(0)

dimacsfile=sys.argv[1].strip()
f = open(dimacsfile, 'r')
data=f.read()
lines=data.split('\n')
commentLine = re.compile('c.*') #Regular expression to detect comment lines
statLine = re.compile('p\s*cnf\s*(\d*)\s*(\d*)') #Regular expression to detect stat line

formula=[]
for line in lines:
    line=line.strip()
    if line=="%" or not line:
        continue
    if not commentLine.match(line):
        stats=statLine.match(line)
        if stats:
            varCount=int(stats.group(1)) #number of unknowns
            termCount=int(stats.group(2)) #number of clauses/terms
        else:
            numbers=line.rstrip('\n').split()
            literals=[]
            for number in numbers:
                n=int(number)
                if(n!=0):
                    literals.append(-n)
            formula.append(literals)

unknowns=[x for x in range(1, varCount+1)] #create list of unknowns
satisfiable=gbl.newAlgo(formula, unknowns)
if not satisfiable:
	print "UNSATISFIABLE"
