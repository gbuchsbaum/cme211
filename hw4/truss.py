"""
This module contains all class data and methods for a truss object.
"""

# Import necessary modules
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.sparse
import scipy.sparse.linalg
import warnings

class Truss:
    """
    Truss: A class used to create a truss object.

    This class takes in a file giving information on the location and
    forces on joints, and a file listing which joints each beam is
    connected to. It assembles this information into a simulation of 
    a truss, and can calculate the forces in static equilibrium.

    Attributes:
    -----------
    joints : 2D numpy array, data type float64
        all of the information on the joints extracted from the file
    fixed : 1D numpy array, data type int32
        a list of which joints are fixed (rigidly supported)
    beams : 2D numpy array, data type int32
        the joints each beam is connected to, extracted from beams file
    results : 1D numpy array, data type float64
        the results from the static equilibrium calculations

    Methods:
    --------
    __init__
        constructor: loads truss geometry from files
    trig(b)
        returns the portion of the compression force of a beam acting
        in the x and y directions
    computeStaticEquilibrium()
        computes the static equilibrium forces in the truss
    PlotGeometry()
        plots the truss geometry
    __repr__
        returns a string containing the results
    """

    def __init__(self,jointsFile,beamsFile):
        """
        Reads given files and uses them to construct a truss object.
        """

        # Check to make sure that files exist
        if not os.path.exists(jointsFile):
            raise RuntimeError("Joints file does not exist")
        if not os.path.exists(beamsFile):
            raise RuntimeError("Beams file does not exist")

        # Read joints file, checking for errors.
        try:
            self.__joints = np.loadtxt(jointsFile, dtype = np.float64)
        except:
            raise RuntimeError("Joints file unreadable")
        if self.__joints.shape[1] != 6:
            raise RuntimeError("Joints file improperly formatted")
        # A separate array is created to record fixed joints to avoid
        # complications due to switching between integers and floats.
        try:
            self.__fixed=np.loadtxt(jointsFile,dtype=np.int32,usecols=(5,))
        except:
            raise RuntimeError("Joints file improperly formatted")
        # Read beams file, checking for errors.
        try:
            self.__beams = np.loadtxt(beamsFile,dtype = np.int32)
        except:
            raise RuntimeError("Beams file unreadable")
        if self.__beams.shape[1] != 3:
            raise RuntimeError("Beams file improperly formatted")
        # A blank array is created for results to allow the __repr__ method
        # to respond if it is called before calculations are performed.
        self.__results = np.zeros((0,))

        # Check to make sure that the number of joints in the joints file is
        # the same as the number of joints referenced in the beams file
        # to ensure that both refer to the same truss and truss is properly
        # defined.
        nJointsInBeams = max(max(self.__beams[:,1]),max(self.__beams[:,2]))
        if nJointsInBeams != self.__joints.shape[0]:
            raise RuntimeError("Joints and beams do not match")

    def trig(self,b):
        """
        Calculates portion of compression force in beam b that is acting
        in x and y directions. This includes the signs relative to the
        joint listed first for each beam. The results are returned as
        a numpy array.
        Note: b is zero-indexed to avoid unnecessary conversions.
        """

        # Identify coordinates of each given endpoint of the beam
        joint1 = self.__joints[self.__beams[b,1]-1,1:3]
        joint2 = self.__joints[self.__beams[b,2]-1,1:3]
        # Find displacement and beam length
        displacement = joint2 - joint1
        length = np.linalg.norm(displacement)
        # Return x and y displacement, normalized by beam length
        results = displacement / length
        return results

    def computeStaticEquilibrium(self):
        """
        Calculates the forces in static equilibrium, and stores them
        in results as a numpy array.
        """

        # Determine number of equations and each type of variable
        nJoints = self.__joints.shape[0]
        nEqn = 2 * nJoints
        nFixed = sum(self.__fixed)
        nBeams = self.__beams.shape[0]
        nVariables = nBeams + 2 * nFixed
        # If the number of equations and the number of variables are unequal
        # (i.e. the system is overdetermined or underdetermined),
        # report this and end all following calculations.
        if nEqn != nVariables:
            e = "Truss geometry not suitable for static equilbrium analysis"
            raise RuntimeError(e)

        # Determine total number of coefficients needed in system of equations.
        # This includes all beam-joint connections (on both ends), and the
        # reaction forces in rigidly supported points.
        nCoefficients = 4 * nBeams + 2 * nFixed
        # Set up arrays needed for sparse array constructor
        data = np.zeros((nCoefficients,),dtype=np.float64)
        rowInd = np.zeros((nCoefficients,),dtype=np.int32)
        colInd = np.zeros((nCoefficients,),dtype=np.int32)

        # Add data to arrays.
        # For each beam, find the x and y coefficients, and the correct
        # location for each in the equation matrix. These are copied (with
        # reversed signs) for the second joint.
        for i in range(nBeams):
            beamJoints = self.__beams[i,1:3]
            beamxy = self.trig(i)
            data[4*i:4*i+4] = [beamxy[0],beamxy[1],-beamxy[0],-beamxy[1]]
            rowInd[4*i:4*i+2] = [2*(beamJoints[0]-1),2*beamJoints[0]-1]
            rowInd[4*i+2:4*i+4] = [2*(beamJoints[1]-1),2*beamJoints[1]-1]
            colInd[4*i:4*i+4] = i

        # Add reaction forces to equations, by going through each joint
        # and marking the correct spot in the equation array if the
        # joint is rigidly supported.
        nReact = 0
        data[4*nBeams:nCoefficients] = 1
        for i in range(self.__fixed.shape[0]):
            if self.__fixed[i] == 1:
                rowInd[4*nBeams+nReact:4*nBeams+nReact+2]=[2*i,2*i+1]
                colInd[4*nBeams+nReact]=nBeams+nReact
                colInd[4*nBeams+nReact+1]=nBeams+nReact+1
                nReact += 2

        # Use stored data to create a sparse CSR matrix holding the
        # coefficients used in the equations.
        equations = scipy.sparse.csr_matrix((data,(rowInd,colInd)))

        # Create an array holding external forces at each joint to use
        # as the resultant vector for the matrix multiplication.
        external = np.zeros((nEqn,),dtype = np.float64)
        for i in range(nJoints):
            external[2*i] = self.__joints[i,3]
            external[2*i + 1] = self.__joints[i,4]
            
        # Catch warnings from solver as errors
        warnings.filterwarnings('error')
        # Solve the system of equations and record the beam and reaction forces
        # in results. An exception is raised if a unique solution cannot be
        # determined.
        try:
            sol = scipy.sparse.linalg.spsolve(equations,external)
        except:
            e = "Cannot solve the linear system, unstable truss?"
            raise RuntimeError(e)
        self.__results = sol


    def PlotGeometry(self,fileName):
        """
        Plots the truss geometry, and saves it under the specified name.
        """

        plt.figure(1)
        # For each beam, find the coordinates of its endpoints and plot
        # a line connecting those points.
        for i in range(self.__beams.shape[0]):
            x1 = self.__joints[self.__beams[i,1]-1,1]
            y1 = self.__joints[self.__beams[i,1]-1,2]
            x2 = self.__joints[self.__beams[i,2]-1,1]
            y2 = self.__joints[self.__beams[i,2]-1,2]
            x = [x1,x2]
            y = [y1,y2]
            plt.plot(x,y,'b-')

        # Find the region occupied by the truss, and extend the axes limits
        # to one unit beyond these in each direction. This ensures that there
        # is a buffer around the truss, so that nothing is hidden by the
        # edges of the plot.
        minx = min(self.__joints[:,1])
        maxx = max(self.__joints[:,1])
        miny = min(self.__joints[:,2])
        maxy = max(self.__joints[:,2])
        plt.xlim(minx-1,maxx+1)
        plt.ylim(miny-1,maxy+1)
        # Save and show the figure, which contains every beam.
        plt.savefig(fileName)
        plt.show()

    def __repr__(self):
        """
        Converts the truss object to a string for the purpose of printing
        the results to the console.
        """

        # If the forces have not been calculated, calculate them
        if self.__results.shape[0] == 0:
            self.computeStaticEquilibrium()
        # Assemble the string line-by-line
        strOut = "Beam      Force\n"
        strOut += "---------------"
        formStr = "\n{:3d}  {: 10.3f}"
        # Add a line for each beam. While results does include reaction
        # forces, these are not included in the string representation
        for i in range(self.__beams.shape[0]):
            strOut += formStr.format(self.__beams[i,0],self.__results[i])
        return strOut
