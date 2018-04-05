import requests, sys, os, json

# Parameters to locate the RENEMA App API.
server = 'http://10.0.2.30:5000'
url_parentalcontrol = '/renemaapps/parentalcontrol/policies'
url_networkstatus = '/renemaapps/networkstatus'
headers = {'content-type': 'application/json'}

# Format used to define a policy:
policy_post = {
    	'device':'00:16:3e:18:51:9f',
    	'action':'block',
    	'priority':'high',
    	'schedule':[
        	{'day': 'monday', 'time': '09h00-17h00'},
        	{'day': 'sunday', 'time': '10h00-20h00'}   
    	]
	}

# Example about how a policy could be updated.
policy_put = {
    	'priority':'high',
    	'schedule':[
        	{'day': 'tuesday', 'time': '15h00-21h00'},  
    	]
	}

# Method to ask the user if the program should continue running.	
def checking():
	choice = raw_input('\n\t*Continue: y or n?')
	if choice == 'y':
		pass
	else:
		os.system('clear')
		sys.exit()


while True:

		# RENEMA Apps Menu
		os.system('clear')
		print '\n---RENEMA App Client Emulator:'
		print '\n\tApps:'
		print '\t1: Parental Control(+)'
		print '\t2: Network Status(+)'
		print '\t3: Exit'

		option = int(raw_input('\n\t*Select an Option:'))

		# Parental Control App available options.
		if option == 1:
			os.system('clear')
			print '\n(+)Parental Control (REST API):\n'
			print '\t1: Get Policies'
			print '\t2: Get a Device Policy'
			print '\t3: Define a Policy'
			print '\t4: Update a Policy'
			print '\t5: Delete a Policy'
			print '\t6: Clear Policies'
			print '\t7: Push Notification'

			choice = int(raw_input('\n\t*Select an Option:'))
			os.system('clear')

			if choice == 1:
				response = requests.get(server + url_parentalcontrol)
				print response.text
				checking()

			elif choice == 2:
				mac = raw_input('\n\t*Type the MAC address to retrieve the policy:')
				os.system('clear')
				response = requests.get(server + url_parentalcontrol + '/' + mac)
				print response.text
		  		checking()

			elif choice == 3:
				mac = raw_input('\n\t*Type the MAC address to define the policy:')
				action = raw_input('\n\t*Type the action (block | allow):')
				priority = raw_input('\n\t*Type the priority (low | medium | high):')
				os.system('clear')
				policy_post['device'] = mac
				policy_post['action'] = action
				policy_post['priority'] = priority
				new_policy = requests.post(server + url_parentalcontrol, data=json.dumps(policy_post), headers=headers)
				print new_policy.text
				checking()

			elif choice == 4:
				mac = raw_input('\n\t*Type the MAC address to update the policy:')
				action = raw_input('\n\t*Type the action (block | allow):')
				priority = raw_input('\n\t*Type the priority (low | medium | high):')
				os.system('clear')
				policy_post['device'] = mac
				policy_post['action'] = action
				policy_post['priority'] = priority
				updated_policy = requests.put(server + url_parentalcontrol + '/' + mac, data=json.dumps(policy_post), headers=headers)
				print updated_policy.text
				checking()

			elif choice == 5:
				mac = raw_input('\n\t*Type the MAC address to delete the policy:')
				os.system('clear')
				deleted_policy = requests.delete(server + url_parentalcontrol + '/' + mac)
				print deleted_policy.text
				checking()

			elif choice == 6:
				response = requests.get(server + url_parentalcontrol + '/clear')
				print response.text
		  		checking()

		# Network Status App available options.
		elif option == 2:
			os.system('clear')
			print '\n(+)Network Status (REST API):'
			print '\t1: Get Stats'
			print '\t2: Get Device Stats '
			print '\t3: Get Network Resources'
			print '\t4: Get Device Resources'
			print '\t5: Get Devices State'
			print '\t6: Get Device State'
			print '\t7: Push Notification'

			choice = int(raw_input('\n\t*Select an Option:'))
			os.system('clear')

			if choice == 1:
				response = requests.get(server + url_networkstatus + '/stats')
				print response.text
				checking()

			if choice == 2:
				mac = raw_input('\n\t*Type the MAC address to retrieve the Stats:')
				os.system('clear')
				response = requests.get(server + url_networkstatus + '/stats/' + mac)
				print response.text
				checking()

			if choice == 3:
				response = requests.get(server + url_networkstatus + '/resources')
				print response.text
				checking()

			if choice == 4:
				mac = raw_input('\n\t*Type the MAC address to retrieve the Resources State:')
				os.system('clear')
				response = requests.get(server + url_networkstatus + '/resources/' + mac)
				print response.text
				checking()

			if choice == 5:
				response = requests.get(server + url_networkstatus + '/devices')
				print response.text
				checking()

			if choice == 6:
				mac = raw_input('\n\t*Type the MAC address to retrieve the State:')
				os.system('clear')
				response = requests.get(server + url_networkstatus + '/devices/' + mac)
				print response.text
				checking()


		elif option == 3:
			os.system('clear')
			sys.exit()


		else:
			print '\n*Invalid option, try again!!!'
