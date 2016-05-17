#-*-coding:utf8;-*-
#qpy:2
#qpy:console

#Assuming numpy installed on device
from numpy import *
passed = 0
#Funcionality below:

grid = zeros((9,9), dtype=int32)
#completed = zeros((9,9), dtype=int32)
possible = ones((9,9,10), dtype=int32)

#Prints visual state of grid
def printGrid():

    print "\nCurrent Grid:"
    for i in range(9):
    
        if i % 3 == 0:
            print "|-----------------------|"
            
        for j in range(9):
            
            if j % 3 == 0:
                print '|',
                
            if grid[i][j]:
                print grid[i][j],
            else:
                print " ",
                
        print '|'
        
    print "|-----------------------|\n"   
     
    return 
    
#___________________________________
#Resets the grid for future use
def flush():

    for i in range(9):
        for j in range(9):
            #completed[i][j] = 0
            
            for k in range(10):
                possible[i][j][k] = 1

    return 

#____________________________________
#Makes sure candidate solution is valid
def verify(coords):

    newRow, newCol, new = coords

    boxRow = newRow/3
    boxCol = newCol/3

    """if add(possible[newRow,:,new]) == 0:
        return -1
    elif add(possible[:,newCol,new]) == 0:
        return -1"""
    
    #check if candidate number is valid in grid
    for r in range(9):
        
        #same row
        if grid[r][newCol] == new:
            return -1
        
        #same column
        if grid[newRow][r] == new:
            return -1
            
        #same box
        if grid[3*boxRow + r/3][3*boxCol + r%3] == new:
            return -1
    
    #print coords
    grid[newRow][newCol] = new
    #printGrid()
    #raw_input()
    
    #check if grid is complete 
    for r in range(81):
        if grid[r/9][r%9] == 0:
            return 0
    
    return 81

#___________________________________
#Recursive algorithm to determine solution
def recurse():

    for i in range(9):
        for j in range(9):
            for k in range(1,10):
                if grid[i][j] == 0 and possible[i,j,k] > 0:
                    verification = verify((i,j,k))
                    if verification == 81:
                        return 81
                    elif verification == 0:   
                    	    status = recurse()
                    	    if status == 81:
                    	        return 81
                    	    else:
                    	        grid[i][j] = 0
            if grid[i][j] == 0:
                return
#___________________________________
#Based on correct entry, eliminate possibilities for affected neighbouring cells
def eliminate(coords):
    
    newRow, newCol, new = coords
    
    #update data structures
    grid[newRow][newCol] = new
    possible[newRow][newCol][:] = 0
    
    #eliminate possibilities
    boxRow = newRow/3
    boxCol = newCol/3
    
    for r in range(9):
        
        #same row
        possible[r][newCol][new] = 0
        
        #same column
        possible[newRow][r][new] = 0
    
        #same box
        possible[3*boxRow + r/3][3*boxCol + r%3][new] = 0
        
    return

#____________________________________
#Main algorithm to find next valid number
def search():
    global passed

    #v1
    #Simple elimination (last option standing wins)
    incomplete = 0
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                incomplete = 1
                amount = add.reduce(possible[i][j][1:10])
                
                if amount == 0:
                    print "No options at", i, j, "!!!",possible[i,j]
                    return (-2,-2)
                elif amount == 1:
                    for k in range(1,10):
                        if possible[i][j][k] == 1:
                            print "1"
                            return (i,j,k)
                    
            elif grid[i][j] > 0 and possible[i][j][0] == 1:	
                return (i,j,grid[i][j])
    
                
    if incomplete == 0: #all cells are full
        return (81,81)

    #prints state after simple test    
    if passed == 0:
        passed = 1
        printGrid()
       
    #print "Passed simple"
    
    
    changed = 0
    
    #v2
    #sweep elimination (only place for number to go in row/col/box)
    for n in range(1,10):
        
        #rows
        for i in range(9):
            locale = argwhere(possible[i,:,n] > 0)
            if len(locale) > 0:
                if len(locale) == 1:
                    print "22"
                    return (i,locale[0][0],n)
                    
                #v4 - the only candidates in a row/col share the same box
                elif min(locale[:,0])/3 == max(locale[:,0])/3:
                    cbcol = locale[0,0]/3
                    replace = argwhere(possible[3*(i/3):3*(i/3)+3,3*cbcol:3*cbcol+3,n] > 0)
                    if len(locale) != len(replace):
                        for p in replace:
                            possible[3*(i/3)+p[0],3*cbcol+p[1],n] = 0
                        for l in locale:
                            possible[i,l[0],n] = 1
                        print "R444"
                        
        #cols
        for j in range(9):
            locale = argwhere(possible[:,j,n] > 0)
            if len(locale) > 0:
                if len(locale) == 1:
                    print "22"
                    return (locale[0][0],j,n)
                    
                #v4 - the only candidates in a row/col share the same box
                elif min(locale[:,0])/3 == max(locale[:,0])/3:
                    cbrow = locale[0,0]/3
                    replace = argwhere(possible[3*cbrow:3*cbrow+3,3*(j/3):3*(j/3)+3,n] > 0)
                    if len(locale) != len(replace):
                        for p in replace:
                            possible[3*cbrow+p[0],3*(j/3)+p[1],n] = 0
                        for l in locale:
                            possible[l[0],j,n] = 1
                        print "C444"
        
        
        
        #boxs
        for r in range(9):
            locale = argwhere(possible[3*(r/3):3*(r/3)+3,3*(r%3):3*(r%3)+3,n] > 0)
            if len(locale) > 0:
                if len(locale) == 1:
                    print "22"
                    return (3*(r/3)+locale[0][0],3*(r%3)+locale[0][1],n)
                
                #v3- the only candidates in a box share the same row/col
                elif min(locale[:,0]) == max(locale[:,0]):
                    crow = 3*(r/3) + locale[0][0]
                    replace = argwhere(possible[crow,:,n] > 0)
                    if len(locale) != len(replace):
                        for p in replace:
                            possible[crow,p[0],n] = 0
                        
                        for l in locale:
                            possible[crow,3*(r%3)+l[1],n] = 1
                        print "R33"
                        changed = 1
                        
                elif min(locale[:,1]) == max(locale[:,1]):
                    ccol = 3*(r%3) + locale[0][1]
                    replace = argwhere(possible[:,ccol,n] > 0)
                    if len(locale) != len(replace):
                        for p in replace:
                            possible[p[0],ccol,n] = 0
                        
                        for l in locale:
                            possible[3*(r/3)+l[0],ccol,n] = 1  
                        print "C33"
                        changed = 1
    if changed == 1:
        return (-7,-7)
    else:
        return (-1,-1)#cannot use logical elimination only, signal recurse
    
#____________________________________
#Control function calling search slgorithm
def solveSimple():

    print "Solving simple sudoku..."

    while True:
    
        next = search()
    
        if next[0] == -1:
            print "No more moves!"
            printGrid()
            print "Recursively solving..."
            recurse()
            printGrid()
            break
        elif next[0] == -2:
            print "Error, please verify grid"
            printGrid()
            break
        elif next[0] == 81:
            print "Puzzle solved!"
            printGrid()
            break
        elif next[0] != -7:
            eliminate(next)

    return

#________________________________
#Generates new grid state based on user input
def newGrid():

    global grid
    
    flush()
    
    print "~~Please enter the sudoku grid, row by row."
    print "~~Use 0 for empty space\n"
    
    for i in range(9):
        rowInput = raw_input()
        
        if len(rowInput) != 9:
            print "Bad input, try again"
            return 1
            
        grid[i] = [int(c) for c in rowInput]


    printGrid()
        
    return 0

#______________________________________
#User interface to launch program
def launch():
    
    print "Welcome to Sudoku Solver!"
    
    prompt = 's'
    while prompt != 'q':
        
        prompt = raw_input("~~Press q to quit or s to solve!\n")
        if prompt == 's':
            
            while newGrid(): pass
            
            #raw_input("Enter any letter to start solving!")
            solveSimple()
    return
    
#_________________________________________
#
#    
#
#Script here:
print "This is console module"
print "\n\n"


#Sample puzzle solutions, with increasing difficulty.
#Each puzzle has a separate difficulty output, based on
#   how complicated the search algorithm was needed to find the next number

#v1 grid simple
"""grid = [[5,0,0,1,0,0,7,0,0],
            [0,2,0,0,0,7,1,0,0],
            [3,0,1,4,0,0,8,5,2],
            [6,1,0,5,7,2,4,0,8],
            [0,0,2,9,6,0,0,0,0],
            [0,4,0,0,3,0,6,2,7],
            [4,5,9,0,8,0,0,7,0],
            [1,3,0,0,0,0,9,8,6],
            [2,0,0,0,1,0,0,4,3]]"""       
  
  
        
#v2 grid

"""grid = [[7,9,0,0,0,0,3,0,0],
        [0,0,0,0,0,6,9,0,0],
        [8,0,0,0,3,0,0,7,6],
        [0,0,0,0,0,5,0,0,2],
        [0,0,5,4,1,8,7,0,0],
        [4,0,0,7,0,0,0,0,0],
        [6,1,0,0,9,0,0,0,8],
        [0,0,2,3,0,0,0,0,0],
        [0,0,9,0,0,0,0,5,4]]"""
        
        
        
#v3 grid (common row/col elimination)

"""grid = [[0,0,0,6,4,5,0,0,0],
        [7,0,9,0,0,0,5,0,4],
        [0,0,0,0,0,0,0,0,0],
        [0,2,0,5,0,3,0,7,0],
        [0,0,3,0,0,0,6,0,0],
        [0,1,0,9,0,7,0,3,0],
        [0,0,0,0,0,0,0,0,0],
        [4,0,6,0,0,0,3,0,2],
        [0,0,0,3,2,1,0,0,0]]"""



#Following grids need recurse

#kind of hard ish grid for future iterations
"""grid = [[0,0,9,0,0,0,0,4,0],
        [1,0,0,2,0,0,8,0,0],
        [0,2,0,0,1,3,0,0,7],
        [0,0,3,0,0,0,0,6,0],
        [0,0,4,0,0,0,5,0,0],
        [0,5,0,0,0,0,4,0,0],
        [6,0,0,9,5,0,0,2,0],
        [0,0,7,0,0,2,0,0,1],
        [0,1,0,0,0,0,6,0,0]]"""

#another hard grid

"""grid = [[0,7,8,0,9,0,4,0,0],
        [0,9,0,1,0,8,0,0,7],
        [0,0,0,7,0,0,0,2,0],
        [0,0,3,0,0,2,0,0,0],
        [0,0,1,0,8,0,7,0,0],
        [0,0,0,4,0,0,6,0,0],
        [0,1,0,0,0,4,0,0,0],
        [8,0,0,2,0,1,0,5,0],
        [0,0,2,0,6,0,0,1,0]]"""


#some hard grid
"""grid = [[6,0,1,0,0,2,0,7,0],
        [0,9,0,1,0,0,5,0,0],
        [0,0,0,0,0,6,0,0,4],
        [0,8,0,0,0,0,0,2,0],
        [0,0,6,0,0,0,7,0,0],
        [0,5,0,0,0,0,0,9,0],
        [4,0,0,5,0,0,0,0,0],
        [0,0,9,0,0,3,0,8,0],
        [0,3,0,6,0,0,1,0,7]]"""
            
launch()            
