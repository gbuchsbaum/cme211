This repository contains Gabriel Buchsbaum's work on Homework 6 for CME 211.

# Image class description

## Image attributes

* `boost::multi_array<unsigned char, 2> img`: An array storing the image data
* `std::string fileName`: A string storing the original file name (used so the save method has a default name to use)

## Image methods

* `image(std::string fileName_)`  
 The image constructor, which stores the file name and runs `ReadGrayscaleJPEG()` from `hw6.cpp` to store the image data in `img`
* `void Save(std::string fileName_)`  
 Function to save the image data to a file. It runs `WriteGrayscaleJPEG()` from `hw6.cpp` using the given `fileName`, or using the `filename` attribute if no file name is given.
* `void Convolution(boost::multi_array<unsigned char,2>& input,  
                 boost::multi_array<unsigned char,2>& output,  
		 boost::multi_array<float,2>& kernel)`  
 Function to run a convolution on the image data stored n `input` and store the results in `output`, using the given `kernel` to specify what convolution to do.
* `void BoxBlur(unsigned int kSize)`  
 Function to blur the image with the given blur box size `kSize`. It generates a kernel to produce the desired blur, and runs `Convolution()` with that kernel.
* `unsigned int Sharpness(void)`  
 Function to calculate the sharpness of the image. It creates a kernel approximating the discrete Laplacian operator, runs `Convolution()`, and returns the maximum character value.

# Key implementation details

`main()` uses a loop to go through each desired blur size, creating a new image object in each iteration.  Since the object is created inside the loop, it is deleted after each iteration. The output and file names are automatically generated.

To save computation time, `Convolution()` creates an array that extends the borders of the image.  This allows the subsequent calculations to just look up the pixel value corresponding to the base pixel and the offset from the kernel center, rather than needing to check whether this location is outside of bounds and possibly clamp it to the nearest edge value for every single kernel location for every single pixel.  To identify the value that a certain location in the kernel should be multiplied by, the indices of the kernel location and the base pixel for that iteration are added, and that location in the secondary array is used.

For each pixel, the products of kernel and corresponding pixel values are added, then rounded to an integer and clamped into the range of [0, 255], then converted to `char` and placed in the output array.

`BoxBlur()` generates its own kernel by squaring the given size to find the number of kernel elements, then dividing 1 by this number to find the value of each kernel element (so that they all add to 1). It then generates a boost array of the correct dimensions and fills it with the correct value.