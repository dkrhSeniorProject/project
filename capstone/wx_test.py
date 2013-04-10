#!/usr/bin/env python
import matplotlib
matplotlib.use('WXAgg')

import rd_brd
from ron_map import Map
import os, sys, random
from time import sleep
import threading
import wx
from numpy import arange, sin, pi

#from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
#from matplotlib.backends.backend_wx import NavigationToolbar2Wx
#from matplotlib.figure import Figure


class RedirectText(object):
  def __init__(self,TextCtrl):
      self.out=TextCtrl

  def write(self,string):
  #  self.out.WriteText(string)       #not thread-safe; do not use
    wx.CallAfter(self.out.AppendText,string)    #thread-safe

class t2(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self, parent)
    self.plt = Map(selfie=self,xmin=0, xmax=9, ymin=0, ymax=9, windowWidth=6, windowHeight=6) # create a map object
    self.plt.newScatter('red','ro')
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.sizer.Add(self.plt.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
    self.SetSizer(self.sizer)
    self.Fit()

  def draw(self,xcord,ycord):
    self.plt.ax.clear()
    print "X: ", xcord, "Y: ", ycord
    self.plt.ax.plot(xcord,ycord,'ro')
    self.plt.fig.canvas.draw() # each time this is called, the plot is redrawn
    

class testCanvas(wx.Panel):
  def __init__(self, parent):
    wx.Panel.__init__(self, parent)
    self.figure = Figure()
    self.axes = self.figure.add_subplot(111)
    self.canvas = FigureCanvas(self, -1, self.figure)
    self.sizer = wx.BoxSizer(wx.VERTICAL)
    self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
    self.SetSizer(self.sizer)
    self.Fit()

  def draw(self):
    self.axes.clear()
    t = arange(0.0, 3.0, 0.01)
    s = sin(2 * pi * t)
    self.axes.plot(t, s)
    self.canvas.draw()
    


class bPanel(wx.Panel):
  def __init__(self, parent):
    """Constructor"""
    wx.Panel.__init__(self, parent=parent)


class MyFrame(wx.Frame):    #create new class derived from wx.Frame
  def __init__(self,portname):
    wx.Frame.__init__(self,None, wx.ID_ANY, "In ma plums",size=(600,800))
    self.port = portname 
    self.xCord = 0
    self.yCord = 0    #top-level window.
    
    splitter = wx.SplitterWindow(self)
    #panel = wx.Panel(self, wx.ID_ANY)
    panel = bPanel(splitter)
    self.tpanel = t2(splitter)

    log = wx.TextCtrl(panel, wx.ID_ANY, size=(40,20),
                       style = wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_LINEWRAP)

    self.startBtn = wx.Button(panel, wx.ID_ANY, 'Start')
    self.stopBtn = wx.Button(panel, wx.ID_ANY, 'Stop')
    self.Bind(wx.EVT_BUTTON, self.onStartBtn, self.startBtn)
    self.Bind(wx.EVT_BUTTON, self.onStopBtn, self.stopBtn)
    
    # Add widgets to a sizer        
    sizer = wx.BoxSizer(wx.VERTICAL)        #to align everything vertically
    btn_sizer = wx.BoxSizer(wx.HORIZONTAL)  #to put buttons in same row
    sizer.Add(log, 1, wx.ALL|wx.EXPAND, 5)  #to hold the TextCtrl object
  
    #checkbox to choose whether to work in verbose mode or not
    self.cbVerbose = wx.CheckBox(panel, label = "Verbose mode")    
    
    #split window
    splitter.SplitHorizontally(panel,self.tpanel)
    splitter.SetMinimumPaneSize(200)


    siz = wx.BoxSizer(wx.VERTICAL)
    siz.Add(splitter, 1, wx.EXPAND)

   # btn_sizer.Add(vText,1,wx.ALIGN_LEFT,5) #add to vertical verbose sizer
    btn_sizer.Add(self.startBtn, 0, wx.ALL, 5)  
    btn_sizer.Add(self.stopBtn, 0, wx.ALL, 5)
    sizer.Add(self.cbVerbose,0,wx.ALL|wx.ALIGN_LEFT,10)
    sizer.Add(btn_sizer, 0, wx.ALL|wx.CENTER,5)   #adding hor(button) sizer to vert
    panel.SetSizer(sizer)         #add sizer to the panel
    self.stopBtn.Disable()       #disable the stop button on init


    #redirecting stdout to the log file
    sys.stdout = RedirectText(log)    #everything broke here .... fuck.
  

  #this function starts collecting the data from the board using rd_brd
  def startCollect(self):
    print "Creating new network instace to monitor ",self.port,"..."
    stalk_net = rd_brd.network(self.port)    #new instance
    print "New instance succesfully created.\n" \
          "Data collection in progress, click 'stop' to view results .",

    sleep(0.5)    #this sleep keeps the board from freaking out
    line = stalk_net.ser.readline()     #read a line
    
    while self.collect:
      self.xCord = random.randint(0,10);
      self.yCord = random.randint(0,10);


      if (len(line) > 0) and (str(line[0:4]) == "From"):
        print ".",
        line = stalk_net.ser.readline()     #read next line
        data = []     #create data packet
        while str(line[0:4]) != "From":     #loop until next "From:" line
          if line.strip() != "":
            data.append(line.strip())
          line = stalk_net.ser.readline()     #read next line
        
        if (len(data) > 0) and (data != '\n'):    #parse and update
          if self.cbVerbose.IsChecked():
            print "\n", data
          info = stalk_net.parse_packet(data)
        # print info
          if len(info)%3 == 0:        #only update if we have macs & lqi data
            for i in range(0,len(info)/3):
              stalk_net.update(info[3*i],info[3*i+1],info[3*i+2])
    else:
      line =  stalk_net.ser.readline()      #read a line and proceed
  #  sleep(0.1)      #longer sleep times will give you enough time to read the whole packet
        #longer sleep times will give you enough time to read the whole packet
    #when this exits, it means someone pushed the "stop" button
    print "\nProcess stopped by user."
    stalk_net.print_data()   #print what has been collected
    stalk_net.ser.close()    #close serial connection
    print "Serial port sucesfully closed.\n"

  def doPlot(self):
    print "Initializing plot"
    while self.collect:
      sleep(1)
      self.tpanel.draw(self.xCord,self.yCord)
    
  def OnExit(self,e):
    self.Close(True)  #close frame

  def onStartBtn(self,e):
    #handling startCollect() in a separate thread so the loop doesn't stall the
    #rest of the program
    self.collect = True  #this controls whether we collect data or not
    self.t1 = threading.Thread(target=self.startCollect).start()
    self.t2 = threading.Thread(target=self.doPlot).start()
    #self.t2  = threading.Thread(target=self.doPlot).start()#this thread will run the plot window
  #  self.doPlot()
    #begin the collection
  #  t1.start()
  #  self.startCollect()
  #  print "Collector thread sucesfully started"
    self.startBtn.Disable()  #hide button 1
    self.stopBtn.Enable()  #Show button 2
      
  def onStopBtn(self,e):
    self.collect = False 
  #  self.t1.join()     #wait for thread to complete before proceeding
    self.stopBtn.Disable()  #show button 2
    self.startBtn.Enable()  #show button 1


if __name__ == "__main__":
  if len(sys.argv) !=2:
    print "Wrong use! Exiting"
    sys.exit()

  app = wx.App(redirect=False)
  frame = MyFrame(sys.argv[1])
  frame.Show(True)
  app.MainLoop()
