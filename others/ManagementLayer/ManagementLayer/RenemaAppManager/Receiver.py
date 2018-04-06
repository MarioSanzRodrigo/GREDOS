#!/usr/bin/python

#-------------------------------------------------------------------------------------
# This module is part of the PHD Thesis:
# "A User-Centric SDN Management Architecture for NFV-based Residential Networks".
# Copyright Ricardo Flores Moyano 2016. 
#-------------------------------------------------------------------------------------           		

import socket, json, sys
import threading
from ManagementLayer.DB.DB import DB
from importlib import import_module


class Receiver(threading.Thread):

	# This class represents a module of the RENEMA App Manager. This module is in 
	# charge of receiving the RENESE messages sent from the SDN Application layer.
	# Considering the RENESE Message ReceiverId field, this message is forwarded
	# to the appropriate RENEMA App.
	
	def __init__(self, tcp_port):

		# Init Method to initialize the Receiver:
		threading.Thread.__init__(self)
		self.tcp_port = tcp_port
		self.flag = True
		self.s = socket.socket()
		self.host = socket.gethostname()
		self.s.bind((self.host, self.tcp_port))
		self.s.listen(5) 
		self.s.settimeout(0.1)
		

	def run(self):

		# Run Method: Thread running continuously while flag is True.
		print '\n','-' * 20,'RENEMA App Manager: Receiver Running','-' * 20
		
		while self.flag:
			try:
				c, addr = self.s.accept()     				# Establish connection with client.
				c.settimeout(None)
				received_message = json.loads(c.recv(1024))
				#print received_message
				c.close()

				# The received_message must be forwarded to the corresponding RENEMA App.
				# Based on the Receiver_Id, the class_name of the RENEMA App is retrieved from
				# the HashMap (forwarding_table) in order to launch the method "get_ReneseMessage"
				# dynamically. This method is called "reflection or instrospection".
				class_name = DB().get_renema_class_name(received_message['ReceiverId'])
				package, module = class_name.rsplit('.', 1)
				generic_module = import_module(package)
				generic_instance = getattr(generic_module, module)
				generic_instance().get_ReneseMessage(received_message)
			
			except socket.timeout:
				pass
			                		
	
	def stop_receiver(self):

		# Stop Method: the Receiver is stopped since the Booter has also been stopped.
		self.flag = False
		self.s.close()
		print '-' * 20,'RENEMA App Manager: Receiver Stopped','-' * 20