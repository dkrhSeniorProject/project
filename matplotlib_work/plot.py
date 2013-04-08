import matplotlib.pyplot as plt
from random import randint

def update_line(hl, xcoord, ycoord):
    hl.set_xdata(xcoord)
    hl.set_ydata(ycoord)
    plt.draw()
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
plt.axis([0,10, 0, 10])
hl, = plt.plot([1], [randint(1,10)], 'ro')
plt.ylabel('some numbers')

while 1 :
	update_line(hl, randint(1,10), randint(1,10))
	fig.canvas.draw()
