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
pulley = np.array([[0, 0, 2000], [0, 0, 1900],
                   [8000, 0, 1900], [8000, 0, 2000],
                   [0, 4000, 2000], [0, 4000, 1900],
                   [8000, 4000, 1900], [8000, 4000, 2000]])
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
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


# Test values
desPos = [7800, 200, 200]
desOri = [0, 45, 0]
curPos = [200, 3800, 1800]
curOri = [0, 0, 0]
# Conversion
for i in range(len(desOri)):
    desOri[i] = desOri[i] * m.pi / 180
    curOri[i] = curOri[i] * m.pi / 180
# Other
duration = 20
numDots = 10
# Call the funcs
breadPath, breadView = breadCrumb(curPos, desPos, curOri, desOri, numDots)
graphBoxes(breadBox(breadPath, breadView))