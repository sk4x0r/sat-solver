import gbl
import re
    
dimacsfile="input3.cnf" #CNF file containing formula to be checked for consistency in DIMACS format
f = open(dimacsfile, 'r')
data=f.read()
lines=data.split('\n')
commentLine = re.compile('c.*') #Regular expression to detect comment lines
statLine = re.compile('p\s*cnf\s*(\d*)\s*(\d*)') #Regular expression to detect stat line

formula=[]
for line in lines:
    line=line.strip()
    if line=="%":
        break
    if not commentLine.match(line):
        stats=statLine.match(line)
        if stats:
            varCount=int(stats.group(1)) #number of unknowns
            termCount=int(stats.group(2)) #number of clauses/terms
        else:
            numbers=line.rstrip('\n').split(' ')
            literals=[]
            for number in numbers:
                n=int(number)
                if(n!=0):
                    literals.append(-n)
            formula.append(literals)
gbl.printSopFormula(formula)

unknowns=[x for x in range(1, varCount+1)] #create list of unknowns
gbl.newAlgo(formula, unknowns)
print "Unsatisfiable"