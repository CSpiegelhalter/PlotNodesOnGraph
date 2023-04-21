import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import ConnectionPatch
import math
import random
import copy
from itertools import permutations, combinations_with_replacement


# class Node:
#     def __init__(self, data, next):
#         self = data
#         self.next = None


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
numberOfDestinationsToCompare = 8
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
        def r(): return random.randint(0, 255)
        if r not in seenColors:
            seenColors.append(r)
            haveNotFoundUniqueRandomNumber = False
            return '#%02X%02X%02X' % (r(), r(), r())


colors = []
points = []
for i in range(numberOfDestinationsToCompare):
    colors.append(getRandomColors())
    if randomize:
        points.append([randomLongitudes[i], randomLatitudes[i]])
    else:
        points.append([pickup_longitude[i], pickup_latitude[i]])

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



# worst = None
# best = None
# for i in range(len(nodes[0]['connectedNodes'])):
#     node = nodes[0]['connectedNodes'][i]
#     startId = nodes[0]['id']
#     for inner in nodes[i]['connectedNodes']:
#         current = node['distanceBetween']
#         addString = ''

#         addString += f'{current}'

#         if inner['id'] == node['id']:
#             continue
#         if inner['id'] == startId:
#             continue
#         for each in nodes:
#             if each['id'] == inner['id']:
#                 for distance in each['connectedNodes']:
#                     if distance['id'] == node['id'] and distance['id'] != startId:
#                         addString += f" + {distance['distanceBetween']}"
#                         current += distance['distanceBetween']

#         print(addString)
#         if worst == None or current > worst:
#             worst = current
#         if best == None or current < best:
#             best = current


# count = 0
# reset = False
# def dfs(graph, node, ogCount):
#     for each in node['connectedNodes'].keys():
#         if node['id'] not in node[each]['visited']:
#             for i in graph.keys():
#                 graph[i]['connectedNodes'][node['each']]['visited'][node['id']] = True
#             count += node[each]['distanceBetween']


# worst = None
# best = None
# starterId = nodes.keys()[0]['id']
# for key in nodes[starterId]['connectedNodes'].keys():
#     copied = copy.deepcopy(nodes[1:])
#     firstRelation = copied[key]['connectedNodes'][starterId]
#     count += firstRelation['distanceBetween']
#     for kill in copied.keys():
#         for j in copied.keys():
#             kill['connectedNodes'][starterId]['visited'][j] = True
#     ogCount = count
#     dfs(copied, copied[key], ogCount)
#     if worst == None or count > worst:
#         worst = count
#     if best == None or count < best:
#         best = count
#     count = 0

combos = {}
permutation = permutations(list(nodes.keys())[1:], len(nodes.keys()) - 1)
index = 0
for comb in permutation:
    build = {'1': '1'}
    for i in range(len(comb)):
        build[str(comb[i])] = str(comb[i])
    combos[index] = build
    index += 1

print(nodes)
# print(range(len(combos.keys())))
counts = []
for i in range(len(combos.keys())):
    count = 0
    print(combos[i].keys())
    indexCount = 0
    for key in combos[i].keys():
        nextIndex = list(combos[i].keys()).index(key) + 1
        #  in nodes[int(key)]['connectedNodes']
        if len(list(combos[i])) > nextIndex:
            print(len(list(combos[i])))
            print(nextIndex)
            # print(nodes[int(key)]['connectedNodes'])
            count += nodes[int(key)]['connectedNodes'][int(list(combos[i])[nextIndex])]['distanceBetween']
        indexCount += 1
    counts.append(count)

print(counts)
best = None
worst = None
for count in counts:
    if best == None or count < best:
        best = count
    if worst == None or count > worst:
        worst = count


print('Best case: ', best)
print('Worst case: ', worst)
plt.show()
