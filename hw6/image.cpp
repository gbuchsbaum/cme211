// Include required headers
#include <algorithm>
#include <boost/multi_array.hpp>
#include <cmath>
#include <sstream>
#include <stdexcept>
#include <string>

#include "hw6.hpp"
#include "image.hpp"

image::image(std::string fileName_) {
  /* Constructor. Records file name and reads the file. */
  this->fileName = fileName_;
  ReadGrayscaleJPEG(fileName, img);
}

void image::Save(std::string fileName_) {
  /* If file name is given, write to given location. If not, write to the
   * original file location. 
   */
  if (fileName_.size() == 0) {
    WriteGrayscaleJPEG(fileName, img);
  }
  else {
    WriteGrayscaleJPEG(fileName_, img);
  }
}

void image::Convolution(boost::multi_array<unsigned char,2>& input,
			boost::multi_array<unsigned char,2>& output,
			boost::multi_array<float,2>& kernel) {
  /* Performs convolution on image stored in input, using given kernel.
   * Results are stored in output.
   */

  /* Identify array dimensions */
  const long unsigned int* kShape = kernel.shape();
  const long unsigned int* iShape = input.shape();
  const long unsigned int* oShape = output.shape();
  const int kSize = (int)kShape[0];
  const int nRows = (int)iShape[0];
  const int nCols = (int)iShape[1];

  /* Check validity of inputs. If any errors are found, they are progressively
   * added to the error message, so that all errors are reported and can be
   * fixed at once rather than requiring multiple program runs.
   */
  std::stringstream s;
  if ((iShape[0] != oShape[0]) || (iShape[1] != oShape[1])) {
    s << __func__ << ": Input and output arrays are not the same shape\n";
  }
  if (kShape[0] != kShape[1]) {
    s << __func__ << ": Kernel is not square\n";
  }
  if (kSize % 2 != 1) {
    s << __func__ << ": Kernel is not odd size\n";
  }
  if (kSize < 3) {
    s << __func__ << ": Kernel is not at least size 3\n";
  }
  // Throw an error if any error messages have been added.
  std::string err = s.str();
  if (err.size() != 0) {
    throw std::runtime_error(err);
  }

  // Find the offset betweeen the center and edge of the kernel.
  const int kOffset = (kSize - 1) / 2;

  /* Create an extra boost array that extends the borders by the offset amount
   * so that calculations on pixels close to the edge become simpler. This
   * reduces the time required to constantly check pixel indices and adjust
   * them to within bounds when performing the actual convolution. All extended
   * values are simply the value of the closest given pixel.
   */
  const int rowsB = nRows + kSize - 1;
  const int colsB = nCols + kSize - 1;
  boost::multi_array<unsigned char,2> bordered(boost::extents[rowsB][colsB]);
  for (int i = 0; i < nRows + kSize - 1; i++) {
    /* Identify equivalent location in the original array, clamped to the
     * array bounds.
     */
    int x = std::max(0, std::min(i - kOffset, nRows - 1));
    for (int j = 0; j < nCols + kSize - 1; j++) {
      int y = std::max(0, std::min(j - kOffset, nCols - 1));
      // Copy value from equivalent position in input array.
      bordered[i][j] = input[x][y];
    }
  }

  /* Perform actual convolution. This involves looping through each pixel in
   * the image array. For each pixel, loop through the kernel, finding the
   * product of the kernel value and the the value pixel in the equivalent
   * offset from the center of the kernel, then add all of these products.
   * This uses the previous array with borders added to enable calculations
   * for pixels near the edge and to make the index for each calculation
   * just the sum of the base pixel index and the kernel index.
   */
  for (int i = 0; i < nRows; i++) {
    for (int j = 0; j < nCols; j++) {
      double sum = 0;
      for (int k = 0; k < kSize; k++) {
	// Row index remains constant while looping through columns.
	int x = i+k;
	for (int l = 0; l < kSize; l++) {
	  double product = (double)bordered[x][j+l] * kernel[k][l];
	  sum = sum + product;
	}
      }
      // Round down to integer and clamp result to limits of [0, 255].
      int result = std::min(std::max((int)std::floor(sum),0),255);
      // Convert to character and place in output array.
      output[i][j] = (unsigned char)result;
    }
  }
}

void image::BoxBlur(const unsigned int kSize) {
  /* Function to plur image using a given blur size. It identifies the image
   * dimensions and creates a new output array with the same dimensions. It 
   * then generates a kernel for the blur that has dimensions kSize x kSize,
   * with the value at each location equal to 1/(number of elements in kernel)
   * so that all kernel elements add to zero. It then runs Convolution with
   * img, the new output array, and the self-generated kernel. Finally, the
   * output array is copied into img.
   */
  const long unsigned int* iShape = img.shape();
  const long unsigned int nRows = iShape[0];
  const long unsigned int nCols = iShape[1];
  boost::multi_array<unsigned char,2> output(boost::extents[nRows][nCols]);
  const float kValue = 1 / ((float)(kSize * kSize));
  boost::multi_array<float,2> kernel(boost::extents[kSize][kSize]);
  for (unsigned int i = 0; i < kSize; i++) {
    for (unsigned int j = 0; j < kSize; j++) {
      kernel[i][j] = kValue;
    }
  }
  Convolution(img, output, kernel);
  img = output;
}

unsigned int image::Sharpness(void) {
  /* Function to determine the sharpness of the image. It first determines the
   * image dimensions and creates a new boost array with the same dimensions
   * to hold the results. It then creates a kernel to approximate the
   * Laplacian operator and runs Convolution with this kernel. Finally, it
   * finds the maximum value of the resulting array, converts it to an integer,
   * and returns the result.
   */
  const long unsigned int* iShape = img.shape();
  const long unsigned int nRows = iShape[0];
  const long unsigned int nCols = iShape[1];
  boost::multi_array<unsigned char,2> output(boost::extents[nRows][nCols]);
  
  boost::multi_array<float,2> kernel(boost::extents[3][3]);
  kernel[0][0] = 0;
  kernel[0][1] = 1;
  kernel[0][2] = 0;
  kernel[1][0] = 1;
  kernel[1][1] = -4;
  kernel[1][2] = 1;
  kernel[2][0] = 0;
  kernel[2][1] = 1;
  kernel[2][2] = 0;
  Convolution(img, output, kernel);
  
  auto begin = output.origin();
  auto end = begin + output.num_elements();
  unsigned char maxVal = *std::max_element(begin, end);
  return (unsigned int)maxVal;
}
