from copy import deepcopy
from collections import deque

def Forwardchecking(variable, domain, assignment, constraints):
# Forward checking only checks arc-consistency for arcs that terminate on the new assignment.
    if(len(assignment) == len(variable)):
        return assignment
    for x in variable:
        if x not in assignment:
            break
    
    newDomain = deepcopy(domain)

    colFind(constraints, newDomain, x, assignment)
    
    for val in newDomain[x]:
        
        if isValid(assignment, constraints, x, val):
            assignment[x] = val
        
            if domainWipeOutCheck(constraints, newDomain, x + 1, assignment):
                assignment.pop(x)
            else:
                if (Forwardchecking(variable, newDomain, assignment, constraints)):
                    return assignment
                assignment.pop(x)
    return False

def Backtracking(variable, domain, assignment, constraints):
# Return assignment after backtracking (solution) otherwise failure
    if(len(assignment) == len(variable)):
        return assignment
    for x in variable:
        if x not in assignment:
            break
    for val in domain[x]:
        if isValid(assignment, constraints, x, val):
            assignment[x] = val
            if(Backtracking(variable, domain, assignment, constraints)):
                return assignment
            assignment.pop(x)
    return False


def domainWipeOutCheck(constraints, domains, xi, assignment):
# Checks for domain wipe out (size of the domain becomes zero). After new vairable assigned, return True if domain domain wipe out, false otherwise.
    testDomains = deepcopy(domains)
    if xi >= len(assignment):
        return False
    for assignX in assignment:
        
        if assignment[assignX] in testDomains[xi]:
            testDomains[xi].remove(assignment[assignX])
        if assignment[assignX] + assignX - xi in testDomains[xi]:
            testDomains[xi].remove(assignment[assignX] + assignX - xi)
        if assignment[assignX] - assignX + xi in testDomains[xi]:
            testDomains[xi].remove(assignment[assignX] - assignX + xi)
    if len(testDomains) == 0:
        return True
    return False


def colFind(constraints, domains, xi, assignment):
# Looking ahead at every node to eliminate obvious failure values from the domain of the next unassigned variable.
    for assignX in assignment:

        if assignment[assignX] in domains[xi]:
            domains[xi].remove(assignment[assignX])
        if assignment[assignX] + assignX - xi in domains[xi]:
            domains[xi].remove(assignment[assignX] + assignX - xi)
        if assignment[assignX] - assignX + xi in domains[xi]:
            domains[xi].remove(assignment[assignX] - assignX + xi)

         

def isValid(assignment, constraints, cell, val):
#Check queen placement doesn't cause conflict
    assign = deepcopy(assignment)
    assign[cell] = val

    for A in assign:
      for B in assign:
        a = assign[A]
        b = assign[B]
        if A != B and (a == b or A + a == B + b or A - a == B - b):
          return False
    return True


def AC_3(constraints, variable, domain, neighbours):
# Check if the CSP is arc consistance or not

    queue = deque(constraints)

    while(queue):
        pair = queue.popleft()
        xi = pair[0]
        xj = pair[1]

        # return true if revise the domain of xi
        if Revise(constraints, variable, domain, xi, xj):
          # If the size of domain 0 == 0 return false
          if len(domain[pair[0]]) == 0: 
             return False
          for xk in neighbours[pair[0]]:
            if xk == xj:
              continue
            queue.append([xk, xi])
    return True
    


def Revise(constraints, variables, domains, xi, xj):
# Return true if revise the domain xi
  revised = False
  for valX in domains[xi]:
    flag = False
    for valY in domains[xj]: 
      if isValid({xi:valX}, constraints, xj, valY):
        flag = True
        break
    # if there is no valY in domains[xi] allows (valX, ValY) to satisfy the constraints between xi and xj then delete valX from domains[xi]
    if not flag: 
      domains[xi].remove(valX)
      revised = True
      
  return revised


def Display(variable, n, assignment):
# Display the solution as a board representation otherwise print no solution
    if(assignment):
      print("Var -> Val")
      for x in variable:
        print("%d   ->   %d"%(x,assignment[x]))
      print("\n\nBoard:\n")
      for i in range(0, n):
        for j in range(0, n):
          if(assignment[i] != j):
            print("-", end=" ")
          else:
            print("q", end=" ")
        print("")
      print("\n\n")
    else:
      print("No Solution")


def Assign(n, domains, variables, neighbours, constraints):
# Assing n values for the lists and dictionaries
  for i in range(0, n):
    variables.append(i)

  for x in variables:
    domains[x] = []
    for i in range(0, n):
      domains[x].append(i)

  for x in variables:
    neighbours[x] = []

  for i in range(0, n):
    for j in range(0, n):
      if i == j:
        continue
      neighbours[i].append(j)
         
  for xi in neighbours:
    for xj in neighbours[xi]:
      constraints.append([xi, xj])
    
##-------------------------------------------------------------------------------------------------------------------------
## 
def arc_Consistency_AC3_analysis(N):

    variables = []
    domains = {}
    neighbours = {}
    constraints = []
    Assign(N, domains, variables, neighbours, constraints)

    consistance = AC_3(constraints, variables, domains, neighbours)


def AC3_with_backtracking_analysis(N):
    variables = []
    domains = {}
    neighbours = {}
    constraints = []
    assignment = {}
    
    Assign(N, domains, variables, neighbours, constraints)
   
    Backtracking(variables, domains, assignment, constraints)

    
    
def forward_checking_analysis(N):
   
    variables = []
    domains = {}
    neighbours = {}
    constraints = []
    assignment = {}
    
    Assign(N, domains, variables, neighbours, constraints)
    Forwardchecking(variables, domains, assignment, constraints)