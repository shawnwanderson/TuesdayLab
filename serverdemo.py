#!/usr/bin/env python

import socket
import os

serverSocket = socket.socket(socket.AF_INET,
socket.SOCK_STREAM)

serverSocket.bind(("0.0.0.0", 12346))

serverSocket.listen(5)

while True:
	(incomingSocket, address) = serverSocket.accept()
	childPid = os.fork()
	if (childPid != 0):
		#still on socket accepting process
		continue
	#in client talking process
	outgoingSocket = socket.socket(socket.AF_INET,
	socket.SOCK_STREAM)
	outgoingSocket.connect(("www.google.com", 80))
	done = False
	while not done:
		#fix cpu use with poll() ot select
		incomingSocket.setblocking(0)
		try:
			part = incomingSocket.recv(2048)
		except IOError, exception:
			if exception.errno == 11:
				part = None
			else:
				raise
		if (part):
			outgoingSocket.sendall(part)
		outgoingSocket.setblocking(0)
		try:
			part = outgoingSocket.recv(2048)
		except IOError, exception:
			if exception.errno == 11:
				part = None
			else:
				raise
		if (part):
			incomingSocket.sendall(part)
