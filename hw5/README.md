This repository contains Gabriel Buchsbaum's work for Homework 5.

# Problem description

The goal of this homework is to write a program that can solve a maze defined by a file listing the locations of the walls in the maze. This uses the right-hand algorithm (i.e. following the right-hand wall, taking every possible right turn or turning in the rightmost direction possible until the exit of the maze is reached). The results are written to a file as the location of every step along the path.

# C++ code description

The first thing the code does is read the command line inputs. It then creates a static array of booleans to represent the maze that is large enough to hold the largest maze given. It is initialized by setting the value at each index to false (representing an open space). Next, the maze file is opened. The first line, giving the maze dimensions, is read and checked to ensure that it fits in the given static array. Then each following row is read and interpreted as a set of integer coordinates. If the coordinates are within the given bounds, the value at that location in the static array is set to true (representing a wall).

After the maze has been set up, the starting position is found by searching the top row of the maze until the opening is identified. The solution file is opened, and the initial position is written to the file. For each subsequent move, the correct direction is identified, then the position at the end of the move is written to the file. To avoid a long string of conditionals, directions are represented by an integer that can be converted to instructions on how to move. The correct direction is identified by steadily turning to the left and testing if the location in that direction is open, starting with the location to the right of the current direction of travel. This process is continued until the last row of the matrix is reached.

# Solution verification description

First, the command line inputs are read, and the maze file is loaded into a numpy array. The dimensions of the maze are identified, and a numpy array of that size with values of zero is created to represent the maze. For each pair of coordinates in the maze file, the value of the array representing the maze at that location is set to one (representing walls). Then, the solution file is loaded into a numpy array.

First, the beginning of the solution is checked to ensure that it is at the top of the maze and in an open location (i.e. the value of the matrix array at that location is zero). Then, each move is checked for validity. This involves making sure that the move is exactly one unit in one direction, and that the new location is not in a wall. Once the end of the solution is reached, it is checked to confirm that it is the last row of the maze. At each point, if the solution is found to have a flaw, a message declaring it invalid is printed and the program exits. The solution is only valid if the program reaches the end without finding any flaws.