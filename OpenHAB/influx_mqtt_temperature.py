import paho.mqtt.client as mqtt
import datetime
import time
from influxdb import InfluxDBClient
import json


topic_sub_sensor = "zone_3/box_1/light/id_1"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic_sub_sensor)

def on_message(client, userdata, msg):
    # Use utc as timestamp
    receiveTime=datetime.datetime.utcnow()
    message=json.loads(str(msg.payload))
    light=message['light']
    temperature= message['temperature']
    humidity=message['humidity']

    print(str(receiveTime) + ": " + msg.topic + " light: " + str(light) + " temperature: " + str(temperature) + " humidity: " + str(humidity))

    json_body = [
        {
            "measurement": msg.topic,
            "time": receiveTime,
            "fields": {
                "light": light,
                "temperature": temperature,
                "humidity": humidity
            }
        }
    ]

    dbclient.write_points(json_body)

# Set up a client for InfluxDB
dbclient = InfluxDBClient('localhost', port=8086, database='openhab')

# Initialize the MQTT client that should connect to the Mosquitto broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
connOK=False
while(connOK == False):
    try:
        client.connect("192.168.60.199", 1883, 60)
        connOK = True
    except:
        connOK = False
    time.sleep(2)

# Blocking loop to the Mosquitto broker
client.loop_forever()
