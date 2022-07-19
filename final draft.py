import math as m
import numpy as n
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import style

def main():
    # the propose of this program is to find a skew line(neither intersect nor parallo)
    # should input xi,yi,zi,xt,yt,zt as intial point and end point
    line1 = input("Where is the first line\n").split(",")
    line2 = input("Where is the second line\n").split(",")
    line1 = [ float(x) for x in line1 ]
    line2 = [ float(x) for x in line2 ]
    line1int = line1[:3]
    line1end = line1[3:]
    line2int = line2[:3]
    line2end = line2[3:]
    # find the vector of start point
    differece = paramt(line1int, line2int)#w0
    # parametrize the line
    b1 = paramt(line1int, line1end)#u
    b2 = paramt(line2int, line2end)#v
    product = n.cross(b1,b2)
    numerator = n.dot(differece,product)
    denuminator = rlength(product)
    length = numerator/ denuminator
    print(length)

    # then calculate the shortest point
    a = n.dot(b1,b1)
    b = n.dot(b1,b2)
    c = n.dot(b2, b2)
    d = n.dot(b1, differece)
    e = n.dot(b2, differece)

    c1,c2 = closest_line_seg_line_seg(b1, b2, differece)

    #find point
    point1=[]
    point2=[]
    for i in range(len(b1)):
        point1.append(line1int[i] + c1 * b1[i])
        point2.append(line2int[i] + c2 * b2[i])
    print(point1)
    print(point2)
    drawing(line1int, line2int, line1end, line2end, point1, point2)



def find_point(a,b,c,d,e):
    c1 = (b * e - c * d)/(a * c - b ** 2)
    c2 = (a * e - b * d) / (a * c - b ** 2)
    return c1,c2 # return to constant


def paramt(start, end):
    #input start point and endpoint, return vector between in list
    vector = []
    for i in range(len(start)):
        vector.append(end[i]-start[i])
    return vector

def rlength(list):
    #input a list of number and return their square root sum
    sqaure = 0
    for element in list:
        sqaure = sqaure + element ** 2
    sqaure = sqaure ** 0.5
    return sqaure

def drawing(line1int,line2int,line1end,line2end,point1,point2):
    style.use('ggplot')
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    line1 = create_line_range(line1int,line1end)
    line2 = create_line_range(line2int,line2end)
    line3 = create_line_range(point1,point2)
    ax1.plot(line1[0], line1[1], line1[2], color='black')
    ax1.plot(line2[0], line2[1], line2[2], color='black')
    ax1.plot(line3[0], line3[1], line3[2], color='red')
    plt.show()

def create_line_range(start,end):
    line = []
    for i in range(len(start)):
        line.append([start[i],end[i]])
    return line


def closest_line_seg_line_seg(V1, V2, V21, ):
    v22 = n.dot(V2, V2)
    v11 = n.dot(V1, V1)
    v21 = n.dot(V2, V1)
    v21_1 = n.dot(V21, V1)
    v21_2 = n.dot(V21, V2)
    denom = v21 * v21 - v22 * v11

    if n.isclose(denom, 0.):
        s = 0.
        t = (v11 * s - v21_1) / v21
    else:
        s = (v21_2 * v21 - v22 * v21_1) / denom
        t = (-v21_1 * v21 + v11 * v21_2) / denom

    s = max(min(s, 1.), 0.)
    t = max(min(t, 1.), 0.)
    return s,t








main()