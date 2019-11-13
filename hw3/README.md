This directory contains Gabriel Buchsbaum's work on Homework 3 for CME 211

## Code design

`Airfoil` is a class that holds numerous variables representing various information related to analyzing an airfoil. It can take in a file with coordinates representing the shape of an airfoil, and other files listing the nondimensional pressure coefficient (*C<sub>p</sub>*) at each point on the airfoil, and use them to calculate the lift coefficient and stagnation point of the airfoil for each attack angle.

The following attributes are used in the `Airfoil` class:
* `inputdir`: The directory containing the data for a particular airfoil
* `xyPath`: The path name to find the xy data
* `nacaId`: The name of the particulary airfoil type (e.g. NACA 0012)
* `x`: A list of the x-coordinates
* `y`: A list of the y-coordinates
* `lenData`: The number of line segments used to represent the airfoil
* `cpPaths`: A list of the path names to find the (*C<sub>p</sub>*) data files
* `cpAlpha`: A dictionary storing the (*C<sub>p</sub>*) data, broken up by attack angle alpha
* `angles`: A sorted list of all all attack angles with valid data included in the directory
* `chord`: The chord length of the airfoil (distance from leading to trailing edge)
* `cl`: A dictionary with the lift coefficent for each attack angle
* `stags`: A dictionary storing the stagnation point for each attack angle

The following methods are used in the `Airfoil` class:
* `__init__(self,inputdir)`: The constructor, which is used by main.py to create a new `Airfoil` object from the given directory
* `read_xy(self)`: Reads the x and y data
* `read_cp(self,pathName)`: Reads the *C<sub>p</sub>* data at a given path name
* `dcx(self,alpha,i)`: Determines the x-component of the non-dimensional pressure force at a given attack angle and location on the airfoil
* `dcy(self,alpha,i)`: Determines the y-component of the non-dimensional pressure force at a given attack angle and location on the airfoil
* `lift_coeff(self,alpha)`: Calculates the lift coefficient at a given attack angle
* `calc_cls(self)`: Calculates the lift coefficient at every attack angle
* `stagnation(self,alpha)`: Determines the stagnation point at a given attack angle
* `calc_stags(self)`: Determines the stagnation point at every attack angle
* `__repr__(self)`: Converts the `Airfoil` object to a string when being printed

`Airfoil` is called by the main.py file, which passes the name of the directory the data is stored in as an argument for the `__init__` method.  Assuming all the data is available in the proper format, the `Airfoil` object is constructed using the following process:
1. Read the input directory and ensure it exists.
2. Identify and read the xy data (using `read_xy`).
3. Identify and read all files giving the pressure coefficients at each point of the airfoil at a given attack angle (using `read_cp`). This includes identifying the angle being used from the name of the file.
4. Calculate the chord length.
5. Calculate the lift coefficients (using `calc_cls`). This calls `lift_coeff` for each angle. `lift_coeff` calls `dcx` and `dcy` for each line segment in the airfoil.
6. Find the stagnation points (using `calc_stags`). This calls `stagnation` for each attack angle.

This design demonstrates abstraction because the outward-facing information only includes what the user actually needs. An `Airfoil` object is given a directory to extract data from, and performs all necessary data processing and calculations internally. It then gives the user the required information (airfoil type, lift coefficients, and stagnation points) when being printed. It demonstrates encapsulation by keeping all intermediate attributes like chord length internal, and making attributes private so that they cannot be manipulated by other users. The approached used of having the `__init__` method call each other method and store the results as each attribute means that `calc_cls` and `calc_stags` can be used to obtain the respective results without affecting the `Airfoil` object's attributes. This demonstrates decomposition by breaking each part of the object creation into a separate method.

## Error handling

This initially checks to make sure that the given directory, xy data, and cp data exists.  If any of these is missing, an error is raised. While reading the xy file, it uses try/catch statements to watch for non-numerical data or points that only have one value (rather than a pair of coordinates), recording the line in the file where this occurs and continuing to the next line. Once the entire file has been read, if errors were found, or if there are no valid data points, a RuntimeError is raised, giving the lines that the errors are found in. All of these errors will stop the program.
It then reads through each file containing *C<sub>p</sub>* data, using a try/catch statement to identify lines with non-numerical data. If any data is flawed, a message is printed listing the flawed data, and the program moves on to the next file. Assuming all of the data is formatted correctly, it then checks to see if there is no data, or if the length of the file does not line up with the length of the xy data. Additionally, this all occurs in a try/catch statement that can pick up if the program is unable to determine an angle from the file name. If any of these errors occur, the relevant error message is printed. However, since it is still able to perform calculations using the data at other attack angles, **errors in reading the *C<sub>p</sub>* files do not stop the program; they make it skip recording the flawed data and continue with all valid *C<sub>p</sub>* data**. After reading each file, the program makes one final check to ensure that there is some valid *C<sub>p</sub>* data; if not, an error is raised and the program is stopped.