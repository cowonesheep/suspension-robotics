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



Inpoint=np.array([0,0,0])
Endpoint=np.array([500,500,500])
t = 0
x = 0
y = 0
z = 0
point = ax.plot([0], [0], [0], 'o')
fig.set_size_inches(5, 5)


# parametrize a given line
def para():
    global x,y,z,t,point
    t = np.arange(0,100,.05)
    x = Inpoint[0]+t*(Endpoint[0]-Inpoint[0])
    y = Inpoint[1] + t * (Endpoint[1]-Inpoint[1] )
    z = Inpoint[2] + t * ( Endpoint[2]-Inpoint[2])
    point, = ax.plot([x[0]], [y[0]], [z[0]], 'o')


def update_point(n, x, y, z, point):
    point.set_data(np.array([x[n], y[n]]))
    point.set_3d_properties(z[n], 'z')
    return point


para()
ani=animation.FuncAnimation(fig, update_point, 99, fargs=(x, y, z, point))
plt.show()