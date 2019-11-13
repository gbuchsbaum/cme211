This contains Gabriel Buchsbaum's work on Homework 2 for CME 211

# Part 1

## 1. What were your considerations when creating this test data?
In general, I tried to give two of the movies reasonably similar ratings for most reviewers, and then gave the third movie different responses.  I usually made the first movie have somewhat more extreme ratings so that there would be two that are closely linked, two that are opposite, and two that are generally but not extremely different.  I also made sure to include significant variation (i.e. there are no people with duplicate answers) to include some natural variation.  While I created ratings for every person and every movie, I only included 25 out of the 30 in the file to make sure the program could handle the fact that not everyone sees every movie.
## 2. Were there certain characteristics of the real data and file format that you made sure to capture in your test data?
I used non-consecutive integers for the user and movie ids, since the ids are integers and the program needs to be able to handle gaps in the user ids.  I also made sure to randomize the order.  The information is separated by tabs, as in the real data.  I also added a fourth column with zeroes to represent the timestamps.
## 3. Did you create a reference solution for your test data? If so, how?
I made a reference solution (saved as test_similarities.txt, not pushed to github).  Since I had used excel to keep track of the reviews I was creating, I was able to use it to calculate the similarities.  I found the average rating for each movie, then subtracted the average from each individual review.  I then calculated the similarity value using the given formula, only using reviews done bo users who had reviewed both movies.

# Part 2

## Command line log:
```
$ python3 similarity.py ml-100k/u.data similarities.txt
Input MovieLens file: ml-100k/u.data
Output file for similarity data: similarities.txt
Minimum number of common users: 5
Read 100000 lines with total of 1682 movies and 943 users
Computed similarities in 32.09358239173889 seconds
```
## Output similarity file
```
$ head -n 10 similarities.txt
1 (918,0.9105046586065211,5)
2 (1056,0.9999805766784162,5)
3 (1081,0.9770523936627928,5)
4 (35,0.8035001899406666,6)
5 (976,0.9330795632032152,5)
6 (279,0.9597565073371668,5)
7 (968,0.997420592235218,7)
8 (590,0.8646937307646155,6)
9 (113,0.9644943052520142,5)
10 (1202,0.9724294104431035,5)
```
## Function breakdown
Five functions were used in this code.  The first takes in the dictionary that stores all of the data, and creates a new dictionary containing the average rating for each movie. The second function takes in the dictionary of the data and the dictionary of average ratings, and subtracts the average rating from each data point (since that is what is actually used in the similarity coefficient), changing the original dictionary. These are called one after the other immediately after all of the data is read and compiled into the original dictionary. The third function takes in a dictionary of data and two movie ids, and returns a set of all users that rated both movies. The fourth function takes in the main dictionary, a movie id, and a set of users, and computes the sum used in the denominator of the similarity coefficient equation.  The final function takes in the dictionary, two movie ids, and the set of shared users, and computes the numerator of the similarity coefficient.  These three functions are called for each individual movie pair.
