""" CMPE 365 Lab 2 / Assignment 1
Written by: Nick Dal Farra
Student #: 20010466
Date: 9/21/2019

I certify that this submission contains only my own work, except as noted.

"jesus christ it actually works!"
- Me, 10:13 PM Saturday night

"""

import pprint, sys
pp = pprint.PrettyPrinter() # make the matrix look nice
INFINITY = sys.maxsize # practical infinity

# read the text file
with open("2019_Lab_2_flights_real_data.txt","r") as text:
    ncities = int(text.readline())
    contents = text.read()
    lines = contents.split("\n")
    flist = [] #initialize the flights list of lists
    n = 0 #count the number of flights. Flight # will serve as a unique identifier later.

    for line in lines:
        if line != '':
            flist.append(line[:].split('\t'))
            n += 1
    
    #print(n)
    for i in range(n):
        for j in range(4):
            flist[i][j] = int(flist[i][j])
#in flist[city][0 = departing city], [1 = arriving city], [2 = departing time], [3 = arriving time]

# more preprocessing work - use the flight list to make a 3D list with flights[dep][arv][flight#]
flights = [[[] for _ in range(ncities)] for _ in range(ncities)]
for i in range(n):
    flights[flist[i][0]][flist[i][1]].append(i)
# in this way, we allow for multiple edges between verticies

# pre-processing is done. Let's get algorithmic:
# Where are we starting, and where do we want to go?
start = 66
end = 4

# let's initialize our arra... I mean lists
cost = [INFINITY]*ncities
estimate = [INFINITY]*ncities
reached = [False]*ncities
predecessor=[None]*ncities
# candidate[i][0] holds t/f, candidate[i][1] holds flight#, candidate[i][2] holds flight time
candidate = [[False,None] for _ in range(ncities)]

# what do we know already, from our choice of start?
cost[start] = 0
predecessor[start] = -1 
reached[start] = True

# find out what our estimates are
for i in range(ncities):
    if len(flights[start][i]) != 0: #if accessible from start
        candidate[i][0] = True
        predecessor[i] = start
        for j in flights[start][i]: # for all flights to i
            if flist[j][3] < estimate[i]:
                estimate[i] = flist[j][3]
                candidate[i][1] = j

# this main algorithm code is based loosely off the solutions 
# posted for Lab 1. Note that we once we've discovered the cost
# of getting to our destination, we can stop the loop. If our destination 
# is unreachable, there is an internal break that will cause us to exit
while cost[end] == INFINITY:

    # find the best option available
    best_time = INFINITY
    best_flight = None
    for i in range(ncities):
        if candidate[i][0] and estimate[i] < best_time:
            best_flight = candidate[i][1]
            best_time = flist[best_flight][3]

    if best_time == INFINITY:
        break #no candidates exist

    # things to update once we've selected the best flight:
    best_city = flist[best_flight][1]
    reached[best_city] = True
    cost[best_city] = best_time
    candidate[best_city][0] = False

    # let's update our candidates and predecessors
    # we're looking for reachable neighbours of best_city

    # I don't think this part is working properly (i.e. it isn't finding the best route). It seems
    # that we always look for the best option at the current node, and 
    # that we are only look for the best option across all searched nodes.

    # actually never mind, I got it working. It just feels good to write this afterwards :)
    # I just needed to add the time_arv < estimate[x] conidition to the bottom if statement
    for x in range(ncities):
        if len(flights[best_city][x]) != 0 and not reached[x]:
            best_time_test = INFINITY
            for flight in flights[best_city][x]: # checking all flights out of best_city
                time_out = flist[flight][2]
                time_arv = flist[flight][3]
                if time_out >= best_time and time_arv < best_time_test and time_arv < estimate[x]:
                    best_time_test = time_arv
                    candidate[x][0] = True
                    candidate[x][1] = flight
                    estimate[x] = time_arv
                    predecessor[x] = best_city

# Time to print our results. using predecessor, follow our path from end to start, then 
# we print it out backwards to show the chronological order of travel.
if cost[end] != INFINITY:
    city = end
    reversechronological = [end]
    while city != start:
        reversechronological.append(predecessor[city])
        city = predecessor[city]

    # print it backwards
    n = len(reversechronological)
    print('Optimal route from ' + str(start) + ' to ' + str(end) + ':\n')
    for i in range(n-1):
        print('Fly from ' + str(reversechronological[n - i - 1]) + ' to ' + str(reversechronological[n - i - 2]))
    print('\nWe arrive at time ' + str(cost[end]))
else:
    print('Your destination is not reachable. Amey\'s taxi: (613) 646 - 1111')

# This assignment took a while but was lots of fun.
# Also this is my first time using Python so critiques on form are really appreciated!
# Next step for me is looking at defining internal functions / taking advantage of
# more of Python's features
# 
# All the best,
# 
# Nick
