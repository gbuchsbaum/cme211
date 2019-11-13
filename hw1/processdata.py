import sys
import time
if len(sys.argv) <= 3:
    # Not enough arguments, print usage message
    print("Usage:")
    print("  $ python3 processdata.py <ref_file> <reads_file> <align_file>")
    sys.exit(0)
# Assign inputs to variables
refFile = sys.argv[1]
readsFile = sys.argv[2]
alignFile = sys.argv[3]
# Read reference (removing line break at end)
with open(refFile,'r') as f1:
    reference = (f1.read()).strip()
# Read reads file and create a list, with each read as a separate element
with open(readsFile,'r') as f2:
    reads = f2.readlines()
# Intialize variables to record reads of each type
align0 = 0.0
align1 = 0.0
align2 = 0.0
# Record start time
timeStart = time.time()
with open(alignFile,'w') as f3:
    for read_ in reads:
        read = read_.strip()
        firstAlign = reference.find(read)
        f3.write(read + " " + str(firstAlign))
        if firstAlign >= 0:
            secondAlign = reference.find(read,firstAlign+1)
            if secondAlign >=0:
                f3.write(" " + str(secondAlign))
                align2 = align2 + 1
            else:
                align1 = align1 + 1
        else:
            align0 = align0 + 1
        f3.write("\n")
timeStop = time.time()
timeElapsed = timeStop - timeStart
nReads = len(reads)
print("reference length: {}".format(len(reference)))
print("number reads: {}".format(nReads))
print("aligns 0: {}".format(align0/nReads))
print("aligns 1: {}".format(align1/nReads))
print("aligns 2: {}".format(align2/nReads))
print("elapsed time: {}".format(timeElapsed))
