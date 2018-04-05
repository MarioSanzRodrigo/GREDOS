#!/usr/bin/python

#-------------------------------------------------------------------------------------
# This module is part of the PHD Thesis:
# "A User-Centric SDN Management Architecture for NFV-based Residential Networks".
# Copyright Ricardo Flores Moyano 2016. 
#-------------------------------------------------------------------------------------           		

import os, json
from time import sleep
from ManagementLayer.DB.DB import DB
from ManagementLayer.RenemaAppManager.Sender import Sender
from ManagementLayer.RenemaAppManager.IdAllocator import IdAllocator



class NetworkStatus(object):

	# This Class represents the back-end of the NetworkStatus App. This module forms part of the
	# Management Layer. The functionalities of this App are visible by means of the REST API developed.

	def get_Name(o):

		# This method returns the full name of the NetworkStatus class. This name is
		# stored in the forwarding_table dictionary as value. This class name is used to
		# invoke dynamically the method in charge of getting the RENESE Messages.
		module = o.__class__.__module__
		if module is None or module  == str.__class__.__module__:
			return o.__class__.__name__
		return module + '.' + o.__class__.__name__


	def get_Reneseid(self):

		# This method gets the Id of the RENESE required to perform the different tasks
		# of this RENEMA App.
		# By now, the NetworkStatus gets the Id of the DeviceTracking and NESA services.
		# This RENEMA App also needs to get the Id of the NERON service.

		if DB().get_devicetracker_id() == '':

		# To simplify the message to discover a given RENESE, the field "Todiscover" was
			# added to the header. However, this is not correct because modifies the
			# standard header composed of 4 fields: SenderId, ReceiverId, Service and Arguments.
			# The commented message should be used instead:
		#message_discover = {
			#		'SenderId': DB().get_networkstatus_id(),
			#		'ReceiverId': '',
			#		'Service': 'service_discovery_request',
			#		'Arguments': {
			#			'ToDiscover': 'devices_tracking',
			#		}
			#}
			
			message_discover = {
					'SenderId': DB().get_networkstatus_id(),
					'ReceiverId': '',
					'Service': 'service_discovery_request',
					'Todiscover': 'devices_tracking'
				}
	
			sender = Sender()
			sender.setMessageToSend(json.dumps(message_discover))
			sender.start()

		if DB().get_nesa_id() == '':
			message_discover['Todiscover'] = 'network_statistics'
			sender = Sender()
			sender.setMessageToSend(json.dumps(message_discover))
			sender.start()

		if DB().get_neron_id() == '':
			message_discover['Todiscover'] ='network_resources'
			sender = Sender()
			sender.setMessageToSend(json.dumps(message_discover))
			sender.start()


	def get_Renema_id(self):

		# First, the NetworkStatus App requests an Id if there is no one allocated.
		if DB().get_networkstatus_id() == '':
			DB().save_networkstatus_id(IdAllocator().get_renema_app_id())

		# Next, the NetworkStatus App registers its Id on the RENEMA App Manager.
		networkstatus_id = DB().get_networkstatus_id()
		networkstatus_class_name = self.get_Name()
		IdAllocator().service_registry(networkstatus_id, networkstatus_class_name)


	def devicetracker_subscription(self):

		# Once the NetworkStatus App has got the Id of the RENESE(s) requiered, the
		# subscription process must be carried out in order to use the underlying services.
		# For the NetworkStatus App case, a subscription to the "DeviceTracking", "NESA" 
		# and "NERON" services is carried out.
		# After this process, the state of the corresponding subscription is saved.
		if DB().get_devicetracking_subscription() == '':
			subscription = {
					'SenderId':DB().get_networkstatus_id(),
					'ReceiverId':DB().get_devicetracker_id(),
					'Service': 'subscription_request'
			}

			sender = Sender()
			sender.setMessageToSend(json.dumps(subscription))
			sender.start()
			subscription['ReceiverId'] = DB().get_nesa_id()
			sender = Sender()
			sender.setMessageToSend(json.dumps(subscription))
			sender.start()
			subscription['ReceiverId'] = DB().get_neron_id()
			sender = Sender()
			sender.setMessageToSend(json.dumps(subscription))
			sender.start()
			DB().save_devicetracking_subscription('done')

		
	def get_ReneseMessage(self, message):

		# This Method receives all RENESE Messages sent from the SDN Application layer. Thereby, the
		# the "connection" or "disconnection" of end user's devices on the network are notified by the
		# DeviceTracking service. 
		# The messages Subscription and Service Discovery messages are also received.
		if message['Service'] == 'new_connection':
			print '\n---NetworkStatus App:'
			print 'New device connected:'
			print 'Device: ', message['Arguments']['device_mac'], '\tPort:', message['Arguments']['device_port']
			state_device = 'online'
			self.set_state(message, state_device)
			self.show_devices()

		elif message['Service'] == 'disconnection':
			print '\n--NetworkStatus App:'
			print 'Device Disconnected'
			print 'Device: ', message['Arguments']['device_mac'], '\tPort:', message['Arguments']['device_port']
			state_device = 'offline'
			DB().update_status(message['Arguments']['device_mac'], 'state', 'offline')
			#self.delete_device(notification['mac'])
			self.show_devices()

		elif message['Service'] == 'subscription_reply':
			print '\n---NetworkStatus App: Service Subscription Reply received'

		elif message['Service'] == 'stats_reply': # It should be named 'network_stats_notification'
			print '\n---NetworkStatus App: Stats Received'
			DB().save_stats(message['Arguments'])

		elif message['Service'] == 'resources_reply':
			print '\n---NetworkStatus App: Resources State Received'

		elif message['Service'] == 'service_discovery_reply':
			print '\n---NetworkStatus App: Service Discovery Reply received'
			if message['Todiscover'] == 'devices_tracking':
				DB().save_devicetracker_id(message['SenderId'])
			elif message['Todiscover'] == 'network_statistics':
				DB().save_nesa_id(message['SenderId'])
			elif message['Todiscover'] == 'network_resources':
				DB().save_neron_id(message['SenderId'])

		elif message['Service'] == 'resources_state_notification':
			print '\n---NetworkStatus App: Resources State Notification received'
			DB().save_resources_state(message['Arguments'])

		else:
			print '\n---NetworkStatus App: Unknown Service'


	def set_state(self, message, state):

		# This Method creates a new state entry into the DB.
		# The entry is created if it has not been created before, otherwise it is updated.
		retrieve_state = DB().get_state(message['Arguments']['device_mac'])

		if len(retrieve_state) == 0:
			query = DB().get_policy(message['Arguments']['device_mac'])

			if len(query) is not 0:
				condition = 'defined'
			else:
				condition = 'undefined'

			state = {
        		'device': message['Arguments']['device_mac'],
        		'port': message['Arguments']['device_port'], 
        		'policy': condition,
        		'state': state
			}

			status = DB().get_status()
			status.append(state)
			DB().save_status(status)

		else:
			DB().update_status(message['Arguments']['device_mac'], 'state', 'online')


	def show_devices(self):

		# This Method shows all the state entries stored in the DB.
		print '\n--NetworkStatus App:'
		print '\t\t', 'Status of connected devices'
		query = DB().get_status()
		for raw in query:
			print 'Device:', raw['device'], '\t', 'Port:', raw['port'], '\t', 'Policy:', raw['policy'], '\t', 'State:', raw['state']


	def get_status(self):

		# This Method returns the state of all devices connected to the residential
		# network.
		return DB().get_status()


	def delete_device(self, device):

		# This Method deletes the device state from the DB.
		status = DB().get_status()
		state = DB().get_state(device)
		status.remove(state[0])
		DB().save_status(status)


	def devices_state(self):

		# The NetworkStatus App together with the DeviceTracking service inform the residential user about
		# all the devices that have been connected or disconnected. The Application groups into two categories,
		# the "ONLINE" devices and the "OFFLINE" devices.
		connected_devices = []
		no_connected_devices = []
		status = DB().get_status()
		for entry in status:
			if entry['state'] == 'online':
				connected_devices.append(entry['device'])
			if entry['state'] == 'offline':
				no_connected_devices.append(entry['device'])
		devices_state = {'ONLINE devices': connected_devices, 'OFFLINE devices': no_connected_devices}
		return devices_state


	def device_state(self, device):

		# This Method returns the state of a specific device.
		# The state is composed of the following fields: "Device", "Port", "Policy" and "State".
		device_state = DB().get_state(device)

		if len(device_state) == 0:
			print '\n--Network Status App:'
			print 'No Device State'

		return device_state


	def devices_stats(self):

		# This method returns the statistics of all connected devices.
		# The total bandwdith consumption (Tx + Rx) per device is provided as array.
		stats_to_show = []
		stats = DB().get_stats()
		status = DB().get_status()
		for entry in stats:
			for state in status:
				if entry['port'] == state['port']:
					consumption = "{0:.2f}".format((float(entry['bw_rx']) + float(entry['bw_tx']))/1000000)
					stats_to_show.append({'device': state['device'], 'consumption (Mbps)': consumption})

		return stats_to_show


	def device_stats(self, device):

		# This method returns a more detailed statistic of a specific connected device.
		device_state = DB().get_state(device)
		stats = DB().get_stats()
		for entry in stats:
			if entry['port'] == device_state[0]['port']:
				Transmission = "{0:.2f}".format(float(entry['bw_tx'])/1000000)
				Reception = "{0:.2f}".format(float(entry['bw_rx'])/1000000)
				stat_to_show = {'device': device, 'port': device_state[0]['port'], 'Transmission (Mbps)': Transmission, 'Reception (Mbps)': Reception}

		return stat_to_show


	def network_resources(self):

		# This method returns the global state of network resources.
		resources = DB().get_resources()
		resources_to_show = {
				'Hired Bandwidth (Mbps)': "{0:.2f}".format(float(resources['contracted_ic_bw'])/1000000),
				'Bandwidth Consumption (Mbps)': "{0:.2f}".format(float(resources['used_ic_bw'])/1000000),
				'Available Bandwidth (Mbps)': "{0:.2f}".format(float(resources['available_ic_bw'])/1000000),
				'Active Ports': resources['active_ports']
		}

		return resources_to_show


	def device_resources(self, device):

		# This method returns a more detailed state of network resources per device.
		device_state = DB().get_state(device)
		resources = DB().get_resources()
		resources_to_show = {
				'Device': device,
				'Port': device_state[0]['port'],
				'Port Bandwidth': "{0:.2f}".format(float(resources['bw_per_port'])/1000000),
				'Available Queues': {
						'q1 (Mbps)': "{0:.2f}".format(float(resources['q1_bw'])/1000000),
						'q2 (Mbps)': "{0:.2f}".format(float(resources['q2_bw'])/1000000),
						'q3 (Mbps)': "{0:.2f}".format(float(resources['q3_bw'])/1000000),
				}
		}

		return resources_to_show


	def stats_query(self):

		# This method allows getting the network stats using an on-demand model.
		# (Not used at the moment).
		arguments = []
		status = DB().get_status()
		for entry in status:
			arguments.append({'port':entry['port'], 'bw_rx':0, 'bw_tx':0})

		renese_message = {
				'SenderId':DB().get_networkstatus_id(),
				'ReceiverId':DB().get_nesa_id(),
				'Service': 'stats_request',
				'Arguments': arguments
		}

		sender = Sender()
		sender.setMessageToSend(json.dumps(renese_message))
		sender.start()


	def clear_status(self):

		# This Method sets the "Policy" field in "undefined" for all the state entries.
		# This method is called when the ParentalControl App deletes all the defined policies.
		policies = DB().get_policies()

		if len(policies) is 0:

			status = DB().get_status()
			for state in status:
				state['policy'] = 'undefined'

			DB().save_status(status)

		else:
			print 'Impossible to delete the status'