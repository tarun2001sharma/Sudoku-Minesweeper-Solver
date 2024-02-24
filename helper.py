# This function takes a list of strings representing clauses
# and converts each string into a list of individual literals.
def makeClauses(clause_list):
    ans = []
    for i in clause_list:
        ans.append(list(i.split()))
    return ans

# This function creates a standardized representation of each sudoku cell's value
def convertReadability(row, col, num, neg = 0):
    # 'neg' flag is used to indicate if the literal should be negated (used for creating CNF clauses)
    if not neg:
        return 'n'+str(num)+'_r'+str(row)+'_c'+str(col)
    else:
        return '!n'+str(num)+'_r'+str(row)+'_c'+str(col)

# This function parses the initial sudoku puzzle provided as a list of strings
# and converts it into a dictionary with (row, column) tuples as keys and cell values as values.
def parser(inputs):
    sudoku_dict = {}
    for i in inputs:
        sudoku_dict[(int(i[0]), int(i[1]))] = int(i[3])   
    return sudoku_dict

# This function creates the CNF clauses based on the Sudoku board constraints.
# The below constraints are used to create the CNF clauses
# 1) At least one digit in a box:
# 2)  Unique row:
# 3) Unique column:
# 4) Unique 3x3:
# 5) Initial board:

def sudokuConstraints(board_dict):
    CNFclauses = []
    for key, value in board_dict.items():
        CNFclauses.append([convertReadability(key[0], key[1], value, neg=0)])
    # For each given value in the sudoku board, add a clause that enforces that value
    # Create clauses to enforce that each cell contains a unique value
    for r in range(1, 10):
        for c in range(1, 10):
            for n in range(1, 10):
                for next_n in range(n + 1, 10):
                    CNFclauses.append([convertReadability(r,c,n,neg=1), convertReadability(r,c,next_n,neg=1)])
                for next_c in range(c + 1, 10):
                    CNFclauses.append([convertReadability(r,c,n,neg=1), convertReadability(r,next_c,n,neg=1)])
                for next_r in range(r + 1, 10):
                    CNFclauses.append([convertReadability(r,c,n,neg=1), convertReadability(next_r,c,n,neg=1)])

                # Define the min_row and min_col for the 3x3 subgrid that the cell belongs to
                if r/3 <= 1:
                    min_r = 1
                else:
                    if r/3 <= 2:
                        min_r = 4
                    else:
                        min_r = 7

                if c/3 <= 1:
                    min_c = 1
                else:
                    if c/3 <= 2:
                        min_c = 4
                    else:
                        min_c = 7
                # Ensure 'n' is unique in its 3x3 subgrid
                for i in range(min_r, min_r + 3):
                    for j in range(min_c, min_c + 3):
                        if i != r and j != c:
                            CNFclauses.append([convertReadability(r,c,n,neg=1), convertReadability(i,j,n,neg=1)])
            # Ensure each cell contains at least one number 'i' from 1 to 9
            temp = []
            for i in range(1, 10):
                temp.append(convertReadability(r,c,i,neg=0))
            CNFclauses.append(temp)
    return CNFclauses

# This function converts the solution from the DPLL algorithm (dictionary form)
# back into a 9x9 sudoku grid format for easy readability.
def convertBack(answers):
    if not answers:
        print("No valid DPLL Assignments for the abpve set of clauses")
        print("Sudoku cannot be solved")
    sudoku = []
    for i in range(9):
        sudoku.append([-1]*9)
    for key, value in answers.items():
        if value:
            num = int(key[1])
            row = int(key[4])-1
            col = int(key[-1])-1
            sudoku[row][col] = num
    return sudoku

# This function prints the sudoku solution in a human-readable format.
def printSudoku(solution):
    print("Solved Sudoku:")
    for i in solution:
        for j in i:
            print(j, end=" ")
        print()

    

    
