#!/usr/bin/python 

#-------------------------------------------------------------------------------------
# This module is part of the PHD Thesis:
# "A User-Centric SDN Management Architecture for NFV-based Residential Networks".
# Copyright Ricardo Flores Moyano 2016. 
#-------------------------------------------------------------------------------------          		

import socket, json, sys
import threading

class Sender(threading.Thread):

	# To send RENESE messages to the lower layer, each RENEMA App uses the Sender service of the
	# RENEMA App Manager to do it.
	# The sequence is as follows: Fist, a new instance of the Sender is created. Second, the message 
	# to be sent is load in the "message_to_send" variable and finally, the method run is launch as a
	# thread. 

	def __init__(self):

		# Init Method to initialize the Sender:
		threading.Thread.__init__(self)
		self.tcp_port = 14713
		self.message_to_send = ''


	def run(self):

		# This method is called to send the RENESE message once the "message_to_send" has been previously
		# defined by the RENEMA App.
		s = socket.socket()         	
		host = socket.gethostname() 	                	
		s.connect((host, self.tcp_port))
		s.send(self.message_to_send)
		s.close 


	def setMessageToSend(self, json_data):

		# This method set the RENESE message to be sent to the lower layer.
		# The message received here is already formatted as JSON message.
		self.message_to_send = json_data


		