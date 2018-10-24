from openhab import openHAB
import paho.mqtt.client as mqtt
import json
import time


base_url = 'http://localhost:8080/rest'
# base_url = 'http://192.168.0.197:8080/rest'
openhab = openHAB(base_url)

# fetch all items
items = openhab.fetch_all_items()
# print (items)
	
item1 = openhab.get_item("LedVang")
item2 = openhab.get_item("LedXanh")
item3 = openhab.get_item("LedDo")

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
	mes = int(mes['motion'])

	if (mes == 1):
		item1.on()
    else:
        item1.off()
		

client = mqtt.Client()
pre_motion = 0
pre_temp = 0

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
