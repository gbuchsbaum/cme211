"""
This module contains all relevant structures and methods for an airfoil
object.
"""

# Import useful modules
import glob
import math
import os

# Define an Airfoil class
class Airfoil:
    """
    Airfoil: a class used to create an airfoil object.
    
    This class takes in a directory containing data on the shape of an
    airfoil and the resulting pressure coefficients at a range of attack
    angles. It processes this data and uses it to determine the lift
    coefficient and stagnation point at each attack angle.

    Attributes:
    -----------
    inputdir : str
        the name of the input directory, ending with a slash
    xyPath : str
        the path name to find the xy data
    nacaId : str
        the name of the particular airfoil type
    x : list
        the x-coordinates, in order
    y : list
        the y-coordinates, in order
    lenData : int
        the number of line segments representing the airfoil
    cpPaths : list
        the path names to find the cp data files
    cpAlpha : dict
        the cp data, broken up by angles. Each value is a list.
    angles : list
        the angles of the provided data, sorted
    chord : float
        the chord length
    cl : dict
        the lift coefficient at each angle. Values are floats.
    stags : dict
        the stagnation point at each angle. Values are tuples.

    Methods:
    --------
    read_xy()
        returns two lists containing the x and y data
    read_cp(alpha)
        returns a list containing the cp data at each angle
        also returns a list of line numbers containing errors
    dcx(alpha,i)
        returns the x-component of the non-dimensional pressure force
    dcy(alpha,i)
        returns the y-component of the non-dimensional pressure force
    lift_coeff(alpha)
        returns the lift coefficient at a given angle
    calc_cls()
        returns a dictionary of the lift coefficient at each angle
    stagnation(alpha)
        returns a tuple giving the stagnation point at a given angle
    calc_stags(alpha)
        returns a dictionary of the stagnation point at each angle
    __repr__
        converts the Airfoil's information into a formatted string
    """
    
    def __init__(self,inputdir):
        """
        Constructs an airfoil object, reads given files, and calculates all
        required results.
        """
        # Make sure that the directory has a '/' at the end to allow for access
        # of files inside the directory.
        if inputdir[-1] == '/':
            self.__inputdir = inputdir
        else:
            self.__inputdir = inputdir + '/'
        # Make sure the given directory exists. If not, raise an exception
        # and inform the user that the directory does not exist.
        if not os.path.exists(self.__inputdir):
            raise RuntimeError('Given directory does not exist.')

        # Identify and read the xy data.
        self.__xyPath = self.__inputdir + "xy.dat"
        if not os.path.exists(self.__xyPath):
            raise RuntimeError('No xy data')
        (self.__nacaId,self.__x,self.__y) = self.read_xy()
        self.__lenData = len(self.__x) - 1
        
        # Identify all files that have pressure coefficient data at a certain
        # attack angle.
        self.__cpPaths = glob.glob(self.__inputdir+"alpha*.dat")
        if len(self.__cpPaths) == 0:
            raise RuntimeError('No cp data')
        # For each file, identify the angle, and read the file. The data is
        # stored in a dictionary using the attack angles (converted to numbers)
        # as keys and a lists with the data as values. If any error is
        # identified, an appropriate message is printed, and the file in
        # question is skipped, allowing the program to continue with the valid
        # data.
        self.__cpAlpha = dict()
        for pathName in self.__cpPaths:
            fileName = os.path.split(pathName)[1]
            alphaStr = fileName[5:-4]
            try:
                alpha = float(alphaStr)
                (cp,errors) = self.read_cp(pathName)
                if len(errors) > 0:
                    string = "ERROR: Non-numerical cp data at alpha = {}: {}"
                    print(string.format(alpha,errors))
                    continue
                if len(cp) == self.__lenData:
                    self.__cpAlpha[alpha] = cp
                elif len(cp) == 0:
                    print("ERROR: {} has no data".format(alpha))
                elif len(cp) > self.__lenData:
                    print("ERROR: {} has too many values".format(pathName))
                elif len(cp) < self.__lenData:
                    print("ERROR: {} has too few values".format(pathName))
            except ValueError:
                print("ERROR: {} has improper name".format(pathName))
        # Make a sorted list of the angles.  If no valid data was
        # identified, raise an error.
        self.__angles = sorted(self.__cpAlpha.keys())
        if len(self.__angles) == 0:
            raise RuntimeError("All cp data is flawed")

        # Calculate the chord length (the distance from the point with the
        # lowest x value to the point with the highest x value).
        leadx = min(self.__x)
        leady = self.__y[self.__x.index(leadx)]
        trailx = max(self.__x)
        traily = self.__y[self.__x.index(trailx)]
        self.__chord = math.sqrt((leadx-trailx)**2 + (leady-traily)**2)

        # Calculate the lift coefficents and stagnation points
        self.__cl = self.calc_cls()
        self.__stags = self.calc_stags()


    def read_xy(self):
        """
        Reads the file containing data on the shape of the airfoil.
        
        This converts the file to numerical data, and returns a string
        naming the airfoil type, a list with the x data, and a list with
        the y data.
        """
        x = []
        y = []
        tErrors = []
        cErrors = []
        with open(self.__xyPath,'r') as f:
            nacaId = f.readline().strip()
            for i, line in enumerate(f):
                # If line contains two numbers, record x and y values; if not,
                # record line number.
                try:
                    xy = line.split()
                    x.append(float(xy[0].strip()))
                    y.append(float(xy[1].strip()))
                except ValueError:
                    tErrors.append(i)
                except IndexError:
                    cErrors.append(i)
        # If any line is flawed, give the relevant message and exit.
        if len(x) == 0:
            raise RuntimeError('xy data file empty')
        if len(tErrors) > 0:
            raise RuntimeError("Non-numerical points: {}".format(tErrors))
        if len(cErrors) > 0:
            raise RuntimeError("Points missing y-value: {}".format(cErrors))
        return (nacaId,x,y)

    def read_cp(self,pathName):
        """
        Reads the cp data from a given file.

        This returns a list of cp data and a list of the indices of lines
        containing flawed data.
        """
        cp = []
        errors = []
        with open(pathName,'r') as f:
            f.readline()
            for i, line in enumerate(f):
                # If the line is a number, store it; if not, record the line
                # number and move on.
                try:
                    cp.append(float(line.strip()))
                except ValueError:
                    errors.append(i)
        return (cp,errors)

    def dcx(self,alpha,i):
        """
        Finds the pressure increment in the x direction for a given attack
        angle and location on the airfoil.
        
        Uses equation dcx = -(cp * dy) / chord
        """
        y1 = self.__y[i]
        y2 = self.__y[i+1]
        dy = y2 - y1
        cp = self.__cpAlpha[alpha][i]
        return -cp * dy / self.__chord

    def dcy(self,alpha,i):
        """
        Finds the pressure increment in the y direction for a given attack
        angle and location on the airfoil.
        
        Uses equation dcy = (cp * dx) / chord
        """
        x1 = self.__x[i]
        x2 = self.__x[i+1]
        dx = x2 - x1
        cp = self.__cpAlpha[alpha][i]
        return cp * dx / self.__chord

    def lift_coeff(self,alpha):
        """
        Finds the lift coefficient at a given attack angle.
        
        Adds up each individual dcx and dcy to find cx and cy, and
        calculates lift coefficient using the equation
        cl = cy * cos(alpha) - cx * sin(alpha)
        """
        cx = 0.0
        cy = 0.0
        # Math module assumes that angles are in radians for trigonometry.
        alphar = math.radians(alpha)
        for i in range(len(self.__x) - 1):
            cx += self.dcx(alpha,i)
            cy += self.dcy(alpha,i)
        cl = cy * math.cos(alphar) - cx * math.sin(alphar)
        return cl

    def calc_cls(self):
        """
        Finds the lift coefficient for each attack angle.
        """
        cl = dict()
        for alpha in self.__angles:
            cl[alpha] = self.lift_coeff(alpha)
        return cl

    def stagnation(self,alpha):
        """
        Finds the stagnation point for a given attack angle.

        The stagnation point is the point where cp is closest to 1. This 
        identifies that line segment, and returns the average x and y values
        of the segment, as well as the cp value.
        """
        stag = []
        for cp in self.__cpAlpha[alpha]:
            stag.append(abs(1-cp))
        stagMin = min(stag)
        ind = stag.index(stagMin)
        cpStag = self.__cpAlpha[alpha][ind]
        xp = (self.__x[ind] + self.__x[ind + 1]) / 2
        yp = (self.__y[ind] + self.__y[ind + 1]) / 2
        return (xp,yp,cpStag)

    def calc_stags(self):
        """
        Finds the stagnation point for each attack angle.
        """
        stags = dict()
        for alpha in self.__angles:
            stags[alpha] = self.stagnation(alpha)
        return stags
    
    def __repr__(self):
        """
        Converts the airfoil object to a string when being printed.
        
        This includes the NACA id and a line for each valid attack angle
        giving the lift coefficient and stagnation point.
        """
        string = "Test case: " + self.__nacaId + '\n\n'
        string += "  alpha     cl           stagnation pt\n"
        string += "  -----  -------  --------------------------\n"
        form = "  {0: .2f}  {1: .4f}  ({2[0]: .4f}, {2[1]: .4f})  {2[2]:.4f}\n"
        for alpha in self.__angles:
            string += form.format(alpha,self.__cl[alpha],self.__stags[alpha])
        return string
