import matplotlib.pyplot as plt
import os
Xframe=int(input("What is the width of the frame"))
Yframe=int(input("What is the height of the frame"))
Xi=int(input("What is the X"))
Yi=int(input("What is the Y"))
fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax1.set(xlim=[0, Xframe], ylim=[0, Yframe], title='Previous',
       ylabel='Y-Axis', xlabel='X-Axis')
ax2.set(xlim=[0, Xframe], ylim=[0, Yframe], title='Now',
       ylabel='', xlabel='X-Axis')
ax2.plot([0,Xi],[Xframe,Yi])
ax2.plot([Xi,Xframe],[Yi,Yframe])
plt.show()



def drawline():
 global Xn
 global Yn
 global Xi
 global Yi
 Xn=int(input("What is the new X"))
 Yn=int(input("What is the new Y"))
 plt.figure()
 fig =plt.figure()
 ax1 = fig.add_subplot(221)
 ax2 = fig.add_subplot(222)
 ax1.set(xlim=[0, Xframe], ylim=[0, Yframe], title='Previous',
       ylabel='Y-Axis', xlabel='X-Axis')
 ax2.set(xlim=[0, Xframe], ylim=[0, Yframe], title='Now',
       ylabel='', xlabel='X-Axis')
 ax1.plot([0,Xi],[Xframe,Yi])
 ax1.plot([Xi,Xframe],[Yi,Yframe])
 Xi=Xn
 Yi=Yn
 ax2.plot([0,Xn],[Xframe,Yn])
 ax2.plot([Xn,Xframe],[Yn,Yframe])
 plt.show()

while (Xi>-1):
    
 drawline()

