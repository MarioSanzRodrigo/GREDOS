#!/usr/bin/python 

#-------------------------------------------------------------------------------------
# This module is part of the PHD Thesis:
# "A User-Centric SDN Management Architecture for NFV-based Residential Networks".
# Copyright Ricardo Flores Moyano 2016. 
#-------------------------------------------------------------------------------------          		

from ManagementLayer.DB.DB import DB

prefix = 'ml-app-0'

class IdAllocator(object):

	# Each RENEMA App must have an Identifier (Id). When a RENEMA App starts for the first time, it requests an Id to
	# the RENEMA App Manager. The Id is composed of a "prefix" (ml-app-0) and an "Id". The prefix is a
	# constant string value and the Id is obtained based on the already allocated Ids.


	def get_renema_app_id(self):

		# This method retrieves all the allocated Ids in order to know what should
		# be the next prefix to be allocated.
		# Then, the new Id is stored in the DB.
		renema_apps_ids = []
		renema_apps_ids = DB().get_renema_apps_ids()
		app_id = len(renema_apps_ids) + 1
		renema_id = prefix + str(app_id)
		renema_apps_ids.append(renema_id) 
		DB().save_renema_apps_ids(renema_apps_ids)
		return renema_id

	def service_registry(self, renema_id, class_name):

		# This method allows populating a HashMap (Forwarding_Table) where the
		# key is the RENEMA Id and the value is the class_name of the RENEMA App.
		# This HashMap is used to perform the forwarding of the received message
		# to the specific RENEMA App.
		DB().save_renema_class_name(renema_id, class_name)

		
