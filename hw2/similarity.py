# This program takes in a data file containing movie ratings from an assortment
# of users, and calculates the similarity coefficients of the movies. The data
# is read from the file and placed in a dictionary. It is then processed to
# subtract the average rating for each movie from each individual rating.
# Next, the program goes through each potential pair of movies, finds the
# user that rated both movies, and calculates the similarity coefficient if
# there is enough overlap, placing the results in a new dictionary. A second
# dictionary is used to keep track of pairs that have already been processed
# to avoid wasting time on duplicate calculations. Finally, the most similar
# movie to each movie is determined, and the original movie, secondary movie,
# similarity coefficient, and number of shared users are written to a file.

# Import modules
import sys
import time

# Function to take dictionary of ratings
# and return a dictionary with each movie's average rating
def movie_average(moviesDict):
    # Create empty dictionary
    averageRating = dict()
    # For each movie, iterate through values in sub-dictionary and add rating.
    # Then divide by number of revies of each movie to find average rating.
    for movie in moviesDict:
        sum = 0.0
        for r in moviesDict[movie].values():
            sum += r
        averageRating[movie] = sum/len(moviesDict[movie])
    return averageRating

# Function to take dictionary of ratings and dictionary of average ratings,
# and subtract average ratings from raw ratings.
# This changes the original dictionary rather than creating a new one.
def deviation(moviesDict,avgDict):
    # Iterate through dictionary, subtracting the average value for each movie
    # from the raw rating
    for movie in moviesDict:
        average = avgDict[movie]
        for user in moviesDict[movie]:
            moviesDict[movie][user] -= average

# Function to take dictionary of ratings and two movie ids
# and return a set with all user ids that rated both movies
def overlap(moviesDict,movie1,movie2):
    # Create sets with the ids for all users who rated each movie
    users1 = set(moviesDict[movie1].keys())
    users2 = set(moviesDict[movie2].keys())
    # Find and return the intersection between the two sets
    shared = users1.intersection(users2)
    return shared

# Function to find sum of a list of values squared
def sum_squares(moviesDict,movie,shared):
    # Cycle through the set of shared users,
    # adding the square of their rating's deviation from average
    sum = 0.0
    for user in shared:
        sum += moviesDict[movie][user] ** 2
    return sum

# Function to find sum of products of shared movie ratings
def sum_products(moviesDict,movie1,movie2,shared):
    # Cycle through set of shared users,
    # adding the product of the deviations of their ratings
    # for each movie from the respective averages
    sum = 0.0
    for user in shared:
        r1 = moviesDict[movie1][user]
        r2 = moviesDict[movie2][user]
        sum += r1 * r2
    return sum

# Check for correct number of user inputs,
# and print usage message if inputs are inadequate
if len(sys.argv) < 3:
    print("Usage:")
    usage1 = "  $ python3 similarity.py <data_file>"
    usage2 = " <output_file> [user_thresh (default = 5)]"
    print(usage1 + usage2)
    sys.exit(0)
# Record input arguments. If a user threshold is specified, use that;
# if not, set default of 5
dataFile = sys.argv[1]
outputFile = sys.argv[2]
if len(sys.argv) == 4:
    userThresh = int(sys.argv[3])
else:
    userThresh = 5

# Read data file and convert to a dictionary.
# The keys for each dictionary are each movie ID.
# The value for each item is another dictionary.
# For each sub-dictionary, the key is the user ID
# and the value is the rating given to the movie by the user.
t1=time.time()
moviesDict = dict()
lines = 0
userIds = set()
with open(dataFile,'r') as f:
    # Iterate through each line of the data file,
    # converting each line into a list with entries representing user id,
    # movie id, rating, and timestamp (which is subsequently ignored)
    for line in f:
        lines += 1
        entry = []
        for value in line.split():
            entry.append(value)
        # Create variables to keep track of each value.
        # These are converted to integers to assist with later sorting.
        # If any value is not a number, the program responds by catching the
        # resulting ValueError and skipping over the line (although it still
        # adds to the line counter).
        try:
            user = int(entry[0])
            movie = int(entry[1])
            rating = float(entry[2])
            userIds.add(user)
            # If movie already is represented in the dictionary,
            # add the user and rating to its sub-dictionary.
            # If not, create a new sub-dictionary for the movie,
            # using the given user and rating.
            if movie in moviesDict:
                moviesDict[movie][user] = rating
            else:
                moviesDict[movie]={user: rating}
        except ValueError:
            continue

# Find the average rating for each movie
t2 = time.time()
averageRating = movie_average(moviesDict)
# Convert dictionary from raw ratings to deviation from average rating
t3 = time.time()
deviation(moviesDict,averageRating)

# Go through the dictionary, and determine the similarity coefficients for
# each pair of movies.
# The data is stored in a dictionary, with values of the movie ids
# and values of tuples storing results.
# The tuples contain three lists: the ids of movies with enough shared users,
# the simiaritiy coefficients, and the numbers of shared users.
# These lists are all in the same order (i.e. the second similarity coefficient
# refers to the second paired movie).
# This structure allows for the results for each movie to be considered
# separately, and for the maximum similarity coefficient to be easily identified
# and linked to its corresponding movie id and number of shared users
#
# Additionally, a second dictionary is used to keep track of the movie pairs
# whose similarities have already been calculated to avoid duplicate analysis
# (such as finding movie 1's similarity to movie 2, then movie 2's similarity
# to movie 1).
# The keys in this second dictionary are tuples with the first movie id
# and the second movie id.
# The values are lists with the similarity coefficient and number of
# shared users.
# This structure allows for specific pairs to be checked, and the result of
# each pair to be easily found.
#
# If there is insufficient data to find the similarity coefficient of two
# movies, the pair is not added to the first dictionary, and the list of
# results in the second dictionary is left blank.
t4 = time.time()
similarDict = dict()
completedPairs = dict()
for movie1 in moviesDict:
    # set up entry in dictionary
    similarDict[movie1] = ([],[],[])
    for movie2 in moviesDict:
        # Ignore all cases where movie is repeated
        if movie1 == movie2:
            continue
        # Check to see if the movie pair's similarity has already been
        # calculated. If so, and there is a valid result, the result is entered
        # into the dictionary. If the previous calculation did not produce a
        # valid result, nothing happens.
        # There is no need to enter this pair into the dictionary of completed
        # pairs, as it cannot come up a third time.
        elif (movie2,movie1) in completedPairs:
            if len(completedPairs[(movie2,movie1)]) > 0:
                similarDict[movie1][0].append(movie2)
                prior = completedPairs[(movie2,movie1)]
                similarDict[movie1][1].append(prior[0])
                similarDict[movie1][2].append(prior[1])
        # If the pair has not been previously determined, find a set of the
        # shared users.
        else:
            shared = overlap(moviesDict,movie1,movie2)
            nShared = len(shared)
            # If there are not enough shared users, add a blank record of the
            # pair to the dictionary of completed pairs, and add nothing to
            # the results dictionary.
            if nShared < userThresh:
                completedPairs[(movie1,movie2)]=[]
            # If there are enough shared users, calculate the similarity
            # as given in the assignment.
            else:
                s1 = sum_squares(moviesDict,movie1,shared)
                s2 = sum_squares(moviesDict,movie2,shared)
                # If the denominator is zero, there is no variation in the
                # ratings for one of the movies, and thus not enough information
                # to calculate the similarity coefficient, so a blank entry
                # is added to the completed pairs dictionary and nothing is
                # added to the results dictionary.
                if (s1 * s2) == 0:
                    completedPairs[(movie1,movie2)]=[]
                else:
                    s12 = sum_products(moviesDict,movie1,movie2,shared)
                    sim12 = s12 / ((s1 * s2) ** (0.5))
                    # Second movie id, similarity coefficient, and number of
                    # shared users are appended to the correct lists,
                    # and the results are placed in the completed pairs
                    # dictionary
                    similarDict[movie1][0].append(movie2)
                    similarDict[movie1][1].append(sim12)
                    similarDict[movie1][2].append(nShared)
                    completedPairs[(movie1,movie2)] = [sim12,nShared]

# Create a sorted list of all movie ids to use when writing the results to
# a file
t5 = time.time()
movieIds = list(similarDict.keys())
movieIdsSorted = sorted(movieIds)

# Write the movie ids to a file, accompanied by the most similar movie,
# the similarity coefficient, and the number of shared users, if there is
# at least one sufficiently similar movie.
with open(outputFile,'w') as f:
    for movie1 in movieIdsSorted:
        f.write(str(movie1))
        movieResults = similarDict[movie1]
        # If any movies have enough shared users, find the highest similarity
        # coefficient and the corresponding movie id and number of shared
        # users and write these to the file. If there are no paired movies,
        # do nothing, leaving the rest of the line blank.
        if len(movieResults[0]) >= 1:
            value = max(movieResults[1])
            loc = movieResults[1].index(value)
            movie2 = movieResults[0][loc]
            nCommon = movieResults[2][loc]
            f.write(" ({},{},{})".format(movie2,value,nCommon))
        # add a line break between movies
        f.write("\n")

# Find number of movies and users
nMovies = len(movieIds)
nUsers = len(userIds)

# Print required outputs
print("Input MovieLens file: " + dataFile)
print("Output file for similarity data: " + outputFile)
print("Minimum number of common users: {}".format(userThresh))
countStatement = "Read {} lines with total of {} movies and {} users"
print(countStatement.format(lines,nMovies,nUsers))
print("Computed similarities in {} seconds".format(t5-t1))
