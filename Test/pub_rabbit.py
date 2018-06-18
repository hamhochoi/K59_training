import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import ast
import json
import threading
from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
from kombu.utils.compat import nested
import time

BROKER_CLOUD = "localhost"

producer_connection = Connection(BROKER_CLOUD)
consumer_connection = Connection(BROKER_CLOUD)
MODE = "PUSH" # PUSH or PULL

exchange = Exchange("IOT", type="direct")


request_queue = Queue(name='alert_in', exchange=exchange, routing_key='alert_in')
request_routing_key = 'alert_in'
producer_connection.ensure_connection()

with Producer(producer_connection) as producer:

	message = {
        'item_global_id' : 1,
        'item_state'     : 2,
        'past_state'     : 3
    }

	producer.publish(
	json.dumps(message),
	exchange=exchange.name,
	routing_key=request_routing_key,
	declare=[request_queue],
	retry=True
	)
	time.sleep(3)

print ("Send alert!")
