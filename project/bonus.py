# Import necessary modules
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
import sys

# If not enough input arguments are given, print usage message.
if len(sys.argv) < 3:
    print('Usage:')
    print('  python3 bonus.py <input file> <solution file>')
    sys.exit(0)

# Record input arguments
inputFile = sys.argv[1]
solutionFile = sys.argv[2]

if not os.path.exists(inputFile):
    raise RuntimeError(inputFile + " does not exist")
if not os.path.exists(solutionFile):
    raise RuntimeError(solutionFile + " does not exist")

# Read the input file and determine dimensions from it.
try:
    with open(inputFile, 'r') as fi:
        setup = (fi.readline()).split()
    length = float(setup[0])
    width = float(setup[1])
    h = float(setup[2])
except:
    raise RuntimeError("Input file unreadable")

# Set up figure
fig = plt.figure()
plt.xlim(0,length)
plt.ylim((width-length)/2,(length-width)/2 + width)
plt.xlabel('x')
plt.ylabel('y')

# Determine the number of the solution file
nSolution = int(solutionFile[-7:-4])

# Set up arrays to determine locations in the color plot and hold the average
# curve.
X = np.arange(0, length + h, h)
Y = np.arange(0, width + h, h)
avgCurve = np.empty(X.shape[0])

# Initialize list to hold images (each image is a list containing the color
# plot and the average temperature curve).
ims = []

# Loop through each intermediate solution file until the final one is reached,
# generating each color plot and average curve and adding them to ims.
nImage = 0;
while nImage < nSolution:
    # Detemine appropriate file name.
    currentFile = solutionFile[:-7] + '{:0>3}.txt'.format(nImage)
    if not os.path.exists(currentFile):
        raise RuntimeError(currentFile + "  does not exist")
    # Load data
    try:
        current = np.loadtxt(currentFile, dtype=np.float64)
    except:
        raise RuntimeError(currentFile + " is unreadable")
    # Calculate average temperature
    avg = np.mean(current[:,:-1])
    # Determine location of average temperature in each column
    for i in range(X.shape[0]):
        avgCurve[i] = np.interp(avg, current[:,i], Y)
    # Generate the current color plot
    im1 = plt.pcolor(X, Y, current, cmap='jet')
    # Generate the average temperature curve
    im2, = plt.plot(X,avgCurve, color='black')
    # Add plots as a sublist in ims and move to the next intermediate solution
    ims.append([im1, im2])
    nImage += 10

# Repeat process with final solution. This is done separately because the last
# file is most likely not a multiple of 10.
try:
    solution = np.loadtxt(solutionFile, dtype=np.float64)
except:
    raise RuntimeError(solutionFile + " is unreadable")
avg = np.mean(solution[:,:-1])
for i in range(X.shape[0]):
    avgCurve[i] = np.interp(avg, solution[:,i], Y)
im1 = plt.pcolor(X, Y, solution, cmap='jet')
im2, = plt.plot(X,avgCurve, color='black')
ims.append([im1, im2])

# Animate the images with an Artist Animation
im_ani = animation.ArtistAnimation(fig, ims, interval=200, repeat_delay=3000, blit=True)

# Set up writer and save animation as an mp4
if 'ffmpeg' in animation.writers.list():
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=5, metadata=dict(artist='gbuchsbaum'), bitrate=1800)
    im_ani.save(solutionFile[:-3]+'mp4', writer=writer)
else:
    print("Missing ffmpeg writer, no file saved")
    
print("Input file animated: {}".format(inputFile))

# Show results
plt.show()
