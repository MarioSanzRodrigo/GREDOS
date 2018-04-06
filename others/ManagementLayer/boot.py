#!/usr/bin/python   

#-------------------------------------------------------------------------------------
# This module is part of the PHD Thesis:
# "A User-Centric SDN Management Architecture for NFV-based Residential Networks".
# Copyright Ricardo Flores Moyano 2016. 
#-------------------------------------------------------------------------------------

import commands, sys, requests, json, os
from time import sleep
from ManagementLayer.RenemaAppManager.Receiver import Receiver
from ManagementLayer.RenemaAppManager.Sender import Sender
from ManagementLayer.DB.DB import DB
from ManagementLayer.RenemaApps.ParentalControl import ParentalControl
from ManagementLayer.RenemaApps.NetworkStatus import NetworkStatus


# -------------------------------------------------------------------------------------------------------------------
def boot():

	# This script helps in configuring the initial stages of all RENEMA Apps.
	# In addition the Receiver module of the RENEMA App Manager as well as the REST API
	# are launched.

	#------------------------------- STARTUP VALUES -------------------------------
	tcp_port = 14712   # Receiver TCP port
	server = 'http://localhost:5000'
	headers = {'content-type': 'application/json'}
	apirest_path = os.path.dirname(os.path.realpath(__file__))
	api_rest_full_path = 'python ' + apirest_path + '/ApiRest.py'
	os.system('clear')
	#------------------------------------------------------------------------------

	# A DB object is created in order to initialize its default values:
	db = DB()
	# A subdirectory called 'data' is created to save the files:
	if os.path.exists(os.getcwd() + '/ManagementLayer/DB/data'):
		pass
	else:
		os.makedirs(os.getcwd() + '/ManagementLayer/DB/data')


    # The different modules are launched. Ctrl + C ends the booter.
	try:	
		print '-' * 26,'MANAGEMENT LAYER RUNNING','-' * 26
		print '(Press CTRL+C to quit)'
		# The Receiver of RENEMA App Manager is launched:
		receiver = Receiver(tcp_port)
		receiver.start()

		# All RENEMA Apps request an Id
		ParentalControl().get_Renema_id()
		NetworkStatus().get_Renema_id()

		# All RENEMA Apps request the RENESE Id based on the service to be used
		ParentalControl().get_Reneseid()
		NetworkStatus().get_Reneseid()

		# Once the RENESE Id has been discovered, all RENEMA Apps must subscribe to a specific RENESE
		sleep(0.04)
		ParentalControl().switching_subscription()
		NetworkStatus().devicetracker_subscription()

		# The REST API (flask) is launched:
		sleep(0.5)
		status,output = commands.getstatusoutput(api_rest_full_path)
		
		while True:
			sleep(1)   # Infinite loop until "CTRL+C" be pressed.
			
		
	except KeyboardInterrupt:
		
		# Killing the Receiver of RENEMA App Manager:
		receiver.stop_receiver()

		# Killing the REST API (flask):
		#new_policy = requests.post(server + '/shutdown', data=json.dumps(''), headers=headers)
		print '-' * 26,'MANAGEMENT LAYER STOPPED','-' * 26
		sys.exit(0)
		

# -------------------------------------------------------------------------------------------------------------------

# Calling the booter:
boot()
