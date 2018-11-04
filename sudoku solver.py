#%%
import numpy as np #load numpy

#%% Enter a sudoku
given = np.array([[5,0,8,7,0,0,1,0,0],
                  [0,1,0,9,0,5,0,0,0],
                  [0,0,0,0,0,0,0,3,0],
                  [4,0,0,2,0,0,0,9,0],
                  [0,2,1,0,0,0,5,4,0],
                  [0,3,0,0,0,4,0,0,8],
                  [0,7,0,0,0,0,0,0,0],
                  [0,0,0,6,0,9,0,1,0],
                  [0,0,4,0,0,2,6,0,9]])

#%% Basic functions
def flatten(someList):
    '''Flattens a list with elements that are lists (i.e. removes one level of []).
    Takes: list with list elements
    Returns: list
    Call: flatten(list)'''
    newList = []
    for i in someList:
        newList.extend(i)
    return newList

def getBox(square):
    '''Calculates the top left square in the box input belongs to.
    Takes: coordinates of a square (i,j)
    Returns: coordinates of top left box coordinates (a,b)
    Syntax: getBox(square[ = (i,j)])'''
    a = 3*int(square[0]/3)
    b = 3*int(square[1]/3)
    return (a,b)

def legal(sudoku, strict = True):
    '''Checks if a given sudoku is legal (i.e. no duplicate numbers in row,
    column, or box). If strict = False, will not check for completion,
    only for duplicates. If strict = True, will check both completion and
    duplicates.
    Takes: 9 by 9 array (unknowns marked with '0')
    Returns: Boolean
    Syntax: legal(sudoku, strict = True)'''
    if strict and 0 in sudoku:
        return False
    for square in [(i,j) for i in range(9) for j in range(9)]:
        m,n = square
        a,b = getBox(square)
        value = sudoku[m,n]
        if value in range(1,10):
            if sudoku[m,:].tolist().count(value) != 1: return False
            if sudoku[:,n].tolist().count(value) != 1: return False
            if flatten(sudoku[a:a+3,b:b+3].tolist()).count(value) != 1:
                return False
    return True
            
def get_peers(square):
    '''Gets coordinates of squares in the same row, column, or box as input.
    Takes: coordinates of a square (i,j)
    Returns: list of coordinates of squares in same row, column, or box
    Syntax: get_peers(square)'''
    m = square[0]
    n = square[1]
    peersList = []
    a,b = getBox((m,n))
    peersList.extend([(m,i) for i in range(9)])
    peersList.extend([(i,n) for i in range(9)])
    peersList.extend([(i,j) for i in range(a,a+3) for j in range(b,b+3)])
    peersList = list(set(peersList))
    return peersList

#%%
def makeDict(counts):
    '''Makes a dictionary of value frequencies given a list.
    Takes: list
    Returns: dict with list elements as keys and frequency as values
    Syntax: makeDict(list)'''
    countDict = {}
    for i in counts:
        countDict[i] = countDict.get(i,0) + 1
    return countDict

def listPossible(sudoku):
    '''Lists possible values for every box in input sudoku.
    Takes: 9 by 9 array
    Returns: possible values for every square as a list of lists
    Syntax: listPossible(sudoku)'''
    index = [(i,j) for i in range(9) for j in range(9)]
    sol = [[[] for i in range(9)] for i in range(9)]
    complete = set(range(1,10))
    for i in index:
        m = i[0]
        n = i[1]
        if sudoku[m,n] != 0:
            continue
        not_possible = set()
        not_possible = not_possible.union(set(sudoku[:,n]))
        not_possible = not_possible.union(set(sudoku[m,:]))
        box = getBox(i)
        not_possible = not_possible.union(set(flatten(sudoku[box[0]:box[0]+3,
                              box[1]:box[1]+3].tolist())))
        possible = list(complete-not_possible)
        sol[m][n].extend(possible)
    return sol

def fill_byRow(sudoku):
    '''Fills in values by row. Looks at missing values in each row, and if
    a missing value is possible in only one square, assigns that value to
    that square.
    Takes: 9 by 9 array
    Returns: 9 by 9 array
    Syntax: fill_byRow(sudoku)'''
    sol = listPossible(sudoku)
    original = np.zeros((9,9))
    while not (original == sudoku).all():
        original = sudoku.copy()
        for m in range(9):
            row = sol[m]
            missing = set(flatten(row))
            counts = makeDict(flatten(row))
            for i in missing:
                if counts[i] == 1:
                    for n in range(9):
                        if i in row[n]:
                            sudoku[m,n] = i
                            for peer in get_peers((m,n)):
                                a,b = peer
                                sol[a][b] = list(set(sol[a][b]) - set([i]))
                                sol[m][n] = []
    return sudoku

def fill_byCol(sudoku):
    '''Fills in values by column. Looks at missing values in each column,
    and if a missing value is possible in only one square, assigns that
    value to that square.
    Takes: 9 by 9 array
    Returns: 9 by 9 array
    Syntax: fill_byCol(sudoku)'''
    sol = listPossible(sudoku)
    original = np.zeros((9,9))
    while not (original == sudoku).all():
        original = sudoku.copy()
        for n in range(9):
            col = [sol[m][n] for m in range(9)]
            missing = set(flatten(col))
            counts = makeDict(flatten(col))
            for i in missing:
                if counts[i] == 1:
                    for m in range(9):
                        if i in col[m]:
                            sudoku[m,n] = i
                            for peer in get_peers((m,n)):
                                a,b = peer
                                sol[a][b] = list(set(sol[a][b]) - set([i]))
                                sol[m][n] = []
    return sudoku

def fill_byBox(sudoku):
    '''Fills in values by box. Looks at missing values in each box, and if
    a missing value is possible in only one square, assigns that value to
    that square.
    Takes: 9 by 9 array
    Returns: 9 by 9 array
    Syntax: fill_byBox(sudoku)'''
    sol = listPossible(sudoku)
    original = np.zeros((9,9))
    while not (original == sudoku).all():
        original = sudoku.copy()
        for sq in [(i,j) for i in [0,3,6] for j in [0,3,6]]:
            box = [sol[i][j] for i in range(sq[0],sq[0]+3) for j in range(sq[1],sq[1]+3)]
            missing = set(flatten(box))
            counts = makeDict(flatten(box))
            for i in missing:
                if counts[i] == 1:
                    for m in range(sq[0],sq[0]+3):
                        for n in range(sq[1],sq[1]+3):
                            if i in sol[m][n]:
                                sudoku[m,n] = i
                                for peer in get_peers((m,n)):
                                    a,b = peer
                                    sol[a][b] = list(set(sol[a][b]) - set([i]))
                                    sol[m][n] = []
    return sudoku

def fill_byOne(sudoku):
    '''Fills in values by ones. Checks list of possible values for all squares.
    If a square has only one possible value, assigns that value to that square.
    Takes: 9 by 9 array
    Returns: 9 by 9 array
    Syntax: fill_byRow(sudoku)'''
    sol = listPossible(sudoku)
    original = np.zeros((9,9))
    while not (original == sudoku).all():
        original = sudoku.copy()
        for m in range(9):
            for n in range(9):
                if len(sol[m][n]) == 1:
                    sudoku[m,n] = sol[m][n][0]
                    value = sol[m][n][0]
                    for peer in get_peers((m,n)):
                        a,b = peer
                        sol[a][b] = list(set(sol[a][b])-set([value]))
                        sol[m][n] = []
    return sudoku
            

def fill(given):
    '''Applies fill_byRow, fill_byCol, fill_byOne, and fill_byBox until such
    methods produce no more changes to the sudoku.
    Takes: 9 by 9 array
    Returns: 9 by 9 array
    Syntax: fill(sudoku)'''
    sudoku = given.copy()
    original = np.zeros((9,9))
    while not (original == sudoku).all():
        original = sudoku.copy()
        sudoku = fill_byOne(sudoku)
        sudoku = fill_byRow(sudoku)
        sudoku = fill_byCol(sudoku)
        sudoku = fill_byBox(sudoku)
    return sudoku

def guess(sudoku, prefill = True):
    '''Solves a sudoku by guessing possible values and checking whether solution
    is legal. If multiple answers, returns first answer it happens upon.
    Takes: 9 by 9 array
    Returns: 9 by 9 array
    Syntax: guess(sudoku)'''
    start = sudoku.copy()
    if not legal(start, strict = False):
        return False
    if legal(start, strict = True):
        return start
    if prefill:
        start = fill(start)
    sol = listPossible(start)
    for sq in [(i,j) for i in range(9) for j in range(9)]:
        if len(sol[sq[0]][sq[1]]) > 1:
            m,n = sq
            break
    try:
        values = sol[m][n]
    except:
        return False
    for vals in values:
        guess1 = start.copy()
        guess1[m,n] = vals
        guess1 = fill(guess1)
        if legal(guess1, strict = False):
            if legal(guess1, strict = True):
                return guess1
            else:
                guess1 = guess(guess1)
                if guess1 is not False:
                    return guess1
                else: continue
    return False

def solve(sudoku, prefill = True, solList = []):
    '''Returns a list of all possible solutions for a sudoku. Guesses values and
    checks solutions for legality.
    Takes: 9 by 9 array
    Returns: 9 by 9 array
    Syntax: solve(sudoku)'''
    start = sudoku.copy()
    if not legal(start, strict = False):
        return False
    if legal(start, strict = True):
        return start
    if prefill:
        start = fill(start)
    sol = listPossible(start)
    for sq in [(i,j) for i in range(9) for j in range(9)]:
        if len(sol[sq[0]][sq[1]]) > 1:
            m,n = sq
            break
    try:
        values = sol[m][n]
    except:
        return []
    for vals in values:
        guess1 = start.copy()
        guess1[m,n] = vals
        guess1 = fill(guess1)
        if legal(guess1, strict = False):
            if legal(guess1, strict = True):
                solList.append(guess1)
                print('appended')
                continue
            else:
                guess1 = solve(guess1, solList)
                if len(guess1) > len(solList):
                    solList = guess1
                    print('extended')
                    continue
    return solList

#%%
solution = solve(given, False)
print(solution)









