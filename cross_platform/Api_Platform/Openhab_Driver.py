####################################################################################
######## This part for the docs of this program ####################################
'''
.
. 	thing_global_id = platform_id + thing_local_id
. 	item_global_id  = platform_id + thing_local_id + item_local_id
. 	A item without things seemly as a thing
.
'''


import paho.mqtt.client as mqtt
import json
from requests import get
import hashlib
from openhab import openHAB
import urllib
import numpy as np


platform_id = "openHAB"
# host = "localhost"
host = "25.43.45.205"
port = "8080"
base_url = "http://" + host + ":" + port + "/rest"
pre_info = None

broker_address = "broker.hivemq.com"
clientMQTT = mqtt.Client("openHAB_Driver")  # create new instance
clientMQTT.connect(broker_address)  # connect to broker

openhab = openHAB(base_url)

# things = get(thing_url).json()
# item_name = things[0]["channels"][0]["linkedItems"][0]

# item = openhab.get_item(item_name)

# item_url = "http://" + host + ":" + port + "/rest/items?recursive=false"
# items = get(item_url).json()

# print (items)


def get_states():

	try:
		thing_url = "http://" + host + ":" + port + "/rest/things"
		things = get(thing_url).json()
		openhab = openHAB(base_url)
	except:
		get_states()



	states = []
	item_of_thing_list = []

	# Get all things in openHAB

	# print (things)

	# Get all items in openHAB
	items = openhab.fetch_all_items() # dict of openHAB items
	items = items.items()	# convert dict into list
	items = np.asarray(items)

	items_list = list(items[:, 0])
	# print (items_list)


	# Get all things and items of things in openHAB
	for thing in things:
		# print (thing)
		thing_type = thing["thingTypeUID"]
		# print (thing_type)
		thing_name = thing["label"]
		thing_local_id = thing["UID"]
		thing_global_id = platform_id + "/" + thing_local_id
		thing_location = thing["location"]
		linked_items = thing["channels"]
		items_state = []

		for linked_item in linked_items:
			item_type = linked_item["itemType"]
			item_name = linked_item["linkedItems"][0]
			item_of_thing_list.append(item_name)	# Get all item of things.
			# item_local_id  = linked_item["uid"]
			item_local_id = item_name
			item_global_id = platform_id + "/" + thing_local_id + "/" + item_local_id
			item_url = "http://" + host + ":" + port + "/rest/items?recursive=false"
			item = openhab.get_item(item_name)
			item_state = str(item.state)
			can_set_state = True
			items_state.append({
				'item_type': str(item_type),
				'item_name': str(item_name),
				'item_global_id': str(item_global_id),
				'item_local_id': str(item_local_id),
				'item_state': str(item_state),
				'can_set_state': str(can_set_state)
			}
			)


		state = {
			'thing_type': str(thing_type),
			'thing_name': str(thing_name),
			'thing_global_id': str(thing_global_id),
			'thing_local_id': str(thing_local_id),
			'location': str(thing_location),
			'items': items_state
		}
		states.append(state)

	# Get items not belong thing
	remain_item_list = list(set(items_list) - set(item_of_thing_list))
	# print (remain_item_list)

	# Those items above be converted to things
	for item_to_thing in remain_item_list:
		item = openhab.get_item_raw(item_to_thing)

		item_type = item['type']; thing_type = item_type
		item_name = item['name']; thing_name = item_name
		item_state = item['state']
		item_local_id = item_name; thing_local_id = thing_name
		thing_global_id = platform_id + '/' + thing_local_id
		item_global_id = platform_id + '/' + thing_local_id + '/' + item_local_id
		location = 'unknown'
		can_set_state = True

		items_state = [
			{
				'item_type': str(item_type),
				'item_name': str(item_name),
				'item_global_id': str(item_global_id),
				'item_local_id': str(item_local_id),
				'item_state': str(item_state),
				'can_set_state': str(can_set_state)
			}
		]

		state = {
			'thing_type': str(thing_type),
			'thing_name': str(thing_name),
			'thing_global_id': str(thing_global_id),
			'thing_local_id': str(thing_local_id),
			'location': str(thing_location),
			'items': items_state
		}

		states.append(state)

	list_thing = {
		'platform_id': platform_id,
		'things': states
	}


	return list_thing

def check_configuration_changes():
	global pre_info

	print('Check for changes')
	item_of_thing_list = []
	now_info = []
	try:
		thing_url = "http://" + host + ":" + port + "/rest/things"
		things = get(thing_url).json()
	except:
		check_configuration_changes()

	# Get all items in openHAB
	items = openhab.fetch_all_items() # dict of openHAB items
	items = items.items()	# convert dict into list
	items = np.asarray(items)

	items_list = list(items[:, 0])



	for thing in things:
		# print (thing)
		thing_type = thing["thingTypeUID"]
		# print (thing_type)
		thing_name = thing["label"]
		thing_local_id = thing["UID"]
		thing_global_id = platform_id + "/" + thing_local_id
		thing_location = thing["location"]
		linked_items = thing["channels"]
		items_state = []

		for linked_item in linked_items:
			item_type = linked_item["itemType"]
			item_name = linked_item["linkedItems"][0]
			# item_local_id  = linked_item["uid"]
			item_of_thing_list.append(item_name)	# Get all item of things.
			item_local_id = item_name
			item_global_id = platform_id + "/" + thing_local_id + "/" + item_local_id
			item_url = "http://" + host + ":" + port + "/rest/items?recursive=false"
			item = openhab.get_item(item_name)
			item_state = item.state
			can_set_state = True
			items_state.append(
				{
					'item_type': str(item_type),
					'item_name': str(item_name),
					'item_global_id': str(item_global_id),
					'item_local_id': str(item_local_id),
					'can_set_state': str(can_set_state)
				}
			)


		state = {
			'thing_type': str(thing_type),
			'thing_name': str(thing_name),
			'thing_global_id': str(thing_global_id),
			'thing_local_id': str(thing_local_id),
			'location': str(thing_location),
			'items': items_state
		}
		now_info.append(state)


	remain_item_list = list(set(items_list) - set(item_of_thing_list))
	# print (remain_item_list)

	# Those items above be converted to things
	for item_to_thing in remain_item_list:
		item = openhab.get_item_raw(item_to_thing)

		item_type = item['type']; thing_type = item_type
		item_name = item['name']; thing_name = item_name
		item_state = item['state'];
		item_local_id = item_name; thing_local_id = thing_name
		thing_global_id = platform_id + '/' + thing_local_id
		item_global_id = platform_id + '/' + thing_local_id + '/' + item_local_id
		location = 'unknow'
		can_set_state = True

		items_state = [
			{
				'item_type': str(item_type),
				'item_name': str(item_name),
				'item_global_id': str(item_global_id),
				'item_local_id': str(item_local_id),
				# 'item_state': str(item_state),
				'can_set_state': str(can_set_state)
			}
		]

		state = {
			'thing_type': str(thing_type),
			'thing_name': str(thing_name),
			'thing_global_id': str(thing_global_id),
			'thing_local_id': str(thing_local_id),
			'location': str(thing_location),
			'items': items_state
		}

		now_info.append(state)

	# print (now_info)

	hash_now = hashlib.sha256(str(now_info).encode())
	hash_pre = hashlib.sha256(str(pre_info).encode())
	if hash_now.hexdigest() == hash_pre.hexdigest():
		return [True, 'No Change', platform_id]
	else:
		pre_info = now_info
		return [False, now_info, platform_id]

def set_states(thing_local_id, item_local_id, thing_type, item_type, state):
	item = openhab.get_item(item_local_id)
	item.command(state)


def init():
	print('Init and get platform_id from Registry')
	message = {
		'platform': 'openHAB',
		'host': host,
		'port': port,
	}

	try:
		clientMQTT.publish('registry/request/api_add_platform', json.dumps(message))
		topic_response = 'registry/response/' + host + '/' + port
	except:
		init()

	def handle_init(client, userdata, msg):
		print('Handle_init')
		global platform_id
		platform_id = json.loads(msg.payload.decode('utf-8'))['platform_id']
		print ('Platform_id recived: ', platform_id)
		clientMQTT.unsubscribe(topic_response)

		clientMQTT.subscribe(str(platform_id) + '/request/api_get_states')
		clientMQTT.message_callback_add(str(platform_id) + '/request/api_get_states', api_get_states)

		clientMQTT.subscribe(str(platform_id) + '/request/api_check_configuration_changes')
		clientMQTT.message_callback_add(str(platform_id) + '/request/api_check_configuration_changes', api_check_configuration_changes)

		clientMQTT.subscribe(str(platform_id) + '/request/api_set_state')
		clientMQTT.message_callback_add(str(platform_id) + '/request/api_set_state', api_set_state)

	clientMQTT.subscribe(topic_response)
	clientMQTT.message_callback_add(topic_response, handle_init)


def api_get_states(client, userdata, msg):
	try:
		caller = json.loads(msg.payload.decode('utf-8'))['caller']
		clientMQTT.publish('driver/response/filter/api_get_states', json.dumps(get_states()))
	except:
		pass


def api_check_configuration_changes(client, userdata, msg):
	try:
		caller = json.loads(msg.payload.decode('utf-8'))['caller']
		print('api_check_configuration_changes')
		clientMQTT.publish('driver/response/forwarder/api_check_configuration_changes', str(check_configuration_changes()))
	except:
		pass

def api_set_state(client, userdata, msg):
	# topic_set_state = platform_id + '/request/api_set_state'
	# clientMQTT.subscribe(topic_set_state)
	# clientMQTT.message_callback_add(topic_set_state, handle_set_state)

	# def handle_set_state(client, userdata, msg):
	# 	thing_local_id = json.loads(msg.payload.decode('utf-8'))['thing_local_id']
	# 	item_local_id  = json.loads(msg.payload.decode('utf-8'))['item_local_id']
	# 	item_name      = json.loads(msg.payload.decode('utf-8'))['item_name']
	# 	state = json.loads(msg.payload.decode('utf-8'))['state']

	#   		set_states(thing_local_id, item_local_id, item_name, 1, 1, state)

	thing_local_id = json.loads(msg.payload.decode('utf-8'))['thing_local_id']
	item_local_id  = json.loads(msg.payload.decode('utf-8'))['item_local_id']
	item_name      = json.loads(msg.payload.decode('utf-8'))['item_name']
	state = json.loads(msg.payload.decode('utf-8'))['new_state']

	try:
		set_states(thing_local_id, item_local_id, 1, 1, state)
	except:
		pass

# clientMQTT.unsubscribe(topic_set_state)


init()
clientMQTT.loop_forever()

# [a, b] = check_configuration_changes()

# print (a)
# print (b)

# states = get_states()
# print (states)


# set_states(1, 1, "Switch1", 1, 1, "ON")