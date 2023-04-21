import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import ConnectionPatch
import math
import random


class Node:
    def __init__(self, data, next):
        self.data = data
        self.next = None

df = pd.read_csv('train_distance_matrix.csv')

# In case, somehow, we get the same random value
seenRandomValues = []
def getRandomNumber():
    haveNotFoundUniqueRandomNumber = True
    while(haveNotFoundUniqueRandomNumber):
            # We have 30,000+ rows in the dataset
            number = random.randint(0, 30000)
            if number not in seenRandomValues:
                seenRandomValues.append(number)
                haveNotFoundUniqueRandomNumber = False
                return number



def randomValues(numOfRows, arr):
    values = []

    for row in range(numOfRows):
        values.append(arr[getRandomNumber()])

    return values
        
# Change this to change how many points we see on graph
#######################################################
numberOfDestinationsToCompare = 10
#######################################################

# Change this to randomize points on graph
#######################################################
randomize = True
#######################################################

if randomize:
    pickup_longitude = df['pickup_longitude'].to_list()
    pickup_latitude = df['pickup_latitude'].to_list()
    randomLongitudes = randomValues(numberOfDestinationsToCompare, pickup_longitude)
    randomLatitudes = randomValues(numberOfDestinationsToCompare, pickup_latitude)

else:
    pickup_longitude = df['pickup_longitude'].to_list()[:numberOfDestinationsToCompare]
    pickup_latitude = df['pickup_latitude'].to_list()[:numberOfDestinationsToCompare]


fig = plt.figure()
ax1 = fig.add_subplot(121)

seenColors = []
def getRandomColors():
    haveNotFoundUniqueRandomNumber = True
    while(haveNotFoundUniqueRandomNumber):
            r = lambda: random.randint(0,255)
            if r not in seenColors:
                seenColors.append(r)
                haveNotFoundUniqueRandomNumber = False
                return '#%02X%02X%02X' % (r(),r(),r())
colors = []
points = []
for i in range(numberOfDestinationsToCompare):
    colors.append(getRandomColors())
    if randomize:
        points.append([randomLongitudes[i], randomLatitudes[i]])
    else:
        points.append([pickup_longitude[i], pickup_latitude[i]])

for i in range(len(points)): 
    ax1.plot(points[i][0], points[i][1], markerfacecolor=colors[i], marker='o', markeredgecolor=colors[i])

uuid = 1
tempId = 1
nodes = []
for i in range(len(points)):
    data = {
        'id': uuid,
        'color': colors[i],
        'connectedNodes': []
    }
    node = Node(data, None)
    for coords in points:
        # NOTE: might act weird if there are same values in array -- whichever comes 1st might bring by index
        if points.index(coords) == i:
            continue
            
        tempId += 1
        
        # (x2 - x1) ** 2 + (y2 - y1) **2
        distanceBetween = round(math.sqrt((points[i][0] - coords[0]) ** 2 + (points[i][1] - coords[1]) ** 2) * 100, 2)

        currentNode = {
            # What node this node is looking at
            'distanceBetween': distanceBetween,
            'uuid': tempId,
            'color': colors[tempId - 1]
        }

        node.data['connectedNodes'].append(currentNode)
        midpoint_X = (coords[0] + points[i][0]) / 2
        midpoint_Y = (coords[1] + points[i][1]) / 2
        con1 = ConnectionPatch(xyA=points[i], xyB=coords, coordsA="data", coordsB="data", color="blue", linestyle=':',linewidth=1)
        ax1.add_artist(con1)
        ax1.text(midpoint_X, midpoint_Y, str(round(distanceBetween, 2)))
    uuid += 1
    tempId = 1
    nodes.append(node)

for node in nodes:
    print(node.data)

plt.show()

