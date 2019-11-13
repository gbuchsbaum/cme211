#ifndef SPARSE_HPP
#define SPARSE_HPP

#include <vector>

class SparseMatrix
{
private:
  std::vector<int> i_idx;
  std::vector<int> j_idx;
  std::vector<double> a;
  int ncols;
  int nrows;

  bool isCSR; // Used to ensure that functions operate correctly


public:
  /* Method to modify sparse matrix dimensions */
  void Resize(int nrows, int ncols);
  
  /* Method to add entry to matrix in COO format */
  void AddEntry(int i, int j, double val);
  
  /* Method to convert COO matrix to CSR format using provided function */
  void ConvertToCSR();
  
  /* Method to perform sparse matrix vector multiplication using CSR formatted matrix */
  std::vector<double> MulVec(const std::vector<double> &vec);
  
  /* Constructor used to set the initial value of isCSR to false */
  SparseMatrix();

  /* Method to print the matrix in a readable format */
  void Print();
    
};

#endif /* SPARSE_HPP */
