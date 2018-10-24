from openhab import openHAB
import paho.mqtt.client as mqtt
import json
import time


# base_url = 'http://localhost:8080/rest'
base_url = 'http://192.168.60.197:8080/rest'
openhab = openHAB(base_url)

# fetch all items
items = openhab.fetch_all_items()
# print (items)
	
item1 = openhab.get_item("Switch1")		# Den vang
item2 = openhab.get_item("Switch2")		# Den do
item3 = openhab.get_item("Switch3")		# Den xanh

temp_item = openhab.get_item("Temperature")
light_item = openhab.get_item("Light")
light_state = light_item.state

topic_sub_sensor = "zone_3/box_1/motion/id_1"
def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
	client.subscribe(topic_sub_sensor)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	global pre_motion
	
	mes = json.loads(str(msg.payload))
	mes = mes['motion']

	if (mes == 1 and pre_motion == 0):
		# pre_motion = mes
		light_state = light_item.state
		print (light_state)
		if (light_state == 0):				# LDRReading < 500
			item1.on()						# Bat den vang
			time.sleep(0.5)
			item2.off()
			time.sleep(0.5)
			item3.off()
			print ("Vang: ON, Do: OFF, Xanh: OFF")
		elif (light_state == 1):			# LDRReading >= 500 <600
			item1.off()
			time.sleep(0.5)
			item2.on()						# Bat den do
			time.sleep(0.5)
			item3.off()
			print ("Vang: OFF, Do: ON, Xanh: OFF")	
		elif (light_state == 2):			# LDRReading >= 600
			item1.off()
			time.sleep(0.5)
			item2.off()
			time.sleep(0.5)
			item3.on()						# Bat den xanh
			print ("Vang: OFF, Do: OFF, Xanh: ON")	
		else:
			print ("ERROR!")
			exit()

client = mqtt.Client()
pre_motion = 0
pre_temp = 0

client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.60.199", 1883, 60)
client.loop_forever()
