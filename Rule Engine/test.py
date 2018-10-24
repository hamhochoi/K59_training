# import MySQLdb
# db = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root", db="RuleEngine_DB")
# cursor = db.cursor()
# request = "Select * from Item_State where item_id='" + 'item_id_1' + "' order by time desc limit 2"
#
# cursor.execute(request)
# result = cursor.fetchall()
#
# item_state = result[0]
#
# # print (result)
# print (item_state[0])


'''


from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
from kombu.utils.compat import nested
import datetime
import json
from random import  *

BROKER_CLOUD = "localhost"
producer_connection = Connection(BROKER_CLOUD)
consumer_connection = Connection(BROKER_CLOUD)
exchange = Exchange("IoT", type="direct")



message = {
    'item_name' : "temperature",
    'item_id' : "940347de-8cd8-417f-b0b3-0d63d1d47278",
    "item_type" : "int",
    "item_state" : "60",
    "last_changed" : str(datetime.datetime.now())
}


producer_connection.ensure_connection()
with Producer(producer_connection) as producer:
    producer.publish(
        json.dumps(message),
        exchange=exchange.name,
        routing_key='data_source.to.event_generator_2',
        retry=True
    )

message = {
    'item_name' : "Humidity",
    'item_id' : "0f3ecd50-c870-464c-a4cf-76b5e8b34874",
    "item_type" : "int",
    "item_state" : "60",
    'last_changed' : str(datetime.datetime.now())
}


producer_connection.ensure_connection()
with Producer(producer_connection) as producer:
    producer.publish(
        json.dumps(message),
        exchange=exchange.name,
        routing_key='data_source.to.event_generator_2',
        retry=True
    )

message = {
    'item_name' : "Temperature",
    'item_id' : "04fa6c2b-6fc3-4c61-ae53-4a9cc2188090",
    "item_type" : "int",
    "item_state" : "60",
    'last_changed' : str(datetime.datetime.now())
}


producer_connection.ensure_connection()
with Producer(producer_connection) as producer:
    producer.publish(
        json.dumps(message),
        exchange=exchange.name,
        routing_key='data_source.to.event_generator_2',
        retry=True
    )

# points = []
#
# points.append({
#     "MetricId": "c3198475-06d0-4aec-9516-b9c69a911ca7",
#     "MetricLocalId" : "Temperature",
#     "DataPoint" : {
#         "DataType": "int",
#         "Value": "30"
#     },
#     "TimeCollect": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# })
#
# message = {
#     'header': {},
#     'body': {
#         'states': points
#     }
# }
#
#
# producer_connection.ensure_connection()
# with Producer(producer_connection) as producer:
#     producer.publish(
#         json.dumps(message),
#         exchange=exchange.name,
#         routing_key='rule.request.states',
#         retry=True
#     )


print ("Sent!")

'''

"""
from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
from kombu.utils.compat import nested
import datetime
import json
from random import  *

BROKER_CLOUD = "25.29.146.11"
producer_connection = Connection(BROKER_CLOUD)
consumer_connection = Connection(BROKER_CLOUD)
exchange = Exchange("IoT", type="direct")

queue_get_states = Queue(name='driver.response.collector.api_get_states', exchange=exchange,
                         routing_key='driver.response.collector.api_get_states', message_ttl=20)


def handle_notification(body, message):
    # print (message)
    states = json.loads(body)['body']['states']
    print (states)

while (1):
    try:
        consumer_connection.ensure_connection(max_retries=1)
        with nested(Consumer(consumer_connection, queues=queue_get_states,
                             callbacks=[handle_notification], no_ack=True)
                    ):
            while True:
                consumer_connection.drain_events()
    except (ConnectionRefusedError, exceptions.OperationalError):
        print('Connection lost')
    except consumer_connection.connection_errors:
        print('Connection error')

"""

import paho.mqtt.client as mqtt
