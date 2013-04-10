import matplotlib.pyplot as plt
from random import randint

# run plot_init() once, then plug in xy coords as arrays into update_plot

class ScatterSet:
	hl = None
	fig = None

	def update_set(self, xcoord, ycoord):
		self.hl.set_xdata(xcoord)
		self.hl.set_ydata(ycoord)
		plt.draw()

	def __init__(self):
		plt.ion() # interactive mode, allows updating of map using draw()
		self.fig = plt.figure()
		ax = self.fig.add_subplot(111)
		plt.axis([0,10,0,10])
		hl, = plt.plot([], [], 'ro')

x = ScatterSet()
x.update_set([1],[1])
plt.show()
