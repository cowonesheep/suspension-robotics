"""
Welcome to the CDPR known as Mariette.
Produced by: Philip Andress
Fall 2021
"""
# Libraries
import math as m
import numpy as np
import matplotlib.pyplot as plt

# Variables
length = [0, 0, 0, 0, 0, 0, 0, 0]
pulley = [[100, -100, 100], [-100, 100, 90],
          [100, 100, 90], [-100, -100, 100],
          [100, 100, 100], [-100, -100, 90],
          [100, -100, 90], [-100, 100, 100]]
boxDim = [20, 20, 10]


# Function that takes user input and routes them to various control functions
def menu():
    ans = True
    print("Welcome to Mariette's Menu.\n")
    # menu repeats forever until you set the answer to false
    while ans:
        print("What would you like to do?")
        print("""
        1.Run Zeroing Protocol
        2.Run Input Graph Test
        3.Run Push Control 
        4.Run Planned Control
        5.Exit/Quit
        """)
        # Read in the user input and execute if statements accordingly
        ans = input(":")
        if ans == "1":
            print("\nRunning Zeroing Protocol...\n")
            zero()
        elif ans == "2":
            print("\nRunning Input Graph Test\n")
            input_test()

        elif ans == "3":
            print("\nRunning Push Control...\n")
        elif ans == "4":
            print("\nRunning Planned Control...\n")
        elif ans == "5":
            print("\nWhat’s the matter, don’t like real girls? Ending Menu.\n")
            break
        elif ans != "":
            print("\nNot Valid Choice Try again guy eating noodles\n")


def zero():
    print("""
    Welcome to the zeroing protocol.
    This is going to work by having you cycle through a four loop reeling
    in each cable until the length = zero.
    """)
    for x in length:
        print(x)


def input_test():
    desPos = [0, 0, 0]
    desOri = [0, 0, 0]
    desPos[0] = float(input("What is the initial X"))
    desPos[1] = float(input("What is the initial Y"))
    desPos[2] = float(input("What is the initial Z"))
    desOri[0] = m.pi * float(input("What is the rotation of X roll")) / 180
    desOri[1] = m.pi * float(input("What is the rotation of Y pitch")) / 180
    desOri[2] = m.pi * float(input("What is the rotation of Z yaw")) / 180
    renderBox(desPos, desOri, boxDim)
    #    question？


def renderBox(desPos, desOri, boxDim):
    # Assigns starting positions of the box corners before we rotate or shift
    boxPoint = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    boxPoint[0] = [boxDim[0] / 2, boxDim[1] / 2, boxDim[2] / 2]
    boxPoint[1] = [boxDim[0] / 2, boxDim[1] / 2, -boxDim[2] / 2]
    boxPoint[2] = [boxDim[0] / 2, -boxDim[1] / 2, -boxDim[2] / 2]
    boxPoint[3] = [boxDim[0] / 2, -boxDim[1] / 2, boxDim[2] / 2]
    boxPoint[4] = [-boxDim[0] / 2, boxDim[1] / 2, boxDim[2] / 2]
    boxPoint[5] = [-boxDim[0] / 2, boxDim[1] / 2, -boxDim[2] / 2]
    boxPoint[6] = [-boxDim[0] / 2, -boxDim[1] / 2, -boxDim[2] / 2]
    boxPoint[7] = [-boxDim[0] / 2, -boxDim[1] / 2, boxDim[2] / 2]

    spin(boxPoint, desOri)
    shift(boxPoint, desPos)
    graphBox(boxPoint)


def spin(boxPoint, desOri):  # This works fine unless you use multiple of them... What is that about?
    result = [[0], [0], [0]]
    row = desOri[0]
    pitch = desOri[1]
    yaw = desOri[2]
    rotation = [[m.cos(pitch) * m.cos(yaw),
                 -m.cos(row) * m.sin(yaw) + m.sin(row) * m.sin(pitch) * m.cos(yaw),
                 m.sin(row) * m.sin(yaw) + m.cos(row) * m.sin(pitch) * m.cos(yaw)],
                [m.cos(pitch) * m.sin(yaw),
                 m.cos(row) * m.cos(yaw) + m.sin(row) * m.sin(pitch) * m.sin(yaw),
                 -m.sin(row) * m.cos(yaw) + m.cos(row) * m.sin(pitch) * m.sin(yaw)],
                [-m.sin(pitch),
                 m.sin(row) * m.cos(pitch),
                 m.cos(row) * m.cos(pitch)]]
    for f in range(len(boxPoint)):
        result = [[0], [0], [0]]
        permit = boxPoint[f]
        cal_box = [[0], [0], [0]]
        print(cal_box)
        print(boxPoint[f])
        for i in range(len(permit)):
            cal_box [i][0] = permit [i]
        print(cal_box)
        for i in range(len(rotation)):
            for j in range(len(cal_box[0])):
                for k in range(len(cal_box)):
                    result[i][j] += rotation[i][k] * cal_box[k][j]
        for r in result:
            print(r)
        for i in range(len(cal_box)):
            cal_box[i] = result[i]
        boxPoint[f] = cal_box
        print("")


def shift(boxPoint, desPos):
    for i in range(len(boxPoint)):
        for j in range(3):
            boxPoint[i][j] += desPos[j]


def printBox(boxPoint):
    for i in range(len(boxPoint)):
        print(boxPoint[i])
        print()
        # why two print


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

    ax.scatter(0, 0, 0, 'o', color='green')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()


menu()
