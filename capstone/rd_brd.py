import serial, signal, sys, os
from collections import defaultdict
from time import sleep

class mobile_node:						#routers
	def __init__(self,mac):
		self.zeds = defaultdict(list)			#using the node's mac address for ID
		self.zeds[mac] = []									#keep track of LQI values

class network:
	def __init__(self, port = "COM4"):
		self.members = {}			#contains members of the dict (nodes/routers)
		self.num_routers = 0
		self.ser = serial.Serial(port,baudrate=9600,stopbits=1,timeout=1,xonxoff=0);
	#	signal.signal(signal.SIGINT, self.signal_handler)		#call my handler

	
	def add_router(self,rmac,edmac):		#add router to members dictionary
		for key in self.members:
			if key == rmac:	#node is already present
				return
		#print "Adding new router"
		self.members[rmac] = mobile_node(edmac)		#create new entry
		self.num_routers += 1
		return

	def update(self,rmac,edmac,lqi):
		self.add_router(rmac,edmac)
		for k in self.members:
			if k == rmac:	#node to be updated	
				self.members[k].zeds[edmac].append(lqi)

	def parse_packet(self,data):
		mac = self.get_mac_and_lqi(data)
	#	print "Got: ", mac
		if len(mac)%3 == 0:
			return mac
		return []

	def get_mac_and_lqi(self,data):
	#	print "parsing: .....", data, "\n..........."
		mac = []
		for string in data:
		#	print "..",string
		#	if str(string[0:4]) == "From":
		#		if len(string[5:-7]) == 23:
		#			mac.append(str(string[5:-7]))		#add end device mac
			if str(string[0:7]) == "RouterF":	#RFM
				continue	 		#go to next thing
			if str(string[0:8]) == "Router h":
			#	print "RFM", string[-23:]
			#	print "Mac search", string[-23:]
				if len(string[37:]) == 23:	#should never fail .. but it does
			#		print "dafuq ",string[37:]
					mac.append(str(string[37:]))			#add router
					continue
				else:
					mac.append(str(string[-23:])) 
			#	print "Hehe: ", string[0:7]
			if str(string[0:7]) == "Sheader":
			#	print "dafuq2 : ",string[30:]
				if len(string[-30:]) == 23:					#get end device
					mac.append(str(string[-23:]))
					continue
				else:
			#		print "using alternative method"
					mac.append(str(string[-23:]))
					continue 	
			#get Slqi
			if str(string[0:4]) == 'Slqi':			#if something was found, spit it out
			#	print "Got lqi", string[-2:]
				mac.append(str(string[-2:]))
	#	print mac
		return mac			#return mac found

	def print_data(self):
		print "\nRouter mac\t\t\tZED\t\t\tLQI values",
		for k in self.members:
			print "\n",k,"\t",
			for zkey in self.members[k].zeds:				#print zed mac
				print zkey,"\t",
				for lqi in self.members[k].zeds[zkey]:
					print lqi,",",
				print "\n.\t\t\t\t\t"	
		print "\n"


	def signal_handler(self,signal,frame):
		self.print_data()		#print out data so far
		print "Terminating..."
		self.ser.flush()
		self.ser.close()		#close serial port
		sys.exit()


if __name__ == '__main__':

	stalk_net= network("COM4")   				#create new network

	print "Data collection in progress .",
	sleep(1)		#board freaks out when you try to read too fast at first
	line = stalk_net.ser.readline()			#read a line
	while True: 
		if (len(line) > 0) and (str(line[0:4]) == "From"):
			print "Head beginner"
			line = stalk_net.ser.readline()			#read next line
			data = []			#create data packet
			while str(line[0:4]) != "From":			#loop until next "From:" line
				if line.strip() != "":
					data.append(line.strip())
				line = stalk_net.ser.readline()			#read next line
			
			if (len(data) > 0) and (data != '\n'):		#parse and update
				print ".",
				info = stalk_net.parse_packet(data)
			#	print info
				if len(info)%3 == 0: 				#only update if we have macs & lqi data
					for i in range(0,len(info)/3):
						stalk_net.update(info[3*i],info[3*i+1],info[3*i+2])
		else:
			line = 	stalk_net.ser.readline()			#read a line and proceed
		sleep(0.1)			#longer sleep times will give you enough time to read the whole packet



