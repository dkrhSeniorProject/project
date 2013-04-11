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
	def closeWindow(self):
		plt.close(self.fig)

x = Map()
raw_input()
x.closeWindow()
raw_input()
