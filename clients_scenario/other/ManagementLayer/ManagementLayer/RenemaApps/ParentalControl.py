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


class ParentalControl(object):

	# This Class represents the back-end of the ParentalControl App. This module forms part of the
	# Management Layer. The functionalities of this App are visible by means of the REST API developed.
	
	def get_Name(o):

		# This method returns the full name of the ParentalControl class. This name is
		# stored in the forwarding_table dictionary as value. This class name is used to
		# invoke dynamically the method in charge of getting the RENESE Messages.
		module = o.__class__.__module__
		if module is None or module  == str.__class__.__module__:
			return o.__class__.__name__
		return module + '.' + o.__class__.__name__


	def get_Reneseid(self):

		# This method gets the Id of the RENESE required to perform the different tasks
		# of this RENEMA App.
		# To simplify the process, only the Id of the "Switching" service is requested. It's
		# assumed the NetworkStatus App already has the Id of the "DeviceTracking" service.
		# Considering a strict behavior, the ParentalControl must get all the Ids of the RENESEs
		# required by itself.
		if DB().get_switching_id() == '':
			# To simplify the message to discover a given RENESE, the field "Todiscover" was
			# added to the header. However, this is not correct because modifies the
			# standard header composed of 4 fields: SenderId, ReceiverId, Service and Arguments.
			# The commented message should be used instead:

			#message_discover = {
			#		'SenderId': DB().get_parentalcontrol_id(),
			#		'ReceiverId': '',
			#		'Service': 'service_discovery_request',
			#		'Arguments': {
			#			'ToDiscover': 'switching',
			#		}
			#}

			message_discover = {
					'SenderId': DB().get_parentalcontrol_id(),
					'ReceiverId': '',
					'Service': 'service_discovery_request',
					'Todiscover': 'switching'
				}
	
			sender = Sender()
			sender.setMessageToSend(json.dumps(message_discover))
			sender.start()

			
	def get_Renema_id(self):

		# First, the ParentalControl App requests and Id if there is no one allocated.
		if DB().get_parentalcontrol_id() == '':
			DB().save_parentalcontrol_id(IdAllocator().get_renema_app_id())

		# Next, the ParentalControl App registers its Id on the RENEMA App Manager.
		parentalcontrol_id = DB().get_parentalcontrol_id()
		parentalcontrol_class_name = self.get_Name()
		IdAllocator().service_registry(parentalcontrol_id, parentalcontrol_class_name)


	def switching_subscription(self):

		# Once the ParentalControl App has got the Id of the RENESE(s) requiered, the
		# subscription process must be carried out in order to use the underlying services.
		# For the ParentalControl App case, a subscription to the "Switching" and "DeviceTracking"
		# services is carried out.
		# After this process, the state of the corresponding subscription is saved.
		if DB().get_switching_subscription() == '':
			subscription = {
					'SenderId':DB().get_parentalcontrol_id(),
					'ReceiverId':DB().get_switching_id(),
					'Service': 'subscription_request'
			}

			sender = Sender()
			sender.setMessageToSend(json.dumps(subscription))
			sender.start()
			subscription['ReceiverId'] = DB().get_devicetracker_id()
			sender = Sender()
			sender.setMessageToSend(json.dumps(subscription))
			sender.start()
			DB().save_switching_subscription('done')


	def get_ReneseMessage(self, message):
		
		# This Method receives all RENESE Messages sent from the SDN Application layer. Thereby, the
		# the "connection" or "disconnection" of end user's devices on the network are notified by the
		# DeviceTracking service. 
		# The messages Subscription and Service Discovery messages are also received.
		if message['Service'] == 'new_connection':
			policy = DB().get_policy(message['Arguments']['device_mac'])
			if len(policy) is not 0:
				self.set_policy(policy[0])
			else:
				#if message['Service'] == 'new_connection':
					print '\n--Parental Control App:'
					print 'No policy for the new device. Please, define it!!'

		elif message['Service'] == 'disconnection':
			self.remove_policy(message['Arguments']['device_mac']) # This line must be removed because the flow entry will be automatically 
																	   # removed by the OVS itself.
		elif message['Service'] == 'subscription_reply':
			print '\n---ParentalControl App: Service Subscription Reply received'

		elif message['Service'] == 'service_discovery_reply':
			print '\n---ParentalControl App: Service Discovery Reply received'
			DB().save_switching_id(message['SenderId'])

		elif message['Service'] == 'resource_allocation_reply':				# A resource allocation reply is received considering that a device
			policy = DB().get_policy(message['Arguments']['device_mac'])	# is going to be added to the Switching service
			if len(policy) is not 0:
				self.updateSwitching(policy[0], message)

		else:
			print '\n---ParentalControl App: Unknown Service'
		

	def get_policies(self):

		# This Method returns all the defined policies stored in the DB.
		return DB().get_policies()


	def get_policy(self, device):

		# This Method returns a policy defined for a specific device.
		query = DB().get_policy(device)

		if len(query) == 0:
			print '\n--Parental Control App:'
			print 'The DB is non existent or it is empty'

		return query


	def updateSwitching(self, policy, message):

		# This Method specifies the action to be taken on the end user's device.
		# The verification of the action == allow should not be carried out considering
		# that the resource allocation reply is sent from NERON to add a device to the
		# Switching service
		if policy['action'] == 'allow':
			service = 'add_Device'
			self.add_policy(policy, message, service)
		else:
			service = 'remove_Device'
			

	def set_policy(self, policy):

		# This Method specifies the action to be taken on the resources.
		# This information helps NERON to know if resources must be allocated
		# or released.
		if policy['action'] == 'allow':
			action = 'allocate'
			service = 'resource_allocation_request'
		elif policy['action'] == 'block':
			action = 'release'
			service = 'release_resources'
			self.remove_policy(policy['device'])

		# To build the RESENE Message the device port is requiered. To simplify the process
		# the information already stored in the DB about the device by the NetworkStatus App 
		# is retrieve by the ParentalControl App.
		device_state = DB().get_state(policy['device'])

		# Before to add or remove a device to/from the switching service, it's necessary
		# to get the corresponding queue allocated by NERON.
		renese_message = {
			'SenderId': DB().get_parentalcontrol_id(),
			'ReceiverId': DB().get_neron_id(),
			'Service': service,
			'Arguments': {
				'action': action,
				'device_mac': policy['device'],
				'priority': policy['priority'],
				'device_port': device_state[0]['port']
			}
		}

		#sleep(0.1)  # A delay is introduced until the flow entry be installed on the OVS, otherwise the Drop flow entry
				     # will not be removed.
		sender = Sender()
		sender.setMessageToSend(json.dumps(renese_message))
		sender.start()


	def add_policy(self, policy, message, service):
		
		# This method only prints a message on the screen when an "allow" policy is defined for a device.
		print '\n--Parental Control App:'
		print 'Device: ', policy['device'], ' has the following schedule:'
		for day in policy['schedule']:
			print '\t', day['day'], '-->', day['time']

		print '\n*Device:', policy['device'], ' added to the switching service!!!', '\n'

		# Next, based on the reply of NERON, the device is added or removed to/from
		# the switching service.
		renese_message = {
			'SenderId': DB().get_parentalcontrol_id(),
			'ReceiverId': DB().get_switching_id(),
			'Service': service,
			'Arguments': {
				'device_mac': message['Arguments']['device_mac'],
				'device_port': message['Arguments']['device_port'],
				'port_queue': message['Arguments']['port_queue']
			}
		}

		sender = Sender()
		sender.setMessageToSend(json.dumps(renese_message))
		sender.start()


	def remove_policy(self, device):
		
		# This Method only prints a message on the screen when the device has been removed from the
		# Switching service.
		print '\n--Parental Control App:'
		print '*Device:', device, ' removed from the switching service!!!', '\n'

		# First, the device must be removed from the switching service:
		renese_message = {
			'SenderId': DB().get_parentalcontrol_id(),
			'ReceiverId': DB().get_switching_id(),
			'Service': 'remove_Device',
			'Arguments': {
				'device_mac': device,
				'device_port': 0,
				'port_queue': 0
			}
		}

		sender = Sender()
		sender.setMessageToSend(json.dumps(renese_message))
		sender.start()


	def define_policy(self, policy):

		# This Method stores the policy defined by the user in the DB.
		policies = DB().get_policies()
		policies.append(policy)
		DB().save_policies(policies)
		DB().update_status(policy['device'], 'policy', 'defined') # The device state entry must be updated.
		self.set_policy(policy)


	def update_policy(self, device, update):

		# This Method stores the changes made on a given policy.
		query = DB().get_policies()

		policy = [policy for policy in query if policy['device'] == device]

		policy[0]['action'] = update['action']
		policy[0]['priority'] = update['priority']
		policy[0]['schedule'] = update['schedule'] 

		DB().save_policies(query)  
		self.set_policy(policy[0])


	def delete_policy(self, device):

		# This Method deletes a policy of a specific device and removes the device from
		# the Switching service.
		query = DB().get_policies()
		policy = DB().get_policy(device)
		query.remove(policy[0])
		DB().save_policies(query)
		DB().update_status(policy[0]['device'], 'policy', 'undefined') # The device state entry must be updated.
		policy[0]['action'] = 'block'
		self.set_policy(policy[0])
			

	def clear_policies(self):

		# This Method deletes all the defined policies and informs the Switching service to remove all the devices
		# from its service. This action also implies clearing all the flow entries currently installed on the OpenFlow
		# switch and to install the default flow entry.
		policies = []
		DB().save_policies(policies)
		renese_message = {
			'SenderId': DB().get_parentalcontrol_id(),
			'ReceiverId': DB().get_switching_id(),
			'Service': 'clear_allowedDevicesTable',
			'Arguments': {
				'device_mac':'', 
				'device_port': 0,
				'port_queue': 0
			}
		}
		sender = Sender()
		sender.setMessageToSend(json.dumps(renese_message))
		sender.start()
		renese_message['ReceiverId'] = DB().get_neron_id()
		renese_message['Service'] = 'release_all_resources'
		sender = Sender()
		sender.setMessageToSend(json.dumps(renese_message))
		sender.start()

	
