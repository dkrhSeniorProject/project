import matplotlib.pyplot as plt
from random import randint

class ScatterSet:
	hl = None
	def update_set(self, xcoord, ycoord):
		self.hl.set_xdata(xcoord)
		self.hl.set_ydata(ycoord)
	def __init__(self, icon):
		self.hl, = plt.plot([], [], icon)

class Map:
	fig = None
	scatter = None
	def __init__(self, xmin=0, xmax=10, ymin=0, ymax=10, windowWidth=10, windowHeight=10):
		plt.ion() # interactive mode, allows updating of map using draw()
		self.fig = plt.figure(num=None, figsize=(windowWidth, windowHeight), dpi=80, facecolor='w', edgecolor='k')
		ax = self.fig.add_subplot(111)
		plt.axis([xmin, xmax, ymin, ymax])
		self.scatter = {}
	def newScatter(self, name, icon):
		newScat = ScatterSet(icon)
		if(name in self.scatter):
			print("ScatterSet named " + name + " already exists.")
		else:
			self.scatter[name] = newScat
		return self.scatter[name]
	def printScatter(self):
		print("Names of ScatterSets in scatter:")
		for entry in self.scatter:
			print(entry)
			
y = Map(xmin=0, xmax=9, ymin=0, ymax=9, windowWidth=6, windowHeight=6) # create a map object
y.newScatter('red', 'ro') # create a scatterplot set called 'red' with red circles as markers ('ro')
y.scatter['red'].update_set([1],[1]) # set xy coordinates (1,1) for entries in 'red'
y.newScatter('blue', 'bo')
y.scatter['blue'].update_set([2],[2])

y.printScatter() # prints the names of the scatterplot sets
y.fig.canvas.draw() # each time this is called, the plot is redrawn
print("Press enter to continue.")
raw_input()
####
y.scatter['red'].update_set([1, 2, 3], [1, 4, 9])
y.scatter['blue'].update_set([1.5, 2.5, 3.5], [3, 5, 7])
y.newScatter('green', 'go')
y.scatter['green'].update_set([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5])

y.printScatter()
y.fig.canvas.draw()
print("Press enter to exit.")
raw_input()
