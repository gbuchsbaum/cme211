import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys


if len(sys.argv) < 3:
    print('Usage:')
    print('  python3 bonus.py <input file> <solution file>')
    sys.exit(0)

inputFile = sys.argv[1]
solutionFile = sys.argv[2]

with open(inputFile, 'r') as fi:
    setup = (fi.readline()).split()

length = float(setup[0])
width = float(setup[1])
h = float(setup[2])

fig = plt.figure()

nSolution = int(solutionFile[-7:-4])
print(nSolution)


X = np.arange(0, length + h, h)
Y = np.arange(0, width + h, h)
avgCurve = np.empty(X.shape[0])

fig, ax = plt.subplots()
im1, = plt.pcolor(X,Y,np.loadtxt(solutionFile[:-7]+'000.txt'), cmap='jet', animated=True)
#im2, = plt.plot([],[], animated=True)
ax.set_xlim(0,length)
ax.set_ylim((width-length)/2,(length-width)/2 + width)

def update(nImage, X, Y):
    currentFile = solutionFile[:-7] + '{:0>3}.txt'.format(nImage)
    current = np.loadtxt(currentFile, dtype=np.float64)
    avg = np.mean(current[:,:-1])
    for i in range(X.shape[0]):
        avgCurve[i] = np.interp(avg, current[:,i], Y)
    im1, = plt.pcolor(X, Y, current, cmap='jet')
#    im2, = plt.plot(X,avgCurve)
    return im1,

def init():
    fig.colorbar(im1, ax=ax)
    print('asdf')
    return im1,


ims = np.arange(0, nSolution, 10, dtype=np.int32)
ims = np.append(ims, nSolution)


#solution = np.loadtxt(solutionFile, dtype=np.float64)
#avg = np.mean(solution[:,:-1])
#for i in range(X.shape[0]):
#    avgCurve[i] = np.interp(avg, solution[:,i], Y)
#im1 = plt.pcolor(X, Y, solution, cmap='jet')
#im1.colorbar()
#im3, = plt.plot(X,avgCurve)
#ims.append([im1, im3])

#ims.append((plt.pcolor(X, Y, solution, cmap='jet'),))
    
#for add in np.arange(15):
#    ims.append((plt.pcolor(x, y, base + add, norm=plt.Normalize(0, 30)),))
    
im_ani = animation.FuncAnimation(fig, update, frames=ims, init_func=init(), fargs=(X,Y), interval=200, repeat_delay=3000, blit=True)
    #im_ani.save('im.mp4', metadata={'artist':'Guido'})
    
plt.show()
