import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import ConnectionPatch
import math
from itertools import permutations
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
import numpy as np
import secrets



df = pd.read_csv('train_distance_matrix.csv')

# In case, somehow, we get the same random value
seenRandomValues = []
def getRandomNumber():
    haveNotFoundUniqueRandomNumber = True
    while(haveNotFoundUniqueRandomNumber):
        # We have 30,000+ rows in the dataset
        number = secrets.SystemRandom().randint(0, 30000)
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
numberOfDestinationsToCompare = 4
#######################################################

# Change this to randomize points on graph
#######################################################
randomize = True
#######################################################

if randomize:
    pickup_longitude = df['pickup_longitude'].to_list()
    pickup_latitude = df['pickup_latitude'].to_list()
    randomLongitudes = randomValues(
        numberOfDestinationsToCompare, pickup_longitude)
    randomLatitudes = randomValues(
        numberOfDestinationsToCompare, pickup_latitude)

else:
    pickup_longitude = df['pickup_longitude'].to_list()[
        :numberOfDestinationsToCompare]
    pickup_latitude = df['pickup_latitude'].to_list()[
        :numberOfDestinationsToCompare]


fig = plt.figure()
ax1 = fig.add_subplot(121)

seenColors = []


def getRandomColors():
    haveNotFoundUniqueRandomNumber = True
    while(haveNotFoundUniqueRandomNumber):
        def r(): return secrets.SystemRandom().randint(0, 255)
        if r not in seenColors:
            seenColors.append(r)
            haveNotFoundUniqueRandomNumber = False
            return '#%02X%02X%02X' % (r(), r(), r())


colors = []
points = []
x = []
y = []
for i in range(numberOfDestinationsToCompare):
    colors.append(getRandomColors())
    if randomize:
        points.append([randomLongitudes[i], randomLatitudes[i]])
        x.append(randomLongitudes[i])
        y.append(randomLatitudes[i])
    else:
        points.append([pickup_longitude[i], pickup_latitude[i]])
        x.append(pickup_longitude[i])
        y.append(pickup_latitude[i])

for i in range(len(points)):
    ax1.plot(points[i][0], points[i][1], markerfacecolor=colors[i],
             marker='o', markeredgecolor=colors[i])
    if i == 0:
        ax1.annotate('Start', [points[i][0], points[i][1]])

uuid = 1
tempId = 1
nodes = {}
for i in range(len(points)):
    data = {
        'id': uuid,
        'color': colors[i],
        'connectedNodes': {}
    }
    node = {
        'id': uuid,
        'color': colors[i],
        'connectedNodes': {}
    }
    for coords in points:
        # NOTE: might act weird if there are same values in array -- whichever comes 1st might bring by index
        if points.index(coords) == i:
            tempId += 1
            continue

        # (x2 - x1) ** 2 + (y2 - y1) **2
        distanceBetween = round(math.sqrt(
            (points[i][0] - coords[0]) ** 2 + (points[i][1] - coords[1]) ** 2) * 100, 2)

        currentNode = {
            # What node this node is looking at
            'distanceBetween': distanceBetween,
            'id': tempId,
            'color': colors[tempId - 1],
            'visited': {}
        }

        node['connectedNodes'][tempId] = currentNode
        midpoint_X = (coords[0] + points[i][0]) / 2
        midpoint_Y = (coords[1] + points[i][1]) / 2
        con1 = ConnectionPatch(xyA=points[i], xyB=coords, coordsA="data",
                               coordsB="data", color="blue", linestyle=':', linewidth=1)
        ax1.add_artist(con1)
        ax1.text(midpoint_X, midpoint_Y, str(round(distanceBetween, 2)))
        tempId += 1

    uuid += 1
    tempId = 1
    nodes[node['id']] = node

print(nodes)

startingPoint = [0, 0]
checkedPoints = []

def findNextAnchor(nodes):
    dist = nodes[1]['connectedNodes'][2]['distanceBetween']
    randomPoint_X = round(dist / 2, 3)

    x2 = randomPoint_X
    y2 = dist / (x2 ** 2)

    return [x2, y2]
    # distCheck = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
   
randomAnchor = findNextAnchor(nodes)

def findPointsInCircle(centerPoint, radius):
    points = []
    visitedPoints = {}

    for i in range(0, 360):
        x = round(centerPoint[0] + (radius * math.cos(i)), 2)
        y = round(centerPoint[1] + (radius * math.sin(i)), 2)
        if f'{x, y}' not in visitedPoints:
            points.append([x, y])
            visitedPoints[f'{x, y}'] = True
    return [points, visitedPoints]

# def findPointGivenTwoPoints(points1, distance1, point2, distance2):



def plotAndFindIntercection(startingPoint, randomAnchor):
    plottedNodes = {
        '1': startingPoint,
        '2': randomAnchor,
    }
    print(plottedNodes)
    fig = plt.figure()
    ax2 = fig.add_subplot(121)
    for i in range(3, len(nodes) + 1):
        distanceFromStartingNode = nodes[1]['connectedNodes'][i]['distanceBetween']
        distanceFromAnchor = nodes[2]['connectedNodes'][i]['distanceBetween']







        # resultsAnchor = findPointsInCircle(randomAnchor, distanceFromAnchor)
        # pointsAnchor = resultsAnchor[0]
        # visitedPointsAnchor = resultsAnchor[1]

        # resultsStarting = findPointsInCircle(startingPoint, distanceFromStartingNode)
        # pointsStarting = resultsStarting[0]




        # matches = []
        
        # for i in range(len(pointsAnchor)):
        #     current = pointsAnchor[i]
        #     ax2.plot(float(current[0]), float(current[1]), markerfacecolor=colors[0],
        #             marker='o', markeredgecolor=colors[0])
        # for i in range(len(pointsStarting)):
        #     current = pointsStarting[i]
      
        #     if current in pointsAnchor:
        #         matches.append(current)
        #     ax2.plot(float(current[0]), float(current[1]), markerfacecolor=colors[1],
        #             marker='o', markeredgecolor=colors[0])
    print(matches)
    plt.show()
plotAndFindIntercection(startingPoint, randomAnchor)



df = pd.DataFrame(list(zip(x, y)), columns=['x', 'y'])

########### Elbow method to find K ###########
# print(points)
# k_range = range(2,10)
# sse = []

# optimalValueForK = 0
# for k in k_range:
#     km = KMeans(n_clusters=k)
#     km.fit(df[['x', 'y']])
#     labels = km.labels_
#     print('Labels are: ', labels)
#     score = silhouette_score(df, labels, metric = 'euclidean')
#     if score >= optimalValueForK:
#         optimalValueForK = k
#     sse.append(score)
# print(optimalValueForK)

# # optimalValueForK += 1
# scaler = MinMaxScaler()
# scaler.fit(df[['x']])
# df['x'] = scaler.transform(df[['x']])

# scaler.fit(df[['y']])
# df['y'] = scaler.transform(df[['y']])

# kmReal = KMeans(n_clusters=optimalValueForK)
# y_predict = kmReal.fit_predict(df)
# df['cluster'] = y_predict

# fig = plt.figure()
# ax2 = fig.add_subplot(121)

# for cluster in range(optimalValueForK):
#     ax2.scatter(df[df.cluster == cluster]['x'], df[df.cluster == cluster]['y'], color=colors[cluster])
# plt.show()
# print(sse)



###############################################



# combos = {}
# permutation = permutations(list(nodes.keys())[1:], len(nodes.keys()) - 1)
# print(nodes)
# best = None
# worst = None
# bestCountOrder = None
# for tup in permutation:
#     count = 0
#     indexCount = 0
#     countOrder = []
#     for key in tup:
#         nextIndex = tup.index(key) + 1
#         if tup.index(key) == 0:
#             count += nodes[1]['connectedNodes'][tup[0]]['distanceBetween']
#             countOrder.append(nodes[1]['connectedNodes'][tup[0]]['distanceBetween'])
#         if len(tup) > nextIndex:
#             count += nodes[key]['connectedNodes'][tup[nextIndex]]['distanceBetween']
#             countOrder.append(nodes[key]['connectedNodes'][tup[nextIndex]]['distanceBetween'])
#         indexCount += 1
#     if best == None or count < best:
#         best = count
#         bestCountOrder = countOrder
#     if worst == None or count > worst:
#         worst = count

# print('Count order = ', bestCountOrder)
# print('Best case: ', best)
# print('Worst case: ', worst)
# plt.show()
