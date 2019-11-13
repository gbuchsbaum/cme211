// Include required headers
#include <exception>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

#include "image.hpp"

int main() {
  /* Main function. It loads the original image and determines its sharpness.
   * It then goes through each required kernel size and loads the image
   * as a new object, then blurs with the specified kernel size, prints the
   * sharpness of the blurred image, and saves the blurred image.
   */
  try {
    image original("stanford.jpg");
    std::cout << "Original image: ";
    std::cout << std::setw(3) << original.Sharpness() << std::endl;
    int kSizes[7] = {3, 7, 11, 15, 19, 23, 27};
    // Loop through each required kernel size.
    for (unsigned int i = 0; i < 7; i++) {
      image blur("stanford.jpg");
      blur.BoxBlur(kSizes[i]);
      // Print sharpness with desired format.
      std::cout << "BoxBlur(" << std::setw(2) << kSizes[i] << "): ";
      std::cout << std::setw(6) << blur.Sharpness() <<std::endl;
      // Generate file name and save blurred image.
      std::stringstream s;
      s.fill('0');
      s << "BoxBlur" << std::setw(2) << kSizes[i] << ".jpg";
      blur.Save(s.str());
      }
  }
  catch (std::exception& e) {
    // If errors are generated, print them.
    std::cerr << e.what() << std::endl;
  }
  return 0;
}
