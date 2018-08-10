# Script to deliver data to server

import serial
import time
import datetime
import logging
import os
import csv
import socket

host = "10.16.10.240"
#host = socket.gethostbyname("localhost")

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

# Ask server for an available port
try:
	path = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	path.connect((host, enterPort))
	path.sendall(project)
	port = int(path.recv(1024))
	path.sendall(labels)
	path.close()
except socket.error:
	print "Cannot connect to port " + str(enterPort) + ", exiting"
	exit()

time.sleep(1.5)
print "Connecting to port " + str(port)

try:
	path = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	path.connect((host, port))
except socket.error:
	print "Cannot connect to port " + str(port) + ", exiting"
	exit()

# Start data collection
while True:
	try:
		# Only post if data is different and it contains 'Packet: '
		temp = line.replace(project + ',', "")
		while temp == line.replace(project + ',', "") or line.find('Packet :') == -1:
			# Controls polling rate
			time.sleep(float(refresh))
			temp = ser.readline()
			temp = temp.replace('Packet: ', '')
		line = project + "," + temp
		line = line.replace(delimiter,",")

		print "\nPosting to server: " + line + "\033[F"

		path.sendall(line+str(port))
		reply = path.recv(1024)
		if reply == "":
			print "Error: no reply from server, reconnecting"
			errCount+=1
			for x in xrange(30):
				path.close()
				time.sleep(3)
				print "Connection lost, retry #" + str(x + 1)
				try:
					path = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					path.connect((host, enterPort))
					path.sendall(project)
					port = int(path.recv(1024))
					path.sendall(labels)
					path.close()
				except socket.error:
					print "Socket error"

				time.sleep(0.5)
				print "Connecting to port " + str(port)

				try:
					path = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					time.sleep(0.5)
					print port
					path.connect((host, port))
					break
				except socket.error:
					"Socket error"
		else:
			print repr(reply)
			packCount+=1

		if local == "yes":
			reply.replace('Packet: ', '')
			outputFile = open(project+".csv", "a")
			outputFile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+","+line.replace(project + ',', ""))
			outputFile.close()

	except KeyboardInterrupt:
		print "\n\nTotal packets received: " + str(packCount)
		print "Total packets lost: " + str(errCount)
		path.sendall("exiting")
		path.shutdown(socket.SHUT_RDWR)
		path.close()
		exit()

	except socket.error:
		print "Socket error"
		for x in xrange(30):
			try:
				path.shutdown(socket.SHUT_RDWR)
				path.close()
				print ""
			except Exception, e:
				print e
			time.sleep(3)
			print "Connection lost, retry #" + str(x + 1)
			try:
				path = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				path.connect((host, enterPort))
				path.sendall(project)
				port = int(path.recv(1024))
				print port
				path.sendall(labels)
				path.shutdown(socket.SHUT_RDWR)
				path.close()
			except socket.error:
				print "Socket error"

			time.sleep(0.5)
			print "Connecting to port " + str(port)

			try:
				path = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				time.sleep(0.5)
				path.connect((host, port))
				break
			except socket.error:
				"Socket error"

	except Exception, e:
		print "Error"
		print e
