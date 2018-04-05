#!usr/bin/python
import json, os
from flask import Flask, jsonify, abort, make_response, request
from ManagementLayer.RenemaApps.NetworkStatus import NetworkStatus
from ManagementLayer.RenemaApps.ParentalControl import ParentalControl


app = Flask(__name__)


#---------------------------------------------------------------------------------
#------------------------------PARENTAL CONTROL APP-------------------------------

@app.route('/renemaapps/parentalcontrol/policies', methods=['GET'])
def get_policies():

	policies = ParentalControl().get_policies()

	if len(policies) is 0:
		return jsonify({'policies': policies, 'attention': 'Create a policy'})

	return jsonify({'policies': policies})
#---------------------------------------------------------------------------------

@app.route('/renemaapps/parentalcontrol/policies/<device>', methods=['GET'])
def get_policy(device):
    
    policy = ParentalControl().get_policy(device)
    
    if len(policy) == 0:
        abort(404)
    
    return jsonify({'policy': policy[0]})
#---------------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(error):
    
    return make_response(jsonify({'Error': 'Not found'}), 404)
#---------------------------------------------------------------------------------

@app.route('/renemaapps/parentalcontrol/policies', methods=['POST'])
def define_policy():
    
	if not request.json or not 'device' in request.json:
		abort(400)

	policy = {
        	'device': request.json['device'],    
        	'action': request.json['action'],
        	'priority': request.json.get('priority', 'low'),    # This option allows tolerating a missing "priority" field by means of configuring  
        														# a default value of "low".
        	'schedule': request.json['schedule']
		}
	
	ParentalControl().define_policy(policy)
	
	return jsonify({'policy': policy}), 201
#---------------------------------------------------------------------------------

@app.route('/renemaapps/parentalcontrol/policies/<device>', methods=['PUT'])
def update_policy(device):
	
	policy = ParentalControl().get_policy(device)

	if len(policy) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'action' in request.json and type(request.json['action']) != unicode:
		abort(400)
	if 'priority' in request.json and type(request.json['priority']) is not unicode:
		abort(400)
	#if 'schedule' in request.json and type(request.json['schedule']) is not unicode:
	#	abort(404)

	policy[0]['action'] = request.json.get('action', policy[0]['action'])
	policy[0]['priority'] = request.json.get('priority', policy[0]['priority'])
	policy[0]['schedule'] = request.json.get('schedule', policy[0]['schedule'])

	ParentalControl().update_policy(device, policy[0])

	return jsonify({'policy': policy[0]})
#---------------------------------------------------------------------------------

@app.route('/renemaapps/parentalcontrol/policies/<device>', methods=['DELETE'])
def delete_policy(device):

	policy = ParentalControl().get_policy(device)
    
	if len(policy) == 0:
		abort(404)

	ParentalControl().delete_policy(device)

	return jsonify({'device': device, 'result': 'The policy has been deleted'})
#---------------------------------------------------------------------------------

@app.route('/renemaapps/parentalcontrol/policies/clear', methods=['GET'])
def clear_policies():

	ParentalControl().clear_policies()
	NetworkStatus().clear_status()
	return jsonify({'result': 'all policies have been deleted'})
#---------------------------------------------------------------------------------

@app.route('/renemaapps/parentalcontrol/policies/notification', methods=['GET'])
def push_notification_parentalcontrol():

	# Method used to inform users about notifications.
	# "PUSH notifications"

	return jsonify({'result': 'Push Notification parental_control'})
#---------------------------------------------------------------------------------
#---------------------------------------------------------------------------------

#-----------------------------NETWORK STATUS APP----------------------------------

@app.route('/renemaapps/networkstatus/stats', methods=['GET'])
def get_stats():

	# Method used to get the devices stats.
	devices_stats = NetworkStatus().devices_stats()

	if len(devices_stats) == 0:
		abort(404)

	return jsonify({'Statistics':devices_stats})
#---------------------------------------------------------------------------------

@app.route('/renemaapps/networkstatus/stats/<device>', methods=['GET'])
def get_device_stats(device):

	# Method used to get the device stats.
	device_stats = NetworkStatus().device_stats(device)

	return jsonify({'Statistics':device_stats})
#---------------------------------------------------------------------------------

@app.route('/renemaapps/networkstatus/resources', methods=['GET'])
def get_resources():

	# Method used to get the network resources (Total BW).
	network_resources = NetworkStatus().network_resources()

	if len(network_resources) == 0:
		abort(404)

	return jsonify({'Network Resources': network_resources})
#---------------------------------------------------------------------------------

@app.route('/renemaapps/networkstatus/resources/<device>', methods=['GET'])
def get_device_resources(device):

	# Method used to get the device resources (BW per device: port, BW per running service).
	device_resources = NetworkStatus().device_resources(device)

	return jsonify({'Device Resources State': device_resources})
#---------------------------------------------------------------------------------

@app.route('/renemaapps/networkstatus/devices', methods=['GET'])
def get_devices():

	# Method used to get the devices status (online and offline devices list).
	devices_state = NetworkStatus().devices_state()

	if len(devices_state) is not 0:
		return jsonify({'Devices State': devices_state})
	else:
		return jsonify({'Warning!':'No devices connected'})
#---------------------------------------------------------------------------------

@app.route('/renemaapps/networkstatus/devices/<device>', methods=['GET'])
def get_device(device):

	# Method used to get the device state (device, port, policy: defined or not, state: online or offline).
	device_state = NetworkStatus().device_state(device)
    
	if len(device_state) == 0:
		abort(404)
    
	return jsonify({'Device State': device_state[0]})
#---------------------------------------------------------------------------------

@app.route('/renemaapps/networkstatus/devices/notification', methods=['GET'])
def push_notification_networkstatus():

	# Method used to inform users about notifications.
	# "PUSH notifications"

	return jsonify({'result': 'Push Notification network_status'})
#---------------------------------------------------------------------------------

@app.route('/shutdown', methods=['POST'])
def shutdown():
	shutdown_server()
	return 'Server shutting down...'
#---------------------------------------------------------------------------------

def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
#---------------------------------------------------------------------------------

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)