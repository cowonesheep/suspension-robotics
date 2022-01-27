"""
Welcome to the CDPR known as Mariette.
Produced by: Suspension Robotics
Fall 2021
"""

# Libraries
import math as m
import numpy as np
import matplotlib.pyplot as plt

# Constants xyz (z is vertical)
pulley = np.array([[8000, 0, 2000], [0, 4000, 1900],
                   [8000, 4000, 1900], [0, 0, 2000],
                   [8000, 4000, 2000], [0, 0, 1900],
                   [8000, 0, 1900], [0, 4000, 2000]])
boxDim = np.array([200, 200, 200])


# Function that takes in XYZ & RPY of box and returns the coords of the eight corners
def coord2box(desPos, desOri):
    # Setup
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


# Function that takes in XYZ & RPY of current and desired and makes a discrete linear path of box center points
def breadCrumb(curPos, desPos, curOri, desOri, numDots):
    # Setup
    path = np.zeros((numDots + 1, 3))
    view = np.zeros((numDots + 1, 3))
    # Calculate deltas given number of dots
    deltaXYZ = np.subtract(desPos, curPos) / numDots
    deltaRPY = np.subtract(desOri, curOri) / numDots
    # Initial
    path[0] = curPos
    view[0] = curOri
    # Body
    for i in range(numDots):
        for j in range(len(path[i])):
            path[i + 1][j] = (i + 1) * deltaXYZ[j] + path[0][j]
            view[i + 1][j] = (i + 1) * deltaRPY[j] + view[0][j]
    return path, view


# Function that takes the aforementioned linear path and computes the boxpoints associated with it
def breadBox(path, view):
    # Setup
    boxPath = np.zeros((len(path), 8, 3))
    # Loop
    for i in range(len(path)):
        boxPath[i] = coord2box(path[i], view[i])
    return boxPath


# Function that graphs all discrete stops for the box along linear path
def graphBoxes(boxes):
    # Setup
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.axes.set_xlim3d(left=0, right=8000)
    # Range
    ax.axes.set_ylim3d(bottom=0, top=4000)
    ax.axes.set_zlim3d(bottom=0, top=2000)
    # Aspect Ratio
    ax.set_box_aspect((4, 2, 1))
    # Ticks and Grid
    ax.set_xticks(np.arange(0, 8001, 2000))
    ax.set_xticks(np.arange(0, 8001, 500), minor=True)
    ax.set_yticks(np.arange(0, 4001, 2000))
    ax.set_yticks(np.arange(0, 4001, 500), minor=True)
    ax.set_zticks(np.arange(0, 2001, 1000))
    ax.set_zticks(np.arange(0, 2001, 500), minor=True)
    ax.grid(which='both')
    # Plot
    for i in range(8):  # Pulleys
        ax.scatter(pulley[i][0], pulley[i][1], pulley[i][2], 'o', color='green')
    for i in range(len(boxes)):  # Boxes
        for j in range(8):
            ax.scatter(boxes[i][j][0], boxes[i][j][1], boxes[i][j][2], 'o', s=3, color='red')
    for i in range(len(boxes)):  # Cables
        for j in range(8):
            xLine = np.linspace(pulley[j][0], boxes[i][j][0])
            yLine = np.linspace(pulley[j][1], boxes[i][j][1])
            zLine = np.linspace(pulley[j][2], boxes[i][j][2])
            plt.plot(xLine, yLine, zLine, linewidth=0.5, color='grey')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


# Function that calculates the distance between any two points in 3D space
def p2plength(a, b):
    length = m.sqrt(((a[0] - b[0]) ** 2) +
                    ((a[1] - b[1]) ** 2) +
                    ((a[2] - b[2]) ** 2))
    return length


# Function that calculates the cable deltas needed given a breadbox path
def breadCableDelta(boxPath):  # What is a bread cable if not spaghetti?
    # Setup
    cablePath = np.zeros((len(boxPath), 8))
    cablePathDelta = np.zeros((len(boxPath) - 1, 8))
    # Cable Lengths at each dot
    for i in range(len(boxPath)):
        for j in range(len(boxPath[i])):
            cablePath[i][j] = p2plength(boxPath[i][j], pulley[j])
    # Delta Cable length between each dot
    for i in range(len(boxPath[0])):
        column = cablePath[:, i]
        cablePathDelta[:, i] = np.diff(column)
    return cablePathDelta


# Test values
desPos = [7000, 2000, 100]
desOri = [0, 0, 0]
curPos = [1000, 2000, 1900]
curOri = [0, 0, 0]
# Conversion
for i in range(len(desOri)):
    desOri[i] = desOri[i] * m.pi / 180
    curOri[i] = curOri[i] * m.pi / 180
# Other
numDots = 3
# Call the funcs
breadPath, breadView = breadCrumb(curPos, desPos, curOri, desOri, numDots)
breadCableDelta(breadBox(breadPath, breadView))
graphBoxes(breadBox(breadPath, breadView))
