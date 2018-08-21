import paho.mqtt.client as mqtt
import json
from openhab import openHAB
from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
from kombu.utils.compat import nested
import time

base_url = 'http://192.168.60.197:8080/rest'
openhab = openHAB(base_url)

BROKER_CLOUD = "localhost"

producer_connection = Connection(BROKER_CLOUD)
consumer_connection = Connection(BROKER_CLOUD)
exchange = Exchange("IoT", type="direct")


# fetch all items
items = openhab.fetch_all_items()	# dict of openHAB items

items = list(items)


while (1):
    for item in items:
        item = openhab.get_item_raw(str(item))
        item = json.dumps(item)
        item = json.loads(item)

        item_state = item['state']
        item_type = item['type']
        item_name = item['name']
        item_id = item_name


        message = {
            'item_id' : item_id,
            'item_name' : item_name,
            'item_type' : item_type,
            'item_state' : item_state
        }

        producer_connection.ensure_connection()
        with Producer(producer_connection) as producer:
            producer.publish(
                json.dumps(message),
                exchange=exchange.name,
                routing_key='data_source.to.event_generator_2',
                retry=True
            )

        print ("Send event to Rule Engine: " + 'data_source.to.event_generator_2')

    print ("\n\n")

    time.sleep(5)

# clientMQTT = mqtt.Client()
# clientMQTT.connect("192.168.60.197")
#
#
# def send_to_event_generator(client, userdata, msg):
#     msg = json.loads(msg.payload.decode('utf-8'))
#     print ("message: ", msg)
#     clientMQTT.publish('trigger/event_generator_2', json.dumps(msg))
#
#
#
# def on_connect(client, userdata, flags, rc):
#     print("connect to Mosquitto")
#     clientMQTT.subscribe('zone_3/box_1/motion/id_1')
#     clientMQTT.message_callback_add('zone_3/box_1/motion/id_1', send_to_event_generator)
#
#     clientMQTT.subscribe('zone_3/box_1/light/id_1')
#     clientMQTT.message_callback_add('zone_3/box_1/light/id_1', send_to_event_generator)
#
#
# clientMQTT.on_connect = on_connect
# clientMQTT.loop_forever()

