import numpy as np
import math
X=int(input("What is the intial X"))
Y=int(input("What is the intial Y"))
Z=int(input("What is the intial Z"))
row=int(input("What is the rotation of X"))
pitch=int(input("What is the rotation of Y"))
yaw=int(input("What is the rotation of Z"))


array2=[[Z],[Y],[X]]
array1=[[math.cos(pitch)*math.cos(row),math.cos(yaw)*math.sin(row)+math.sin(yaw)*math.sin(pitch)*math.cos(row),math.sin(yaw)*math.sin(row)-math.cos(yaw)*math.sin(pitch)*math.cos(row)],\
        [-math.cos(pitch)*math.sin(row),math.cos(yaw)*math.cos(row)-math.sin(yaw)*math.sin(pitch)*math.sin(row),math.sin(yaw)*math.cos(row)+math.cos(yaw)*math.sin(pitch)*math.sin(row)],\
        [math.sin(pitch),-math.sin(yaw)*math.cos(pitch),math.cos(yaw)*math.cos(pitch)]]
result=[[0],[0],[0]]
for i in range(len(array1)):
    for j in range(len(array2[0])):
        for k in range(len(array2)):
            result[i][j] += array1[i][k]* array2[k][j]           
for r in result:
    print(r)



