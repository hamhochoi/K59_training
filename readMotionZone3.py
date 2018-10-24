import paho.mqtt.client as mqtt
import time
from datetime import datetime

#f = open("time_pin.txt", "a")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("zone_3/box_1/motion/id_1")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload) + " " + str(datetime.now()))
    f = open("time_pin_zone3.txt", "a")
    f.write(str(msg.payload) + " " + str(datetime.now()))
    f.write("\n")
    f.close()
    time.sleep(5*60)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)



client.loop_forever()

