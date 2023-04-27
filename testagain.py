import math

def quadraticFormula(a, b, c):
    bSquared = b ** 2
    fourAc = 4 * a * c
    squareThis = bSquared - fourAc
    if squareThis < 0:
        print(squareThis)
        return 'NO REAL SOLUTIONS'
    else:
        print(squareThis)
        squarRootValue = math.sqrt(squareThis)
        x1 = (-1 * b + squarRootValue) / (2 * a)
        x2 = (-1 * b - squarRootValue) / (2 * a)
        return [x1, x2]
      

def checkDistance(coords1, coords2):
    x1 = coords1[0]
    y1= coords1[1]

    x2 = coords2[0]
    y2 = coords2[1]
    a = (x2 - x1) ** 2
    b = (y2 - y1) ** 2

    sum = a + b
    result = math.sqrt(sum)
    return result

def findNextAnchor():
    dist = 6.89
    randomPoint_X = round(dist / 2, 3)

    x2 = randomPoint_X
    y2 = dist / (x2 ** 2)

    return [x2, y2]

point1 = [0,0]
point2 = findNextAnchor()
# From 1 to 3
dist1 = 5.07

# From 2 to 3
dist2 = 7.8

def findPointGivenTwoPoints(point1, distance1, point2, distance2):
    valX_1 = point1[0]
    valY_1 = point1[1]

    valX_2 = point2[0]
    valY_2 = point2[1]

    foiledX = -2 * valX_2
    valSquared_X = valX_2 ** 2

    foiledY = -2 * valY_2
    valSquared_Y = valY_2 ** 2

    dist1Squared = distance1 ** 2
    dist2Squared = distance2 ** 2


    sumOfSquaredValues = valSquared_X + valSquared_Y - dist2Squared + dist1Squared

    foiledXSquared = foiledX ** 2

    foiledYSquared = foiledY ** 2


    dist_1_times_foiledYSquared = foiledYSquared * dist1Squared

    b = (foiledX * sumOfSquaredValues) + (foiledX * sumOfSquaredValues)

    sumOfSquaredValuesSquared = sumOfSquaredValues ** 2    


    # Simplifying and all to one side
    a = foiledXSquared + foiledYSquared

    c = sumOfSquaredValuesSquared - dist_1_times_foiledYSquared
    bothXValues = quadraticFormula(a, b, c)

    for x in bothXValues:
        y = math.sqrt(dist1Squared - (x ** 2))
        checkDistance([x, y], point1)
        checkDistance([x, y], point2)

findPointGivenTwoPoints(point1, dist1, point2, dist2)
