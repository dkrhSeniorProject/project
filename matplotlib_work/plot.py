import matplotlib.pyplot as plt
from random import randint

def update_line(hl, new_data):
    hl.set_xdata(1)
    hl.set_ydata(new_data)
    plt.draw()
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
plt.axis([0,2, 0, 11])
hl, = plt.plot([1], [randint(1,10)], 'ro')
plt.ylabel('some numbers')
while 1 :
	update_line(hl, randint(1,10))
	fig.canvas.draw()
