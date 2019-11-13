#ifndef HEAT_HPP
#define HEAT_HPP

#include <string>
#include <vector>

#include "sparse.hpp"

class HeatEquation2D
{
private:
  SparseMatrix A;
  std::vector<double> b, x, Tx; // Tx is x-dependent cold boundary temperature

  std::string soln_prefix;
  int nx, ny; // number of unknown points in x and y directions
  double Th; // Hot boundary temperature
  
  public:
  /* Method to setup Ax=b system */
  int Setup(std::string inputfile);
  
  /* Method to solve system using CGsolver */
  int Solve(std::string soln_prefix_);
  
  /* Method to save intermediate solution to a text file */
  void SaveSolution(const std::vector<double> &sol, const int niter);
  
};

#endif /* HEAT_HPP */
