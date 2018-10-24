from openhab import openHAB
import paho.mqtt.client as mqtt
import json
import time

base_url = 'http://192.168.0.197:8080/rest'
openhab = openHAB(base_url)
items = openhab.fetch_all_items()



item1 = openhab.get_item("LedXanh")
item2 = openhab.get_item("LedVang")
item3 = openhab.get_item("LedDo")

temp_item = openhab.get_item("Temperature")
light_item = openhab.get_item("Light")
light_state = light_item.state

topic_sub_sensor = "zone_3/box_1/motion/id_1"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic_sub_sensor)

def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload))
    mes = json.loads(msg.payload.decode('utf-8'))
    mes = int(mes['motion'])
    print (mes)

    if (mes == 1):
        item1.command("ON")
        print (item1.state)
        time.sleep(1)
    else:
        item1.command("OFF")
        print (item1.state)
        time.sleep(1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.197", 1883, 60)
client.loop_forever()