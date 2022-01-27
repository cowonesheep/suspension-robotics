import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
fig.subplots_adjust(left=0, bottom=0, right=1, top=1)
ax = fig.add_subplot(111, projection='3d')
ax.axes.set_xlim3d(left=0, right=8000)
# Range
ax.axes.set_ylim3d(bottom=0, top=4000)
ax.axes.set_zlim3d(bottom=0, top=2000)
ax.set_box_aspect((4, 2, 1))
ax.set_facecolor((0.5, 0.5, 0.5))
gradient = np.linspace(0, 1, 2)
X,Y,Z = np.meshgrid(gradient, gradient, gradient)
colors=np.stack((X.flatten(),Y.flatten(),Z.flatten()),axis=1)
# above are graphing
Inpoint=np.array([0,0,0]) # input
Endpoint=np.array([500,500,500]) # output
boxDim = np.array([200, 200, 200])
t = 0
x = 0
y = 0
z = 0
Box = 0
fig.set_size_inches(5, 5)

# parametrize the path
def para():
    global x,y,z,t,point,Box1,Box2,Box3,Box4,Box5,Box6,Box7,Box8
    t = np.arange(0,1,.1)
    x = Inpoint[0] + t * (Endpoint[0]-Inpoint[0])
    y = Inpoint[1] + t * (Endpoint[1]-Inpoint[1] )
    z = Inpoint[2] + t * (Endpoint[2]-Inpoint[2])
    Box1, = ax.plot([x[0]], [y[0]], [z[0]], 'o', color='red')
    Box2, = ax.plot([x[0]], [y[0]], [z[0]], 'o', color='red')
    Box3, = ax.plot([x[0]], [y[0]], [z[0]], 'o', color='red')
    Box4, = ax.plot([x[0]], [y[0]], [z[0]], 'o', color='red')
    Box5, = ax.plot([x[0]], [y[0]], [z[0]], 'o', color='red')
    Box6, = ax.plot([x[0]], [y[0]], [z[0]], 'o', color='red')
    Box7, = ax.plot([x[0]], [y[0]], [z[0]], 'o', color='red')
    Box8, = ax.plot([x[0]], [y[0]], [z[0]], 'o', color='red')
    point, = ax.plot([x[0]], [y[0]], [z[0]], 'o', color='green')
    print(Box1)
# point update
def update_point(n, x, y, z, point,Box1,Box2,Box3,Box4,Box5,Box6,Box7,Box8):
    point.set_data(np.array([x[n], y[n]]))
    point.set_3d_properties(z[n], 'z')
    Box1.set_data(np.array([x[n] + boxPoint[0][0], y[n] + boxPoint[0][1]]))
    Box1.set_3d_properties(z[n] + boxPoint[0][2], 'z')
    Box2.set_data(np.array([x[n] + boxPoint[1][0], y[n] + boxPoint[1][1]]))
    Box2.set_3d_properties(z[n] + boxPoint[1][2], 'z')
    Box3.set_data(np.array([x[n] + boxPoint[2][0], y[n] + boxPoint[2][1]]))
    Box3.set_3d_properties(z[n] + boxPoint[2][2], 'z')
    Box4.set_data(np.array([x[n] + boxPoint[3][0], y[n] + boxPoint[3][1]]))
    Box4.set_3d_properties(z[n] + boxPoint[3][2], 'z')
    Box5.set_data(np.array([x[n] + boxPoint[4][0], y[n] + boxPoint[4][1]]))
    Box5.set_3d_properties(z[n] + boxPoint[4][2], 'z')
    Box6.set_data(np.array([x[n] + boxPoint[5][0], y[n] + boxPoint[5][1]]))
    Box6.set_3d_properties(z[n] + boxPoint[5][2], 'z')
    Box7.set_data(np.array([x[n] + boxPoint[6][0], y[n] + boxPoint[6][1]]))
    Box7.set_3d_properties(z[n] + boxPoint[6][2], 'z')
    Box8.set_data(np.array([x[n] + boxPoint[7][0], y[n] + boxPoint[7][1]]))
    Box8.set_3d_properties(z[n] + boxPoint[7][2], 'z')
    return point,Box1,Box2,Box3,Box4,Box5,Box6,Box7,Box8

def coord2box(desPos, desOri):
    # Setup
    global boxPoint
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
coord2box(0,0)
print (boxPoint)
para()
ani=animation.FuncAnimation(fig,
                            update_point,
                            10,
                            fargs=(x, y, z, point, Box1,Box2,Box3,Box4,Box5,Box6,Box7,Box8),
                            interval=50,
                            repeat=False)
plt.show()