#include <vector>

/* Function to multiply a CSR-formatted sparse matrix by a vector */
std::vector<double> CSRMultiply(const std::vector<double> &val,
				const std::vector<int>    &row_ptr,
				const std::vector<int>    &col_idx,
				const std::vector<double> &vec);

/* Function to multiply a vector by the transpose of another vector */
double vecMultiply(const std::vector<double> &vec1,
		   const std::vector<double> &vec2);

/* Function to multiply a vector by a scalar */
std::vector<double> scalarMultiply(const std::vector<double> &vec,
				   const double x);

/* Function to subtract a vector from another vector */
std::vector<double> subtract(const std::vector<double> &vec1,
			     const std::vector<double> &vec2);

/* Function to add a vector to another vector */
std::vector<double> add(const std::vector<double> &vec1,
			const std::vector<double> &vec2);

/* Function to determine the L2 norm of a vector */
double L2norm(const std::vector<double> &vec);

/* Functions to print vectors to console */
void printVec(const std::vector<double> &vec);
void printVec(const std::vector<int> &vec);
