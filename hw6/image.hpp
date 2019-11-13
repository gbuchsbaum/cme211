#ifndef IMAGE_HPP
#define IMAGE_HPP

// Include necessary headers
#include <boost/multi_array.hpp>
#include <string>

class image {
  /* Class to represent an image. It stores the image as a boost array of
   * unsigned character values. It also stores the name of the original file.
   */
  boost::multi_array<unsigned char, 2> img;
  std::string fileName;
public:
  // Constructor
  image(std::string fileName_);
  // Function to save image data in given location.
  void Save(std::string fileName_);
  // Function to run convolution with given output and kernel.
  void Convolution(boost::multi_array<unsigned char,2>& input,
		   boost::multi_array<unsigned char,2>& output,
		   boost::multi_array<float,2>& kernel);
  // Function to blur the image with a given box size.
  void BoxBlur(unsigned int kSize);
  // Function to calculate the image sharpnes.
  unsigned int Sharpness(void);
};

#endif /* IMAGE_HPP */
