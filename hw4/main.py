"""
This file contains the code for running an analysis on a given truss.
"""

# Import necessary modules
import sys
import truss

# Check for adequate input arguments, and print usage message if inadequate
if len(sys.argv) < 3:
    print('Usage:')
    str1 = '  python3 main.py [joints file] [beams file] '
    str2 = '[optional plot output file]'
    print(str1 + str2)
    sys.exit(0)

# Store input arguments
jointsFile = sys.argv[1]
beamsFile = sys.argv[2]

try:
    # Create truss object
    t = truss.Truss(jointsFile,beamsFile)

    # If a plot output file is given, plot the truss geometry.
    # This is done before calculations so that geometry can be shown even if
    # forces cannot be calculated.
    if len(sys.argv) == 4:
        outFile = sys.argv[3]
        t.PlotGeometry(outFile)

    # Calculate static equilibrium forces and print results
    t.computeStaticEquilibrium()
    print(t)
    
except RuntimeError as e:
    print('ERROR: {}'.format(e))
    sys.exit(2)
