#!/usr/bin/env python
import matplotlib
matplotlib.use('WXAgg')

import rd_brd
import ron_map     #ron's original file
#from ron_map import Map
import os, sys, random
from time import sleep
import threading
import wx
from numpy import arange, sin, pi

rx1 = 0
ry1 = 0
rd1 = 0
rx2 = 0
ry2 = 0
rd2 = 0
rx3 = 0
ry3 = 0
rd3 = 0

class RedirectText(object):
  def __init__(self,TextCtrl):
      self.out=TextCtrl

  def write(self,string):
  #  self.out.WriteText(string)       #not thread-safe; do not use
    wx.CallAfter(self.out.AppendText,string)    #thread-safe


class bPanel(wx.Panel):
  def __init__(self, parent):
    """Constructor"""
    wx.Panel.__init__(self, parent=parent)


class MyFrame(wx.Frame):    #create new class derived from wx.Frame
  def __init__(self,portname):
    wx.Frame.__init__(self,None, wx.ID_ANY, "Real Time Asset Tracking System v1.0",size=(600,400))
    self.port = portname 
    self.xCord = 0
    self.yCord = 0    #top-level window.
    
    splitter = wx.SplitterWindow(self)
    #panel = wx.Panel(self, wx.ID_ANY)
    panel = bPanel(splitter)
    self.tpanel = bPanel(splitter)

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
        self.update_plot(random.randint(0,10),random.randint(0,10))
        line = stalk_net.ser.readline()     #read next line
        data = []     #create data packet
        while str(line[0:4]) != "From":     #loop until next "From:" line
          if line.strip() != "":
            data.append(line.strip())
          line = stalk_net.ser.readline()     #read next line
        
        if (len(data) > 0) and (data != '\n'):    #parse and update
          #if self.cbVerbose.IsChecked():
            #print "\n", data
          info = stalk_net.parse_packet(data)
        # print info
          if len(info)%3 == 0:        #only update if we have macs & lqi data
            for i in range(0,len(info)/3):
              stalk_net.update(info[3*i],info[3*i+1],info[3*i+2])
              print int(info[3*i+2],16), " , ",
          if len(info) == 9:
            #if we got all 3 data points (lqi values)
            dists = stalk_net.get_dist_from_lqi(int(info[2],16),int(info[5],16),int(info[8],16)) 
            # returns a list of the distance based on lqi
            zed_Coord = self.triangulate(rx1,ry1,rd1,rx2,ry2,rd2,rx3,ry3,rd3)            

    else:
      line =  stalk_net.ser.readline()      #read a line and proceed
  #  sleep(0.1)      #longer sleep times will give you enough time to read the whole packet
        #longer sleep times will give you enough time to read the whole packet
    #when this exits, it means someone pushed the "stop" button
    print "\nProcess stopped by user."
    stalk_net.print_data()   #print what has been collected
    stalk_net.ser.close()    #close serial connection
    print "Serial port sucesfully closed.\n"

  def triangulate(x1, y1, r1, x2, y2, r2, x3, y3, r3):
    A = -2 * x1 + 2 * x2
    B = -2 * y1 + 2 * y2
    C = -2 * x2 + 2 * x3
    D = -2 * y2 + 2 * y3
    E = r1 ** 2 - r2 ** 2 - x1 ** 2 + x2 ** 2 - y1 ** 2 + y2 ** 2
    F = r2 ** 2 - r3 ** 2 - x2 ** 2 + x3 ** 2 - y2 ** 2 + y3 ** 2

    det = A * D - B * C
    detX = E * D - B * F
    detY = A * F - E * C

    return [detX/det, detY/det]  

  def init_plot(self):
    self.y = ron_map.Map(xmin=0, xmax=9, ymin=0, ymax=9, windowWidth=6, windowHeight=6) # create a map object
    self.y.newScatter('red', 'ro') # create a scatterplot set called 'red' with red circles as markers ('ro')

  def update_plot(self,x,y):    #called when new x,y values are gotten
    self.y.scatter['red'].update_set([x],[y])   #plot the x and y cordinates
    self.y.fig.canvas.draw()    #plot

  def OnExit(self,e):
    self.Close(True)  #close frame

  def onStartBtn(self,e):
    #handling startCollect() in a separate thread so the loop doesn't stall the
    #rest of the program
    self.collect = True  #this controls whether we collect data or not
    self.t1 = threading.Thread(target=self.startCollect).start()
  #  self.t2 = threading.Thread(target=self.doPlot).start()
    self.init_plot()    #initialize plot

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
    self.y.closeWindow()

if __name__ == "__main__":
  if len(sys.argv) !=2:
    print "Wrong use! Exiting"
    sys.exit()

  app = wx.App(redirect=False)
  frame = MyFrame(sys.argv[1])
  frame.Show(True)
  app.MainLoop()
