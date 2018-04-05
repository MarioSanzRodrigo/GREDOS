#!/usr/bin/python     

#-------------------------------------------------------------------------------------
# This module is part of the PHD Thesis:
# "A User-Centric SDN Management Architecture for NFV-based Residential Networks".
# Copyright Ricardo Flores Moyano 2016. 
#-------------------------------------------------------------------------------------          		

import os, json

class DB(object):

	# All the data produced by the different RENEMA Apps as well as complementary information 
	# are stored in a folder (/data). This module provides an API to all RENEMA Apps in order 
	# to facilitate the handling and storage of data.
	# By now and for demonstrative purposes a formal DB is not used. When a formal DB be used the API
	# (methods) should be updated.


	def __init__(self):

		# The init method to set the initial values of the class.
		self.p_path = "/data/policies.txt"
		self.s_path = "/data/status.txt"
		self.switching_id_path = "/data/switching_id.txt"
		self.devicetracker_id_path = "/data/devicetracker_id.txt"
		self.nesa_id_path = "/data/nesa_id.txt"
		self.neron_id_path = "/data/neron_id.txt"
		self.renema_apps_ids_path = "/data/renema_apps_ids.txt"
		self.parentalcontrol_id_path = "/data/parentalcontrol_id.txt"
		self.networkstatus_id_path = "/data/networkstatus_id.txt"
		self.devicetracking_done_path = "/data/devicetracking_done.txt"
		self.switching_done_path = "/data/switching_done.txt"
		self.forwarding_table_path = "/data/forwarding_table.txt"
		self.stats_path = "/data/stats.txt"
		self.resources_path = "/data/resources.txt"
		self.db_path = os.path.dirname(os.path.realpath(__file__))


	def get_policies(self):

		# This Method returns all defined policies.
		if os.path.isfile(self.db_path + self.p_path) == False or os.path.getsize(self.db_path + self.p_path) == 0:
			policies = []
		else:
			policies = json.load(open(self.db_path + self.p_path))

		return policies


	def get_policy(self, device):

		# This Method returns a policy defined for a specific device.
		query = self.get_policies()

		if len(query) is not 0:
			policy = [policy for policy in query if policy['device'] == device]   
		else:
			policy = []

		return policy


	def save_policies(self, policies):

		# This Method saves all defined policies.
		json.dump(policies, open(self.db_path + self.p_path, "w"))


	def save_status(self, status):

		# This Method saves the state of all devices.
		json.dump(status, open(self.db_path + self.s_path, "w"))


	def get_status(self):

		# This Method returns the state of all devices.
		if os.path.isfile(self.db_path + self.s_path) == False or os.path.getsize(self.db_path + self.s_path) == 0:
			status = []
		else:
			status = json.load(open(self.db_path + self.s_path))

		return status


	def get_state(self, device):

		# This Method returns the state of a specific device.
		status = self.get_status()

		if len(status) is not 0:
			state = [state for state in status if state['device'] == device]
		else:
			state = []

		return state


	def update_status(self, device, field, value):

		# This Method updates a field into the state of a specific device.
		status = self.get_status()
		state = [state for state in status if state['device'] == device]
		state[0][field] = value
		self.save_status(status)


	def get_devices_list(self):

		# Experimental: not used.
		if os.path.isfile("DB/devices.txt") == False or os.path.getsize("DB/devices.txt") == 0:
			devices = []
		else:
			devices = json.load(open("DB/devices.txt"))

		return devices


	def save_devices_list(self, devices):

		# Experimental: not used.
		json.dump(devices, open("DB/devices.txt", "w"))


	def save_switching_id(self, switching_id):

		# This Method saves the Switching service Id.
		data = {
			'SwitchingId':switching_id
		}
		json.dump(data, open(self.db_path + self.switching_id_path, "w"))


	def get_switching_id(self):

		# This Method returns the Switching Service Id.
		if os.path.isfile(self.db_path + self.switching_id_path) == False or os.path.getsize(self.db_path + self.switching_id_path) == 0:
			switching_id = ''
		else:
			switching_id = json.load(open(self.db_path + self.switching_id_path))
			switching_id = switching_id['SwitchingId']

		return switching_id


	def save_devicetracker_id(self, devicetracker_id):

		# This Method saves the DeviceTracking service Id.
		data = {
			'DeviceTrackerId':devicetracker_id
		}
		json.dump(data, open(self.db_path + self.devicetracker_id_path, "w"))


	def get_devicetracker_id(self):

		# This Method returns the DeviceTracking Service Id.
		if os.path.isfile(self.db_path + self.devicetracker_id_path) == False or os.path.getsize(self.db_path + self.devicetracker_id_path) == 0:
			devicetracker_id = ''
		else:
			devicetracker_id = json.load(open(self.db_path + self.devicetracker_id_path))
			devicetracker_id = devicetracker_id['DeviceTrackerId']

		return devicetracker_id


	def save_nesa_id(self, nesa_id):

		# This Method saves the NESA service Id.
		data = {
			'NesaId':nesa_id
		}
		json.dump(data, open(self.db_path + self.nesa_id_path, "w"))


	def get_nesa_id(self):

		# This Method returns the NESA Service Id.
		if os.path.isfile(self.db_path + self.nesa_id_path) == False or os.path.getsize(self.db_path + self.nesa_id_path) == 0:
			nesa_id = ''
		else:
			nesa_id = json.load(open(self.db_path + self.nesa_id_path))
			nesa_id = nesa_id['NesaId']

		return nesa_id


	def save_neron_id(self, neron_id):

		# This Method saves the NERON service Id.
		data = {
			'NeronId':neron_id
		}
		json.dump(data, open(self.db_path + self.neron_id_path, "w"))


	def get_neron_id(self):

		# This Method returns the NERON Service Id.
		if os.path.isfile(self.db_path + self.neron_id_path) == False or os.path.getsize(self.db_path + self.neron_id_path) == 0:
			neron_id = ''
		else:
			neron_id = json.load(open(self.db_path + self.neron_id_path))
			neron_id = neron_id['NeronId']

		return neron_id


	def get_renema_apps_ids(self):

		# This Method returns an ArrayList of the RENEMA App Ids already allocated.
		# If the file does not exist, an Empty array is returned. Otherwise an array
		# containing the allocated Ids is returned.
		if os.path.isfile(self.db_path + self.renema_apps_ids_path) == False or os.path.getsize(self.db_path + self.renema_apps_ids_path) == 0:
			renema_apps_ids = []
		else:
			with open(self.db_path + self.renema_apps_ids_path, 'r') as f:
				renema_apps_ids = [line.rstrip('\n') for line in f]
		return renema_apps_ids


	def save_renema_apps_ids(self, renema_apps_ids):

		# Once the Ids have been loaded from the file, this Method saves all of them
		# plus the new allocated on the same file.
		with open(self.db_path + self.renema_apps_ids_path, 'w') as f:
			for renema_id in renema_apps_ids:
				f.write(renema_id + '\n')


	def save_parentalcontrol_id(self, parentalcontrol_id):

		# This method saves the allocated ParentalControl Id to a file.
		data = {
			'ParentalControlId':parentalcontrol_id
		}
		json.dump(data, open(self.db_path + self.parentalcontrol_id_path, "w"))


	def get_parentalcontrol_id(self):

		# This Method returns the allocated ParentalControl Id from a file.
		if os.path.isfile(self.db_path + self.parentalcontrol_id_path) == False or os.path.getsize(self.db_path + self.parentalcontrol_id_path) == 0:
			parentalcontrol_id = ''
		else:
			parentalcontrol_id = json.load(open(self.db_path + self.parentalcontrol_id_path))
			parentalcontrol_id = parentalcontrol_id['ParentalControlId']

		return parentalcontrol_id


	def save_networkstatus_id(self, networkstatus_id):

		# This method saves the allocated NetworkStatus Id to a file.
		data = {
			'NetworkStatusId':networkstatus_id
		}
		json.dump(data, open(self.db_path + self.networkstatus_id_path, "w"))


	def get_networkstatus_id(self):

		# This Method returns the allocated NetworkStatus Id from a file.
		if os.path.isfile(self.db_path + self.networkstatus_id_path) == False or os.path.getsize(self.db_path + self.networkstatus_id_path) == 0:
			networkstatus_id = ''
		else:
			networkstatus_id = json.load(open(self.db_path + self.networkstatus_id_path))
			networkstatus_id = networkstatus_id['NetworkStatusId']

		return networkstatus_id


	def save_devicetracking_subscription(self, state):

		# This Method saves the subscription process state to a file.
		data = {
			'DeviceTrackingSubscription':state
		}
		json.dump(data, open(self.db_path + self.devicetracking_done_path, "w"))


	def get_devicetracking_subscription(self):

		# This Method returns the subscription state from a file.
		if os.path.isfile(self.db_path + self.devicetracking_done_path) == False or os.path.getsize(self.db_path + self.devicetracking_done_path) == 0:
			subscription_state = ''
		else:
			subscription_state = json.load(open(self.db_path + self.devicetracking_done_path))
			subscription_state = subscription_state['DeviceTrackingSubscription']

		return subscription_state


	def save_switching_subscription(self,state):

		# This Method saves the subscription process state to a file.
		data = {
			'SwitchingSubscription':state
		}
		json.dump(data, open(self.db_path + self.switching_done_path, "w"))


	def get_switching_subscription(self):

		# This Method returns the subscription state from a file.
		if os.path.isfile(self.db_path + self.switching_done_path) == False or os.path.getsize(self.db_path + self.switching_done_path) == 0:
			subscription_state = ''
		else:
			subscription_state = json.load(open(self.db_path + self.switching_done_path))
			subscription_state = subscription_state['SwitchingSubscription']

		return subscription_state


	def get_renema_class_name(self, renema_id):

		# This Method returns the class name associated to the renema_id received.
		# This Method is used by the RENEMA App Manager to forward the RENESE Message
		# to the appropriated receiver.
		forwarding_table = {}
		if os.path.isfile(self.db_path + self.forwarding_table_path) == False or os.path.getsize(self.db_path + self.forwarding_table_path) == 0:
			class_name = ''
		else:
			forwarding_table = json.load(open(self.db_path + self.forwarding_table_path))
			class_name = forwarding_table[renema_id]

		return class_name


	def save_renema_class_name(self, renema_id, class_name):

		# Once a RENEMA App gets a valid Id, the pair class name and Id are stored as a dictionary.
		# The Key is the renema_id and the value is the class_name.
		forwarding_table = {}

		if os.path.isfile(self.db_path + self.forwarding_table_path) == False or os.path.getsize(self.db_path + self.forwarding_table_path) == 0:
			pass
		else:
			forwarding_table = json.load(open(self.db_path + self.forwarding_table_path))
		
		forwarding_table[renema_id] = class_name
		json.dump(forwarding_table, open(self.db_path + self.forwarding_table_path, "w"))


	def save_stats(self, stats):

		# This Method saves the stats provided by NESA to a file.
		json.dump(stats, open(self.db_path + self.stats_path, "w"))


	def get_stats(self):

		# This Method returns the stats of all devices.
		if os.path.isfile(self.db_path + self.stats_path) == False or os.path.getsize(self.db_path + self.stats_path) == 0:
			stats = []
		else:
			stats = json.load(open(self.db_path + self.stats_path))

		return stats


	def save_resources_state(self, resources):

		# This Method saves the network resources state provided by NERON to a file.
		json.dump(resources, open(self.db_path + self.resources_path, "w"))


	def get_resources(self):

		# This Method returns the network resources state.
		if os.path.isfile(self.db_path + self.resources_path) == False or os.path.getsize(self.db_path + self.resources_path) == 0:
			resources = {}
		else:
			resources = json.load(open(self.db_path + self.resources_path))

		return resources
