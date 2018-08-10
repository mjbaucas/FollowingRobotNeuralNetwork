# Script to deliver data to server

import serial
import time
import datetime
import logging
import os
import csv

com = "NULL"
project = "NULL"
user = "NULL"

# Read config file
file = open("node.cfg")
tmpLine = file.readline()
line =  tmpLine.translate(None, " \n	").split("=")

while line[0] != "" :

	if line[0] == "com":
		com = line[1].split("#")[0]
	elif line[0] == "project":
		project = line[1].split("#")[0]
	elif line[0] == "local":
		local = line[1].split("#")[0]
	elif line[0] == "verbose":
		verbose = line[1].split("#")[0]
	elif line[0] == "refresh":
		refresh = line[1].split("#")[0]
	elif line[0] == "port":	
		enterPort = int(line[1].split("#")[0])
	elif line[0] == "delimiter":
		delimiter = tmpLine.split("\'")[1]
	elif line[0] == "labels":
		labels = line[1].split("#")[0]
		print labels

	tmpLine = file.readline()
	line =  tmpLine.translate(None, " \n	").split("=")

file.close()

if com == "NULL":
	print "Error: com field empty, please see node.cfg"
	exit()
elif project == "NULL":
	print "Error: project field empty, please see node.cfg"
	exit()

# Connection to serial device
ser = serial.Serial(com)

packCount = 0
errCount = 0
line = project + ", "

time.sleep(1.5)

print 'Ready'
# Start data collection
while True:
	try:
		# Only post if data is different and it contains 'Packet: '
		temp = line.replace(project + ',', "")
		while temp == line.replace(project + ',', "") or temp.find('Packet: ') == -1:
			# Controls polling rate
			time.sleep(float(refresh))
			temp = ser.readline()
		line = temp
		line = line.replace(delimiter,",")

		print line
		line = line.replace('Packet: ', '')
		outputFile = open(project+".csv", "a")
		outputFile.write(line.replace(project + ',', ""))
		outputFile.close()

	except KeyboardInterrupt:
		print "\n\nTotal packets received: " + str(packCount)
		print "Total packets lost: " + str(errCount)
		exit()

	except Exception, e:
		print "Error"
		print e
