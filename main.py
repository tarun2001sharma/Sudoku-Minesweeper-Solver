import sys
from helper import *
from DPLL import *
# import propagate_iter2

if __name__ == "__main__":
    # Get the command line arguments in list, excluding the script name
    commandLst = sys.argv[1:]

    start = 0
    # verbose mode
    # Extract the Sudoku inputs from the command line arguments, skipping the '-v' flag
    if '-v' in commandLst:
        isVerbose = True
        start += 1   
    else:
        isVerbose = False
    
    # when guessing, we use the smallest lexicographic atom by default
    isLexico = True
    # mode to get DPLL assignments without lexicographically assigning the values
    if '-random' in commandLst:
        isLexico = False
        start += 1

    sudoku_inputs = commandLst[start:]

    # Parse the Sudoku inputs into a dictionary with keys as (row, col) and values as the 
    # number in that cell
    board = parser(sudoku_inputs)

    # Generate the CNF clauses based on the Sudoku board constraints
    clauses = sudokuConstraints(board)

    # Initialize an empty dictionary to store the final assignments of literals
    finalLiteralValue = {}
 
    # Solve the Sudoku using the DPLL algorithm and get the assignments of literals
    assignments = dpll(clauses, finalLiteralValue, isVerbose, isLexico)

    if not assignments:
        print("NO VALID ASSIGNMENT")

    # Convert the DPLL assignments back into a 9x9 Sudoku grid
    solution = convertBack(assignments)

    # Print the Sudoku solution in a readable format
    printSudoku(solution)

    
