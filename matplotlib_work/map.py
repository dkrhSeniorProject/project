import matplotlib.pyplot as plt
from random import randint

def update_plot(hl, xcoord, ycoord):
    hl.set_xdata(xcoord)
    hl.set_ydata(ycoord)
    plt.draw()

plt.ion() # interactive mode, allows updating of map using draw()

fig = plt.figure()
ax = fig.add_subplot(111)
plt.axis([0,10,0,10])

hl, = plt.plot([], [], 'ro')

while 1:
	update_plot(hl, [randint(1,10), randint(1,10)], [randint(1,10), randint(1,10)])
	fig.canvas.draw()
