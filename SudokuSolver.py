#Backtracking Algorithm

import sys

def CreateDataStructures(boxanswers, rowanswers, columnanswers,allanswers, board):
    """Creates containers for all answers in each box/row/column, a container for looking up the box number, and
        a list of all of the empty spaces that need to be filled."""
    increment = len(board) ** .5
    leftendrownumber = 0
    leftcolumnnumber = 0
    boxnumberreference = {}
    allpossible = []
    #Create all answers structures first as well as box reference
    for boxnumber in range(0, len(board)):
        boxanswer = set()
        if boxnumber % increment == 0 and boxnumber != 0:
            leftendrownumber += 3
            leftcolumnnumber = 0
        for columnnumber in range(leftcolumnnumber, leftcolumnnumber + 3):
            for rownumber in range(leftendrownumber, leftendrownumber + 3):
                #For every row/column pair, mark what box it is to be used as a reference for later
                if rownumber not in boxnumberreference:
                    boxnumberreference[rownumber] = {}
                else:
                    boxnumberreference[rownumber][columnnumber] = boxnumber
                #For every row/col pair that has a columnnumber of 0, it will not be added to the dictionary since it's the beginning of the row
                #Only boxnumberreference[rownumber] = {} would be added. Thus, the below line is necessary.
                boxnumberreference[rownumber][columnnumber] = boxnumber
                #For a non-0 answer at a coordinate in the sudoku board, add to its respective column/row answer container
                #Also, add it to boxanswer which is added onto the boxanswers container at the bottom
                if board[rownumber][columnnumber] != 0:
                    boxanswer.add(board[rownumber][columnnumber])
                    if rownumber not in rowanswers:
                        rowanswers[rownumber] = set([board[rownumber][columnnumber]])
                    else:
                        rowanswers[rownumber].add(board[rownumber][columnnumber])
                    if columnnumber not in columnanswers:
                        columnanswers[columnnumber] = set([board[rownumber][columnnumber]])
                    else:
                        columnanswers[columnnumber].add(board[rownumber][columnnumber])
                #If it's an empty space (0), append it to our list of empty spaces
                else:
                    allpossible.append([rownumber,columnnumber])
        leftcolumnnumber += 3
        boxanswers[boxnumber] = boxanswer
    #If a box/row/column is empty, give it a value of an empty set
    for i in range(0, len(board)):
        if i not in boxanswers:
            boxanswers[i] = set()
        if i not in rowanswers:
            rowanswers[i] = set()
        if i not in columnanswers:
            columnanswers[i] = set()
    return [boxanswers, boxnumberreference, rowanswers, columnanswers,allpossible] 

def Finished(rowanswers):
    for rownumber,rowanswer in rowanswers.items():
        if len(rowanswer) != 9:
            return False
    return True

def SudokuSolver(grid):
    """Given a 9 by 9 Sudoku grid, solves it iteratively using backtracking."""
    allanswers = set([1,2,3,4,5,6,7,8,9])
    structures = CreateDataStructures({},{},{},allanswers,grid)
    boxanswers = structures[0]
    boxref = structures[1]
    rowanswers = structures[2]
    colanswers = structures[3]
    allpossible = structures[4]
    allpossible = sorted(allpossible)
    path = []
    index = 0
    #Keep looping until all values have been validated in each blank spot (0) and filled
    while Finished(rowanswers) == False:
        try:
            current = allpossible[index]
            row = current[0]
            col = current[1]
            valid = True
            ananswer = 0
            for i in range(1, 10):
                #Check box/row/column validity
                boxnumber = boxref[row][col]
                if i not in boxanswers[boxnumber] and i not in rowanswers[row] and i not in colanswers[col]:
                    boxanswers[boxnumber].add(i)
                    rowanswers[row].add(i)
                    colanswers[col].add(i)
                    index += 1
                    ananswer = i
                    grid[row][col] = i
                    path.append([current,ananswer])
                    break
            #Sudoku rules are broken since we were not able to place any valid number into the current coordinates, must backtrack
            if ananswer == 0:
                #Find a valid choice
                while True:
                    index -= 1
                    previous = path[-1]
                    path.remove(previous)
                    coordinates = previous[0]
                    grid[coordinates[0]][coordinates[1]] = 0
                    value = previous[1]
                    boxanswers[boxref[coordinates[0]][coordinates[1]]].remove(value)
                    rowanswers[coordinates[0]].remove(value)
                    colanswers[coordinates[1]].remove(value)
                    #Check if previous value is a 9, meaning the previous value placed (9) is also invalid
                    if value == 9:
                        continue
                    row = coordinates[0]
                    col = coordinates[1]
                    valid = False
                    for value in range(value + 1, 10):
                        #Check box/row/column validity
                        boxnumber = boxref[row][col]
                        #Valid answer has been found
                        if value not in boxanswers[boxnumber] and value not in rowanswers[row] and value not in colanswers[col]:
                            boxanswers[boxnumber].add(value)
                            rowanswers[row].add(value)
                            colanswers[col].add(value)
                            index += 1
                            ananswer = value
                            path.append([[row,col],ananswer])
                            valid = True
                            grid[row][col] = value
                            break 
                    if valid:
                        break
        except:
            return "This Sudoku board is not solvable."
    return grid

#Create board from text file
board = open(sys.argv[1],'r').readlines()
board = [line.strip("\n").split() for line in board]
for i in range(0, len(board)):
    line = board[i]
    for c in range(0, len(line)):
        line[c] = int(line[c])
        
print SudokuSolver(board)
