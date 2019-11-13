/* This program can solve a maze using the right-hand wall following algorithm.
 * It takes a file representing the walls of a maze and a location to save the
 * solution as command line inputs, and produces a file representing a path
 * that can be used to navigate the maze. The basic process is as follows:
 * read the maze file and construct a representation of the maze, then identify
 * the opening in the top row, then solve the maze by following the right-hand
 * wall until the exit is reached, while saving each location along the path
 * to the solution file.
 */

// Import useful libraries
#include <fstream>
#include <iostream>
#include <string>


int main(int argc, char* argv[]) {  
  // Check the number of arguments, and print a usage message if inadequate
  if (argc < 3) {
    std::cout << "Usage:" << std::endl;
    std::cout << " " << argv[0] << " <maze file> <solution file>" << std::endl;
    return 0;
  }

  // Store inputs as variables
  std::string mazeFile = argv[1];
  std::string solFile = argv[2];

  /* The maze is represented as a 2D static boolean array, with true 
   * representing walls and false representing open spaces. The array has
   * dimensions of 201x201, or large enough to handle the largest maze given,
   * but can be adjusted by change the value of size. The maze is initialized
   * by initializing every value of the array as false using a double for-loop.
   */
  const int size = 201;
  bool maze[size][size];
  for (int i = 0; i < size; i++) {
    for (int j = 0; j < size; j++) {
      maze[i][j] = false;
    }
  }

  /* After the maze has been ititialized, the maze file is opened. The first
   * line is read, giving the maze dimensions. If these are larger than the
   * size of the static array, then an error message is printed and the
   * program is terminated.
   */
  int nRow; // In this larger scope to allow for use when solving maze.
  int nCol;
  std::ifstream f0;
  f0.open(mazeFile);
  if (f0.is_open()) {
    f0 >> nRow >> nCol;
    if (nRow > size or nCol > size) {
      std::cout << "Maze is too large for static array" << std::endl;
      return 0;
    }
    
    /* Assuming everything is proper, each line is read and split into a row
     * and a column. If an issue with the file results in out-of-bounds
     * coordinates, an error message is printed and the program is terminated.
     * Otherwise, the location in the array marked by the coordinates is
     * switched to true to mark a wall.
     */
    int row;
    int col;
    while (f0 >> row >> col) {
      if (row >= nRow or col >= nCol) {
	std::cout << "Coordinates exceed given maze size" << std::endl;
	return 0;
      }
      maze[row][col] = true;
    }
    f0.close();
  }
  else { // Print an error message if the maze file does not open.
    std::cout << "Failed to open " << mazeFile << std::endl;
    return 0;
  }

  // Find the start of the path by looping through each column until the
  // point that is in the top row of that column is open.
  int start = -1;
  for (int i = 0; i < nCol; i++) {
    if (not maze[0][i]) {
      start = i;
      break;
    }
  }
  // If the starting position cannot be identified, print a message and exit.
  if (start == -1) {
    std::cout << "Unable to find maze entrance" << std::endl;
    return 0;
  }

  /* The direction is represented as an integer from 0 to 3, with 0 
   * representing south, 1 representing east, 2 representing north, and 3
   * representing west. A 4x2 static integer array is used to store how
   * moving in each direction actually changes the coordinates.
   * The current location is stored in an integer array of length 2.
   * The initial direction is 0 (south), and the initial location is the
   * the opening that was just found.
   */
  int dirs[4][2] = {{1,0},{0,1},{-1,0},{0,-1}};
  int dir = 0;
  int loc[2] = {0, start};

  int test; // Temporary storage of the direction that is being checked.
  // Open file to record solution.
  std::ofstream f1;
  f1.open(solFile);
  if (f1.is_open()) {
    // Write initial position.
    f1 << loc[0] << " " << loc[1] << std::endl;
    /* All subsequent positions are found as follows: Start by testing a right
     * turn from the current direction, and then turn left until an opening is
     * found. In each direction being tested, check whether the location that
     * would be moved to has a wall in it. If so, increment the direction
     * number (or loop around) and try again; if not, exit the loop and move
     * in that direction. Moves are made by adjusting the location coordinates
     * according to the correct direction. This process is repeated with the
     * new locations until the last row of the maze is reached (i.e. the exit
     * is found).
     */
    while (loc[0] < (nRow - 1)) {
      test = (dir + 3) % 4;
      for (int i = 0; i < 4; i++) {
	if (maze[loc[0] + dirs[test][0]][loc[1] + dirs[test][1]]) {
	  test = (test + 1) % 4;
	}
	else {
	  dir = test;
	  break;
	}
      }
      
      loc[0] = loc[0] + dirs[dir][0];
      loc[1] = loc[1] + dirs[dir][1];
      // Write new location to the solution file.
      f1 << loc[0] << " " << loc[1] << std::endl;
    }
    f1.close();
  }
  else { // If the file cannot be opened, print a warning message and exit.
    std::cout << "Failed to open " << solFile  << std::endl;
    return 0;
  }

  // If the program runs to completion, exit with a return value of zero
  return 0;
}

