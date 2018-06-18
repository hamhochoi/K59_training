import ast
import json
import threading
from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
from kombu.utils.compat import nested
from influxdb import InfluxDBClient

clientDB = InfluxDBClient('localhost', 8086, 'root', 'root', 'Collector_DB')
clientDB.create_database('Collector_DB')

BROKER_CLOUD = "localhost"

producer_connection = Connection(BROKER_CLOUD)
consumer_connection = Connection(BROKER_CLOUD)
exchange = Exchange("IoT", type="direct")

# n_record = 10

def get_item_state(list_item_global_id, n_record):
    items = []
    # list_state = []
    for item_global_id in list_item_global_id:
        print ("item global id: ", item_global_id)
        query_statement = 'SELECT * FROM \"' + item_global_id + '\" ORDER BY time DESC LIMIT ' + str(n_record)
        query_result = clientDB.query(query_statement)
        # print ("query result: ", query_result)

        for item in query_result:
            # print ("item: ", item)
            # print ("")
            for iter in range(n_record):
                item_state = {
                    'item_global_id': item[iter]['item_global_id'],
                    'item_state': item[iter]['item_state'],
                    'last_changed': item[iter]['time'],
                    'thing_global_id': item[iter]['thing_global_id']
                }
                # list_state.append(item_state)

                items.append({'item_global_id':item_global_id, 'item_state':item_state})
    print ("items: ", items)
    print ("")
    return items


def api_get_item_state(body, message):
    print("API get_item_state")
    # Message {'list_item_global_id': [], 'reply_to': " ", }
    list_item_global_id = json.loads(body)["list_item_global_id"]
    reply_to = json.loads(body)['reply_to']
    n_record = json.loads(body)['n_record']
    items = get_item_state(list_item_global_id, n_record)
    # print ("send items: ", items)
    # print ("")
    message_response = {
        "items": items
    }
    producer_connection.ensure_connection()
    with Producer(producer_connection) as producer:
        producer.publish(
            json.dumps(message_response),
            exchange=exchange.name,
            routing_key=reply_to,
            retry=True
        )
    print("Done: {}".format(items))


queue_get_item_state = Queue(name='dbreader.request.api_get_item_state', exchange=exchange, routing_key='dbreader.request.api_get_item_state')

while 1:
    try:
        consumer_connection.ensure_connection(max_retries=1)
        with Consumer(consumer_connection, queues=queue_get_item_state, callbacks=[api_get_item_state], no_ack=True):
            while True:
                consumer_connection.drain_events()
    except (ConnectionRefusedError, exceptions.OperationalError):
        print('Connection lost')
    except consumer_connection.connection_errors:
        print('Connection error')
