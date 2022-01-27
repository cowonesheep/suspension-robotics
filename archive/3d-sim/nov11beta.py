"""
Welcome to the CDPR known as Mariette.
Produced by: Philip Andress and Liu 'Franko' Yiyang
Fall 2021
"""
# Libraries
import math as m
import numpy as np
import matplotlib.pyplot as plt

# Constants
pulley = np.array([[100, -100, 100], [-100, 100, 90],
                   [100, 100, 90], [-100, -100, 100],
                   [100, 100, 100], [-100, -100, 90],
                   [100, -100, 90], [-100, 100, 100]])
boxDim = np.array([20, 20, 20])
resolution = 100  # mm


# Function that takes in desired position and orientation of box and returns the coords of the eight corners
def coord2box(desPos, desOri):
    # Blank 2D arrays to work with
    boxPoint = np.zeros((8, 3))
    newboxPoint = np.zeros((8, 3))

    # Assigns starting positions of the box corners before we rotate or shift
    boxPoint[0] = [boxDim[0] / 2, boxDim[1] / 2, boxDim[2] / 2]
    boxPoint[1] = [boxDim[0] / 2, boxDim[1] / 2, -boxDim[2] / 2]
    boxPoint[2] = [boxDim[0] / 2, -boxDim[1] / 2, -boxDim[2] / 2]
    boxPoint[3] = [boxDim[0] / 2, -boxDim[1] / 2, boxDim[2] / 2]
    boxPoint[4] = [-boxDim[0] / 2, boxDim[1] / 2, boxDim[2] / 2]
    boxPoint[5] = [-boxDim[0] / 2, boxDim[1] / 2, -boxDim[2] / 2]
    boxPoint[6] = [-boxDim[0] / 2, -boxDim[1] / 2, -boxDim[2] / 2]
    boxPoint[7] = [-boxDim[0] / 2, -boxDim[1] / 2, boxDim[2] / 2]

    # rotational matrix respect to (0,0,0)
    rotMat = np.array([[m.cos(desOri[1]) * m.cos(desOri[2]),
                        -m.cos(desOri[0]) * m.sin(desOri[2]) + m.sin(desOri[0]) * m.sin(desOri[1]) * m.cos(desOri[2]),
                        m.sin(desOri[0]) * m.sin(desOri[2]) + m.cos(desOri[0]) * m.sin(desOri[1]) * m.cos(desOri[2])],
                       [m.cos(desOri[1]) * m.sin(desOri[2]),
                        m.cos(desOri[0]) * m.cos(desOri[2]) + m.sin(desOri[0]) * m.sin(desOri[1]) * m.sin(desOri[2]),
                        -m.sin(desOri[0]) * m.cos(desOri[2]) + m.cos(desOri[0]) * m.sin(desOri[1]) * m.sin(desOri[2])],
                       [-m.sin(desOri[1]),
                        m.sin(desOri[0]) * m.cos(desOri[1]),
                        m.cos(desOri[0]) * m.cos(desOri[1])]])

    # Matrix Multiplication (numpy is for wimps)
    for i in range(len(boxPoint)):  # Iterate through the eight points
        for j in range(len(boxPoint[i])):  # Iterate through xyz
            newboxPoint[i][j] = boxPoint[i][0] * rotMat[j][0] + boxPoint[i][1] * rotMat[j][1] + boxPoint[i][2] * \
                                rotMat[j][2]
    boxPoint = newboxPoint

    # Shift
    for i in range(len(boxPoint)):
        for j in range(3):
            boxPoint[i][j] += desPos[j]

    return boxPoint


def box2length(boxPoint):
    length = np.zeros(8)
    for i in length:
        length[i] = m.sqrt(((boxPoint[i][0] - pulley[i][0]) ** 2) +
                           ((boxPoint[i][1] - pulley[i][1]) ** 2) +
                           ((boxPoint[i][2] - pulley[i][2]) ** 2))
    return length


def p2plength(a, b):
    length = m.sqrt(((a[0] - b[0]) ** 2) +
                    ((a[1] - b[1]) ** 2) +
                    ((a[2] - b[2]) ** 2))
    return length


def graphBox(boxPoint):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(boxPoint[0][0], boxPoint[0][1], boxPoint[0][2], 'o', color='black')
    for i in range(1, 8):
        ax.scatter(boxPoint[i][0], boxPoint[i][1], boxPoint[i][2], 'o', color='red')
    for i in range(8):
        ax.scatter(pulley[i][0], pulley[i][1], pulley[i][2], 'o', color='green')
    for i in [0, 3, 4, 7]:  # Upper cables
        xLine = np.linspace(pulley[i][0], boxPoint[i][0])
        yLine = np.linspace(pulley[i][1], boxPoint[i][1])
        zLine = np.linspace(pulley[i][2], boxPoint[i][2])
        plt.plot(xLine, yLine, zLine, color='blue')
    for i in [1, 2, 5, 6]:  # Lower Cables
        xLine = np.linspace(pulley[i][0], boxPoint[i][0])
        yLine = np.linspace(pulley[i][1], boxPoint[i][1])
        zLine = np.linspace(pulley[i][2], boxPoint[i][2])
        plt.plot(xLine, yLine, zLine, color='pink')

    ax.scatter(0, 0, -100, 'o', color='green')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()


def linearPath(curPos, curOri, desPos, desOri, duration):# respect to the center point
    deltaXYZ = np.empty
    curBox = np.zeros((8, 3))
    desBox = np.zeros((8, 3))
    outputBox = np.empty
    # Linear Distance between center of box to center of box
    deltaPosBox = m.sqrt(((desPos[0] - curPos[0]) ** 2) +
                      ((desPos[1] - curPos[1]) ** 2) +
                      ((desPos[2] - curPos[2]) ** 2))
    # each breaking down section of the path
    numDots = deltaPosBox / resolution
    # time between each point
    durationPer = duration / numDots
    # Calculate the positions of eight of boxpoints
    curBox = np.array(coord2box(curPos, curOri))# return a 8*3
    desBox = np.array(coord2box(desPos, desOri))# return a 8*3
    # Calculate the change of positions for each eight point
    for i in range(8):
        deltaXYZ = np.array((desBox[i]-curBox[i])/numDots) # return a 8*3
    for i in range(8):  # for eight cable
        curlength = m.sqrt(curBox[i][0] ** 2 + curBox[i][1] ** 2 + curBox[i][2] ** 2) # return current cable length
        Sectionmatix = np.empty# refresh for each point
        for n in range(numDots): #for each section
            deltalength = np.array(p2plength(curBox[i]+deltaXYZ[i]*(n+1),p2plength(curBox[i]+deltaXYZ[i]* n))) # change of length for each section
            Sectionmatix.append([deltalength, durationPer])# add change of length for each section and time
        outputBox.append(Sectionmatix)#return a 8*(n*[2*2]) matrix for 8 point









# Test values
desPos = [0, 0, 0]
desOri = [m.pi * 45 / 180, 0, 0]
# call the func
box = coord2box(desPos, desOri)
# print
for r in box:
    for c in r:
        print(c, end=" ")
    print()
# graph
graphBox(box)
