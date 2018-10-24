import json
import socket
from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
from kombu.utils.compat import nested
import requests
import time


BROKER_CLOUD = "localhost"
rule_api_host = "http://127.0.0.1:5000/rule"
producer_connection = Connection(BROKER_CLOUD)
consumer_connection = Connection(BROKER_CLOUD)

exchange = Exchange("IoT", type="direct")


def send_to_monitor():
    message = requests.get(rule_api_host)
    message = message.json()

    print ("received data:", message)

    producer_connection.ensure_connection()
    with Producer(producer_connection) as producer:
        producer.publish(
            json.dumps(message),
            exchange=exchange.name,
            routing_key='monitor.request.rule_engine',
            retry=True
        )
    print ("Send to Monitor_DB")


while(1):
    try:
        send_to_monitor()
        time.sleep(20)
    except:
        time.sleep(5)