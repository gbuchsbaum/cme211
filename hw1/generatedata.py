import sys
import random
if __name__ == "__main__":
    if len(sys.argv) <= 5:
        # Not enough arguments, print usage message
        print("Usage:")
        print("  $ python3 generatedata.py <ref_length> <nreads> <read_len> <ref_file> <reads_file>")
        sys.exit(0)
    # Assign inputs to variables, including converting strings to numbers if necessary
    refLength = int(sys.argv[1])
    nReads = int(sys.argv[2])
    readLen = int(sys.argv[3])
    refFile = sys.argv[4]
    readsFile = sys.argv[5]
    # Set up converstion from random number to DNA base by creating a list with the available bases
    baseAssign = ['A','C','G','T']
    # Number of randomly-assigned and copied base pairs in reference file.
    # Subtraction is used for to determine the number of copied pairs to avoid issues created by rounding down if refLength is not a multiple of four
    randLength = int(0.75 * refLength)
    copyLength = refLength - randLength
    # A random integer from 0 to 3 is chosen, and then the letter in the corresponding position in baseAssign is written to the end of a list
    randomList = []
    for i in range(randLength):
        randomList.append(baseAssign[random.randint(0,3)])
    randomText = "".join(randomList)
    copyText = randomText[-copyLength:]
    refText = randomText + copyText
    with open(refFile,'w') as f1:
        f1.write(refText)
    # Generate reads
    # Determine the length of the reference sequence made of unique reads
    uniqueLength = int(0.5 * refLength)
    # Set up variables to keep track of the number of reads generated to have each given number of reads.
    # These are floats rather than integers to aid in the division at the end
    align0 = 0.0
    align1 = 0.0
    align2 = 0.0
    # As each read is generated, append it to a list
    readsList = []
    for i in range(nReads):
        rand = random.random()
        if rand < 0.75:
            # 75% of the time, pick a random position in the first (unique) half and generate a read of the required length from there
            # Add a line break at the end and increase the count of single-aligned reads
            readStart = random.randint(0,uniqueLength-1)
            readEnd = readStart + readLen
            readsList.append(refText[readStart:readEnd]+"\n")
            align1 = align1 + 1
        elif rand < 0.85:
            # 10% of the time, pick a random position in the last (doubled) quarter and generate a read of the required length from there
            # Add a line break at the end and increase the count of single-aligned reads
            readStart = random.randint(randLength,(refLength-readLen))
            readEnd = readStart + readLen
            readsList.append(refText[readStart:readEnd]+"\n")
            align2 = align2 + 1
        else:
            # 15% of the time, randomly generate new reads until one not in the reference is found.
            # Use a while loop, since a new read must be repeatedly generated until it does not appear in the reference.
            # Each read is constructed by generating a list of random bases, then joining the list to form a string.
            # The position of the possible read is found in the reference sequence.
            # If the proposed read is not found, the find function returns -1, and the loop is exited with the unique read
            found = 0
            str = ""
            readStr = ""
            while found >= 0:
                readList = []
                for i in range(readLen):
                    readList.append(baseAssign[random.randint(0,3)])
                readStr = str.join(readList)
                found = refText.find(readStr)
            readsList.append(readStr+"\n")
            align0 = align0 + 1
    # Convert readsList to a string and write the string to readsFile
    readsString = "".join(readsList)
    with open(readsFile,'w') as f2:
        f2.write(readsString)
    # Print required outputs
    print("reference length: {}".format(refLength))
    print("number reads: {}".format(nReads))
    print("read length: {}".format(readLen))
    print("aligns 0: {}".format(align0/nReads))
    print("aligns 1: {}".format(align1/nReads))
    print("aligns 2: {}".format(align2/nReads))
