import datetime
import json
import threading
from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
from kombu.utils.compat import nested

BROKER_CLOUD = "192.168.60.248"

producer_connection = Connection(BROKER_CLOUD)
consumer_connection = Connection(BROKER_CLOUD)

exchange = Exchange("IoT", type="direct")

def handle_notification(body, message):
    print('Have Alert')

    # message = {
    #     'item_global_id' : json.loads(body)['item_global_id'],
    #     'item_state'     : json.loads(body)['item_state'],
    #     'past_state'     : json.loads(body)['past_state'],
    #     'content'        : "Data get wrong"
    # }
    #
    # request_queue = Queue(name='alert.api_get_state', exchange=exchange, routing_key='alert.api_get_state')
    # request_routing_key = 'alert.api_get_state'
    # producer_connection.ensure_connection()
    # with Producer(producer_connection) as producer:
    #     producer.publish(
    #         json.dumps(message),
    #         exchange=exchange.name,
    #         routing_key=request_routing_key,
    #         declare=[request_queue],
    #         retry=True
    #     )

    f = open("logs.txt", "a")
    f.write("Time: " + str(datetime.datetime.now()) + ", item_global_id: " + str(json.loads(body)['item_global_id']) + ", item_state: " + str(json.loads(body)['item_state']))
    f.write("\n")
    f.close()

    print('Send alert to Fluentd')

def run():
    queue_notification = Queue(name='monitor.request.alert', exchange=exchange,
                               routing_key='monitor.request.alert', message_ttl=20)

    while 1:
        try:
            consumer_connection.ensure_connection(max_retries=1)
            with nested(Consumer(consumer_connection, queues=queue_notification, callbacks=[handle_notification],
                                 no_ack=True)):
                while True:
                    consumer_connection.drain_events()
        except (ConnectionRefusedError, exceptions.OperationalError):
            print('Connection lost')
        except consumer_connection.connection_errors:
            print('Connection error')


run()



