
# import useful modules
import numpy as np
import sys

def makeMaze(mazeWalls):
    """
    This method takes a numpy array representing the coordinates of the
    walls in a maze, and outputs a numpy array representing the maze.
    The maze array is the size indicated by the top line of the maze file,
    and with values of zero representing empty spaces and values of one
    representing walls.
    """
    mazeSize = (mazeWalls[0,0], mazeWalls[0,1])
    maze = np.zeros(mazeSize, dtype = np.int32)
    for i in range(1,mazeWalls.shape[0]):
        maze[mazeWalls[i,0],mazeWalls[i,1]] = 1
    return maze

def validMove(maze, loc0, loc1):
    """
    This method is used to check whether the a given move is valid.
    It takes in a maze array, as well as the move start and end points
    (represented by numpy arrays of length 2). It first checks to make
    sure that the total distance traveled is one unit in one direction,
    then makes sure that the the new location is not in a wall.
    """
    dist = abs(loc1[0] - loc0[0]) + abs(loc1[1] - loc0[1])
    if dist != 1:
        return False
    if maze[loc1[0],loc1[1]] == 1:
        return False
    return True

# If the program is not given maze and solution files, print a usage message.
if len(sys.argv) < 3:
    print("Usage:")
    print("  python3 checksoln.py <maze file> <solution file>")
    sys.exit(0)

# Store inputs as variables.
mazeFile = sys.argv[1]
solFile = sys.argv[2]

# Read the maze file, and convert it into a maze array.
mazeWalls = np.loadtxt(mazeFile, dtype = np.int32)
maze = makeMaze(mazeWalls)

# Read the solution file, storing it as a numpy array.
solution = np.loadtxt(solFile, dtype = np.int32)
lenSol = solution.shape[0]

# First confirm that the solution begins in the top row.
if solution[0,0] != 0:
    print("Solution is not valid")
    sys.exit(0)
try:
    # Check whether the initial position is open (i.e. entrance correct)
    if maze[solution[0,0],solution[0,1]] == 1:
        print("Solution is not valid")
        sys.exit(0)
    # Loop through each move, checking to confirm that is is valid. If there
    # is a problem at any point, the solution is invalid.
    for i in range(lenSol - 1):
        if validMove(maze, solution[i,:], solution[i+1,:]):
            continue
        else:
            print("Solution is not valid")
            print(i)
            sys.exit(0)
except IndexError:
    # Catch if solution includes location outside of maze.
    print("Solution is not valid")
    sys.exit(0)
# Check whether the final location in the solution is in the last row of the
# maze (i.e. at the exit).
if solution[lenSol - 1,0] != maze.shape[0] - 1:
    print("Solution is not valid")
    sys.exit(0)

# If none of these checks found errors in the solution, print that it is valid.
print("Solution is valid!")
