This directory contains Gabriel Buchsbaum's work on Homework 1 for CME 211.

# Part 2 Writeup:

## Command line log:
```
$ python3 generatedata.py 1000 600 50 "ref_1.txt" "reads_1.txt"
reference length: 1000
number reads: 600
read length: 50
aligns 0: 0.15
aligns 1: 0.7416666666666667
aligns 2: 0.10833333333333334

$ python3 generatedata.py 10000 6000 50 "ref_2.txt" "reads_2.txt"
reference length: 10000
number reads: 6000
read length: 50
aligns 0: 0.14766666666666667
aligns 1: 0.756
aligns 2: 0.09633333333333334

$ python3 generatedata.py 100000 60000 50 "ref_3.txt" "reads_3.txt"
reference length: 100000
number reads: 60000
read length: 50
aligns 0: 0.14996666666666666
aligns 1: 0.7508666666666667
aligns 2: 0.09916666666666667
```

## Test data considerations:
The reference was created by setting up an excel spreadsheet to randomly generate a sequence of 10 bases.  The spreadsheet also determined the read of length 3 generated from each possible starting position in the reference sequence.  The sheet was recalculated until a sequence was generated that had one read doubled.  Then, the doubled read was used, as well as three other reads that were spread relatively evenly through the reference sequence, then I chose an arbitrary set of three bases that did not appear in the reference.  As such, the test data is mostly random and the chosen reads cover most of the reference sequence, but the format is different from that used in the computer-generated data.  As long as the program is well-designed to cover a range of inputs rather than just inputs with the structure used by generatedata.py, anything that works on the test data should work on the full data.

## Distribution:
An exact 15%/75%/10% distribution is extremely unlikely because each time a read is generated, its type is chosen randomly.  However, the more reads that are generated, the closer the distribution comes to the intended distribution.  One point that is worth mentioning is that this just tracks the number of reads that are created to align each given number of times.  It is entirely possible that there are reads that were generated to only appear once, but actually appear twice due to some randomly-generated code happening to repeat a certain sequence.  The odds of this decrease as the read length increases, since randomly repeating 50 letters is much less likely than randomly repeating 10 letters, and increase as the reference length increases because there are more opportunities for a repeated read to occur.

## Time:
I spent about 1 hour doing part 1 and the basic framework for part 2, and 2.5 hours actually coding part 2, plus a half hour finishing comments in the code and working on the writeup.


# Part 3 Writeup:

## Command line log:
```
$ python3 processdata.py ref_1.txt reads_1.txt align_1.txt
reference length: 1000
number reads: 600
aligns 0: 0.15
aligns 1: 0.7416666666666667
aligns 2: 0.10833333333333334
elapsed time: 0.010715961456298828

$ python3 processdata.py ref_2.txt reads_2.txt align_2.txt
reference length: 10000
number reads: 6000
aligns 0: 0.14766666666666667
aligns 1: 0.756
aligns 2: 0.09633333333333334
elapsed time: 0.2736701965332031

$ python3 processdata.py ref_3.txt reads_3.txt align_3.txt
reference length: 100000
number reads: 60000
aligns 0: 0.14996666666666666
aligns 1: 0.7508666666666667
aligns 2: 0.09916666666666667
elapsed time: 23.792274236679077
```

## Distribution comparison:
The distribution of the reads that align zero, one, or two times precisely matches the distribution that was produced.  It is theoretically possible for a read to randomly appear twice even when unintended; however, with longer reads the probability of this occurring is vanishingly low.  For example, the probability of any randomly generated read with length 50 matching a given read is 1 in 1.27*10^30, so the only way a read could be randomly repeated is if the reference sequence is many orders of magnitude longer than the scales being considered here.

## Time scaling:
Based on the results, increasing the reference length (and correspondingly increasing the number of reads) increases the time required by a power of about 5/3 (i.e. multiplying the reference length by 10 multiplies the time required by 46.4).  The read length only has a minor impact on the time required, assuming that the number of reads remains constant.  According to these results, aligning the data for a human with 3 billion base pairs, 30x coverage, and reads of 50 base pairs would require about 690 million seconds, of about 22 years.  This is clearly infeasible with this code.

## Time:
Writing the code for this took about 2.5 hours, and the writeup took another half hour
