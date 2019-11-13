// Import necessary modules
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <vector>

#include "sparse.hpp"
#include "COO2CSR.hpp"
#include "matvecops.hpp"

SparseMatrix::SparseMatrix() {
  /* Constructor sets isCSR to false, does nothing else. */
  this->isCSR = false;
}

void SparseMatrix::Resize(int nrows, int ncols) {
  /* Resize only changes the nrows and ncols variables, since there is no
   * reason to enter unnecessary data.
   */
  this->nrows = nrows;
  this->ncols = ncols;
}

void SparseMatrix::AddEntry(int i, int j, double val) {
  /* Function to add data to the matrix. It simply takes in the i and j
   * indices, as well as the value, and appends them to the appropriate
   * vectors. If the indices are outside the stored dimensions, the dimensions
   * are increased.
   */
  // Make sure the matrix is in COO format for data entry.
  if (isCSR) {
    std::stringstream s;
    s << __func__ << ": Matrix is CSR, must be COO format for data entry";
    throw std::runtime_error(s.str());
  }

  i_idx.push_back(i);
  j_idx.push_back(j);
  a.push_back(val);

  if (i >= nrows) {
    nrows = i+1;
  }
  if (j >= ncols) {
    ncols = j+1;
  }
}

void SparseMatrix::ConvertToCSR() {
  /* Function to convert to CSR. It first checks to make sure the matrix is
   * in COO before converting, then uses the provided COO2CSR function.
   */
  if (not isCSR) {
    COO2CSR(a, i_idx, j_idx);
    isCSR = true;
  }
}

std::vector<double> SparseMatrix::MulVec(const std::vector<double> &vec) {
  /* Function to multiply the matrix by a vector. It first makes sure the
   * matrix is in CSR format, then uses the multiplication function in
   * matvecops.
   */
  if (not isCSR) {
    ConvertToCSR();
  }
  // Ensure dimensions are correct
  int vecLength = (int)vec.size();
  if (ncols != vecLength) {
    std::stringstream s;
    s << __func__ << ": Number of matrix columns and vector entries unequal";
    throw std::runtime_error(s.str());
  }
  return CSRMultiply(a, i_idx, j_idx, vec);
}

void SparseMatrix::Print() {
  /* Function to print the matrix contents to console. Used for debugging. */
  if (isCSR) {
    std::cout << "CSR format" << std::endl;
    std::cout << "Row pointers:" << std::endl;
  }
  else {
    std::cout << "COO format" << std::endl;
    std::cout << "Row indices:" << std::endl;
  }
  printVec(i_idx);
  std::cout << "Column indices:" << std::endl;
  printVec(j_idx);
  std::cout << "Values:" << std::endl;
  printVec(a);
}
