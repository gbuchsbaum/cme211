// Include useful modules
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include "heat.hpp"
#include "matvecops.hpp"
#include "CGSolver.hpp"

int HeatEquation2D::Setup(std::string inputfile) {
  /* Function to take in the address of a file with setup information and
   * use the information to set up the heat equation matrix. It starts by
   * opening the file and storing the information.
   */
  double length, width, h, Tc;
  std::ifstream f;
  f.open(inputfile);
  if (f.is_open()) {
    f >> length >> width >> h >> Tc >> Th;
    f.close();
  }
  else {
    std::cerr << "Failed to open " << inputfile << std::endl;
    return 1;
  }

  /* Use the given dimensions and pixel size to determine the number of unknown
   * points in each direction. This includes the left edge, but excludes the
   * top and bottom edges (as they are known already) and the right edge (since
   * it is just a copy of the left edge). Next, the equation matrix is resized
   * to the right size and the constant and solution vectors are set up
   * (constant with default values of zero, solution with inital guesses of 1)
   */
  nx = (int)(length / h);
  ny = (int)(width / h) - 1;
  const int nPoints = nx * ny;
  A.Resize(nPoints, nPoints);
  b.resize(nPoints, 0.0);
  x.resize(nPoints, 1.0);
  const double h2 = h * h;

  /* Set up the equations. This involves moving through each unknown point
   * in the given area and placing coefficients in the correct row of matrix A
   * to form the equation given in the description. For locations adjacent to
   * top and bottom, the known temperature of the boundary at that column is
   * determined, and placed into the constant vector b. For locations
   * adjacent to the sides, the locations of the coefficients are looped around
   * to correspond to the equivalent indices. The sign of every entry is
   * flipped due to the system being negative definite.
   *
   * To allow the matrix solver to work, the unknown points must be converted
   * from a 2D array to a 1D vector. This is done by going row by row from the
   * bottom to the top, i.e. starting at the bottom left, moving to the bottom
   * right, then going up a row at a time until eventually ending with the
   * top right.
   */
  // Loop through hot boundary at top.
  for (int j = 0; j < nx; j++) {
    // If in the first column, loop around to the last unknown column.
    if (j == 0) {
      A.AddEntry(nx * (ny - 1) + j, nx * ny - 1, -1/h2);
    }
    // Otherwise, add an entry to the matrix representing the point to the left
    else {
      A.AddEntry(nx * (ny - 1) + j, nx * (ny - 1) + j - 1, -1/h2);
    }
    // If in the last unknown column, loop around to the first column.
    if (j == nx - 1) {
      A.AddEntry(nx * (ny - 1) + j, nx * (ny - 1), -1/h2);
    }
    // Otherwise, add an entry to the matrix for the point to the right
    else {
      A.AddEntry(nx * (ny - 1) + j, nx * (ny - 1) + j + 1, -1/h2);
    }
    // Add entry for adjacent row.
    A.AddEntry(nx * (ny - 1) + j, nx * (ny - 2) + j, -1/h2);
    // Add entry for current position.
    A.AddEntry(nx * (ny - 1) + j, nx * (ny - 1) + j, 4/h2);
    // Add Th to the vector b.
    b[nx * (ny - 1) + j] = Th/h2;
  }

  // Set up vector to store temperatures along cold boundary.
  Tx.resize(nx, 0);
  
  // Similarly, loop through the bottom row, against the cold boundary.
  for (int j = 0; j < nx; j++) {
    // If in the first column, loop around to the last unknown column.
    if (j == 0) {
      A.AddEntry(j, nx - 1, -1/h2);
    }
    // Otherwise, add an entry to the matrix representing the point to the left
    else {
      A.AddEntry(j, j - 1, -1/h2);
    }
    // If in the last unknown column, loop around to the first column.
    if (j == nx - 1) {
      A.AddEntry(j, 0, -1/h2);
    }
    // Otherwise, add an entry to the matrix for the point to the right
    else {
      A.AddEntry(j, j + 1, -1/h2);
    }
    // Add entry for adjacent row.
    A.AddEntry(j, nx + j, -1/h2);
    // Add entry for current position.
    A.AddEntry(j, j, 4/h2);
    // Determine cold boundary temperatures and add to the vector b.
    Tx[j] = -Tc*(exp(-10*std::pow((double)j*h-length/2,2))-2);
    b[j] = Tx[j]/h2;
  }

  // loop through remainder of rows
  for (int i = 1; i < ny - 1; i++) {
    for (int j = 0; j < nx; j++) {
      // If in the first column, loop around to the last unknown column.
      if (j == 0) {
	A.AddEntry(nx * i + j, nx * (i + 1) - 1, -1/h2);
      }
      // Otherwise, add an entry to the matrix for the point to the left
      else {
	A.AddEntry(nx * i + j, nx * i + j - 1, -1/h2);
      }
      // If in the last unknown column, loop around to the first column.
      if (j == nx - 1) {
	A.AddEntry(nx * i + j, nx * i, -1/h2);
      }
      // Otherwise, add an entry to the matrix for the point to the right
      else {
	A.AddEntry(nx * i + j, nx * i + j + 1, -1/h2);
      }
      // Add entry for row above.
      A.AddEntry(nx * i + j, nx * (i - 1) + j, -1/h2);
      // Add entry for row below.
      A.AddEntry(nx * i + j, nx * (i + 1) + j, -1/h2);
      // Add entry for current position.
      A.AddEntry(nx * i + j, nx * i + j, 4/h2);
    }
  }
  // Convert to CSR
  A.ConvertToCSR();
  return 0;
}

int HeatEquation2D::Solve(std::string soln_prefix_) {
  /* Function to solve the heat equations. It first records the given file
   * prefix, then rus the CG solver function on the system of equations.
   */
  this->soln_prefix = soln_prefix_;
  double tol = 1.e-5;
  try {
    int niter = CGSolver(A, b, x, tol, *this);
    std::cout << "SUCCESS: CG solver converged in ";
    std::cout << niter << " iterations."<<std::endl;
    SaveSolution(x, niter);
  }

  catch (std::exception& e) {
    std::cerr << e.what() << std::endl;
    return 1;
  }
  return 0;
}


void HeatEquation2D::SaveSolution(const std::vector<double> &sol,
				  const int niter) {
  /* Function to save the solution to a file. This function exists here rather
   * than as part of CGSolver due to the information that a HeatEquation2D
   * object has access to that would need to be passed as additional arguments
   * to CGSolver, such as the array dimensions, the solution file prefix, and
   * the boundary temperatures. It works by being passed as an argument to
   * CGSolver. It takes in a vector with the current status of the solution
   * and an integer with the current number of iterations, then generates the
   * file name, and writes each temperature value to the output file.
   * It adds the temperature to the top and bottom, adds in line breaks to
   * correspond to the actual dimensions, and adds in the last column by
   * repeating the first column.
   */
  std::stringstream fname;
  fname.fill('0');
  fname << soln_prefix << std::setw(3) << niter << ".txt";
  std::ofstream f;
  f.open(fname.str());
  if (f.is_open()) {
    // Write row of cold boundary at the top
    for (int j = 0; j < nx; j++) {
      f << Tx[j] << "  ";
    }
    f << Tx[0] << std::endl;
    // Write body of solution.
    for (int i = 0; i < ny; i++) {
      for (int j = 0; j < nx; j++) {
	f << sol[nx * i + j] << " ";
      }
      f << sol[nx * i] << std::endl;
    }
    // Write row of hot boundary at the top
    for (int j = 0; j < nx; j++) {
      f << Th << " ";
    }
    f << Th << std::endl;
    
    f.close();
  }
  else {
    std::cerr << "Unable to open " << fname.str() << std::endl;
  }
}
