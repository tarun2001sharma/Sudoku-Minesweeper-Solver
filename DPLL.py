from copy import deepcopy

from helper import *

# Function to check if a given literal is a negation
def isNegation(knownLiteral):
    if '!' == knownLiteral[0]:
        return True
    else:
        return False

# Function to get the inverse of a literal (negation if not negated, remove negation if negated)
def getInverse(knownLiteral):
    if isNegation(knownLiteral):
        return knownLiteral[1:]
    else:
        return '!'+knownLiteral

# Function to create a dictionary that counts occurrences of each literal and its negation
# Note that this functions generates literal name and stores the pure and negated count in value
def makeLiteralDictionary(clause_list):
    literalDict = {}
    for clause in clause_list:
        for literal in clause:
            if not isNegation(literal):
                if literal in literalDict:
                    literalDict[literal][0] += 1
                else:
                    literalDict[literal] = [1,0]
            else:
                if getInverse(literal) in literalDict:
                    literalDict[getInverse(literal)][1] += 1
                else:
                    literalDict[getInverse(literal)] = [0, 1]
    return literalDict

# Function to propagate a known literal's value through the clause list
def propagate(clause_list, knownLiteral):
    # Assume that the knownLiteral has True value
    n = len(clause_list)
    for i in range(len(clause_list)):
        if knownLiteral in clause_list[i]:
            # Replace clause with ['.'] if it contains the known literal
            # we will remove this list later
            clause_list[i] = ['.']
        elif getInverse(knownLiteral) in clause_list[i]:
            # Remove the inverse of the known literal from the clause
            clause_list[i].remove(getInverse(knownLiteral))
     # Filter out clauses that have been satisfied (replaced with ['.'])
    res = [ele for ele in clause_list if ele != ['.']]
    return res

# Function to handle unit clauses (clauses with a single literal)
def taskSingletons(clause_list, finalLiteralValue, univLiterals, verbose):
    singleClauses = set()
    for clause in clause_list:
        if len(clause)==1:
            singleClauses.add(clause[0])
    # get the list of singletons
    singleClauses = list(singleClauses)

    # Return if there are no unit clauses
    if len(singleClauses) == 0:
        return False, clause_list
 
    # Propagate the found unit clauses
    for unitClause in singleClauses:
        clause_list = propagate(clause_list, unitClause)
        if verbose:
            print("easy case: unit Singleton ", unitClause)
        if isNegation(unitClause):
            # Assign false to the literal's value if it is a negation
            if getInverse(unitClause) in univLiterals:
                univLiterals.remove(getInverse(unitClause))
                finalLiteralValue[getInverse(unitClause)] = False
        else:
            # Assign true to the literal's value
            if unitClause in univLiterals:
                univLiterals.remove(unitClause)
                finalLiteralValue[unitClause] = True
    return True, clause_list

# Recursive function to continuously process unit clauses until there are none left
def recurSingletons(clause_list, finalLiteralValue, univLiterals, verbose, ):
    isrecur, clause_list = taskSingletons(clause_list, finalLiteralValue, univLiterals, verbose)
    # base case: in case no more singltons found, terminate the recursion
    if not isrecur:
        return clause_list, finalLiteralValue
    else:
        return recurSingletons(clause_list, finalLiteralValue, univLiterals, verbose)

# Function to find pure literals (literals that occur only in non-negated or only
def findPureLiterals(clause_list):
    literalDict = makeLiteralDictionary(clause_list)
    pureLiterals = []
     # Check if a literal is pure by looking at the counts of its positive and negative occurrences
    for clause in clause_list:
        for literal in clause:
            if literal not in pureLiterals:
                if not isNegation(literal):
                    if literalDict[literal][1] == 0:
                        pureLiterals.append(literal)
                else:
                    if literalDict[getInverse(literal)][0] == 0:
                        pureLiterals.append(literal)
    return pureLiterals

# Function to handle pure literals (literals which occur in only one form throughout the set of clauses)
def taskPureLiterals(clause_list, finalLiteralValue, univLiterals, verbose):
    # get the pure literals list
    pureLiterals = findPureLiterals(clause_list)
    # if no pure literal found, return false
    if not pureLiterals:
        return False, clause_list
    # Propagate the found pure literals
    for i in pureLiterals:
        clause_list = propagate(clause_list, i)
        # remove the pure literals from tracked data strucures
        if not isNegation(i):
            univLiterals.remove(i)
            finalLiteralValue[i] = True
            if verbose:
                print("easy case: pure literal ", i, "= ", finalLiteralValue[i])
        else:
            univLiterals.remove(getInverse(i))
            finalLiteralValue[getInverse(i)] = False
            if verbose:
                print("easy case: pure literal ", i, "= ", finalLiteralValue[getInverse(i)])
    return True, clause_list

# Recursive function to continuously process pure literals until there are none left
def recurPureLiterals(clause_list, finalLiteralValue, univLiterals, verbose):
    isrecur, clause_list = taskPureLiterals(clause_list, finalLiteralValue, univLiterals, verbose)
    # base case: in case no more pure literals found, terminate the recursion
    if not isrecur:
        return clause_list, finalLiteralValue
    else:
        return recurPureLiterals(clause_list, finalLiteralValue, univLiterals, verbose)

# Recursive function that implements the DPLL algorithm
def recurDPLL(clause_list, univLiterals, valLiteral, verbose):
    """
    clause_list: list of all the clauses, Form -> [[]]
    univLiterals: list of all unique literals, Form -> []
    valLiteral: dictionary of literals storing T/F, Form -> {str: T/F}
    """
    # Process pure literals and singletons before making any guesses
    clause_list, valLiteral = recurPureLiterals(clause_list, valLiteral, univLiterals, verbose)
    clause_list, valLiteral = recurSingletons(clause_list, valLiteral, univLiterals, verbose)

    # If the clause list is empty, a satisfying assignment has been found
    if not clause_list:
        if verbose:
            # free literals are not printed.
            for key, value in valLiteral.items():
                print(key, '=', value)
        return valLiteral
    
    # Check for contradictions (empty clauses) after propagation
    for i in clause_list:
         # If there's an empty clause, the current assignment leads to a contradiction
        if not i:
            if verbose:
                print("Contradiction: guess is false. Backtracking...")
            return 0
    
    # Guessing step: pick the first unassigned literal for a guess
    guessLiteral = univLiterals[0]

    # Create deep copies for branching to maintain different states
    new_clause_list = deepcopy(clause_list)
    new_univLiterals = deepcopy(univLiterals)
    new_valLiteral = deepcopy(valLiteral)

    # Propagate the guess (assuming it's true) through the clause list
    new_clause_list = propagate(new_clause_list, guessLiteral)
    
    if verbose:
        print("hard case:", guessLiteral, '= True')

    # Assign the guessed literal to True in the value dictionary
    new_valLiteral[guessLiteral] = True
    # Remove the guessed literal from the list of unassigned literals
    new_univLiterals.pop(0)

    # Recursively call DPLL with the new state after the guess
    temp = recurDPLL(new_clause_list, new_univLiterals, new_valLiteral, verbose)
    # If the recursive call returns 0, the guess led to a contradiction
    if temp==0:
        # Create deep copies again for the opposite branch
        new_clause_list = deepcopy(clause_list)
        new_univLiterals = deepcopy(univLiterals)
        new_valLiteral = deepcopy(valLiteral)
        for i in new_clause_list:
            if not i:
                break

        # Propagate the inverse of the guess
        new_clause_list = propagate(new_clause_list, getInverse(guessLiteral))
        new_valLiteral[guessLiteral] = False
        if verbose:
            print("hard case:", guessLiteral, '= False')
        new_univLiterals.pop(0)

        # Recursively call DPLL for the other branch (where the guess is False)
        return recurDPLL(new_clause_list, new_univLiterals, new_valLiteral, verbose)
    
    else:
        # If the recursive call didn't return 0, a solution has been found
        return temp

# Main function to run the DPLL algorithm
def dpll(clause_list, valLiteral, verbose, isLexico):
    # clause_list = makeClauses(rawClauses)
    univLiteralsDict = makeLiteralDictionary(clause_list)
    # Get a sorted list of unique literals for branching to maintain lexicographical order
    univLiterals = list(univLiteralsDict.keys())
    if isLexico:
        univLiterals = sorted(univLiterals)
    # Start the recursive DPLL process
    return recurDPLL(clause_list, univLiterals, valLiteral, verbose)




