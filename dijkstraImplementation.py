import pprint
import sys
INFINITY = sys.maxsize #practical infinity
pp = pprint.PrettyPrinter() #make the matrix look nice

#read data
with open("Dijkstra_Data_1600.txt", "r") as f:
    size = int(f.readline())
    contents = f.read()
    lines = contents.split("\n")
    W = [] #initialize the weights list of lists
    for line in lines:
        W.append(line[:-1].split())
    
    for i in range (size):
        for j in range(size):
            W[i][j] = int(W[i][j])

    #weights matrix is of form W[node][connection]
    #pp.pprint(W)


#Initialize the bookkeeping lists
cost = [INFINITY]*size
estimate = [INFINITY]*size
reached = [False]*size
candidate = [False]*size
#Things we know about node 0
cost[0] = 0
reached[0] = True

#Find estimates for all neighbours of node 0
for i in range(1,size):
    if W[i][0] != 0:
        estimate[i] = W[i][0] #estimate is shortest we've seen
        candidate[i] = True #now a candidate for next shortest path

#print(candidate)
#print(estimate)

#Big ol' while loop. The bread and butter
while INFINITY in cost:

    best_candidate_estimate = INFINITY
    for x in range(size):
        if candidate[x] and estimate[x] < best_candidate_estimate:
            v = x
            best_candidate_estimate = estimate[v]

    cost[v] = estimate[v]
    reached[v] = True
    candidate[v] = False

    for y in range(size): #update the neighbours of v
        if W[v][y] > 0 and reached[y] == False:
            if cost[v] + W[v][y] < estimate[y]:
                estimate[y] = cost[v] + W[v][y]
                candidate[y] = True

x = 0
xindex = 0
for i in range(size):
    if cost[i] > x:
        x = cost[i]
        xindex = i

print("\nThis network has " + str(size) + " nodes.")
print("The node furthest from node 0 is node " + str(xindex) + ".")
print("It is a distance of " + str(x) + " from node 0.\n")