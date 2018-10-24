import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import ast
import json
import threading
from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
from kombu.utils.compat import nested
import _thread
import time
import os
from multiprocessing import Process


BROKER_CLOUD = "localhost"
host_api_set_state = "http://localhost:5000/api/items"

clientDB = InfluxDBClient('localhost', 8086, 'root', 'root', 'Collector_DB')

producer_connection = Connection(BROKER_CLOUD)
consumer_connection = Connection(BROKER_CLOUD)
MODE = "PUSH" # PUSH or PULL

exchange = Exchange("IoT", type="direct")

TIME_COLLECT = 5

list_platform_id = []
list_past_item = []             # Use to store past items
wait_for_alert = []             # Use as a flag to alert
list_current_items = []                 # Use to store current items
n_record = 10
upper_threshold = 1.5
lower_threshold = 0.5

list_rule = []


def monitor():
    global list_current_items
    global list_rule

    print ("Monitoring...")
    # print ("list current items: ", list_current_items)

    for rule in list_rule:
        things           = rule['rule_condition']['bitwise']['things']
        bitwise_operator = rule['rule_condition']['bitwise']['bitwise_operator']
        bitwise          = rule['rule_condition']['bitwise']['bitwise']
        actions          = rule['rule_action']
        rule_name        = rule['rule_name']

        result = check_rule_condition(things, bitwise_operator, bitwise)

        print ("(rule name, result) : ", rule_name, result)


        if (result == True):
            for action in actions:
                thing_global_id = action['thing_global_id']
                item_global_id  = action['item_global_id']
                new_state       = action['new_state']
                action_name     = action['action_name']
                # timer           = action['timer']

                if (action_name == "update"):
                    print ("api set state")
                    #api_set_state(thing_global_id, item_global_id, new_state)
                    time.sleep(3)
                elif (action_name == "send_alert"):
                    send_alert(item_global_id, item_state=None, past_state=None)


def request_past_things_info(query_statement):

    message = {
        'query_statement' : query_statement,
        'reply_to' : 'dbreader.respond.monitor',
    }

    producer_connection.ensure_connection()
    with Producer(producer_connection) as producer:
        producer.publish(
            json.dumps(message),
            exchange=exchange.name,
            routing_key='dbreader.request.api_get_item_state_custom',
            retry=True
        )
    print ("Send request to DBreader")


    # query_result = []
    # global query_result

    # Wait for message from Dbreader and get the query_result
    # while (query_result == None):
    #     global query_result

    # return  query_result

def get_past_state_by_global_id(item_global_id, timer):
    query_statement = 'select item_state from \"' + item_global_id + '\" where time > now() - ' + timer
    # query_result = clientDB.query(query_statement)

    request_past_things_info(query_statement)
    global query_result
    # print ("query result: ", query_result)

    past_state = []
    for item in query_result:
        for i in range(len(item)):
            # print ("past state: ", item[i]['item_state'])
            past_state.append(item[i]['item_state'])

    return past_state


def api_set_state(thing_global_id, item_global_id, new_state):
    message = {
        "thing_global_id" : thing_global_id,
        "item_global_id"  : item_global_id,
        "new_state"       : new_state
    }

    os.system("curl -H \"Content-type: application/json\" -X POST " + host_api_set_state + " -d" + "\'" + json.dumps(message) + "\'")


def check_condition(condition, item_state, value):
    if (condition == "EQ"):
        if (item_state == float(value)):
            return True
        else:
            return False
    elif (condition == "NEQ"):
        if (item_state != float(value)):
            return True
        else:
            return False
    elif (condition == "LT"):
        if (item_state < float(value)):
            return True
        else:
            return False
    elif (condition == "LEQ"):
        if (item_state <= float(value)):
            return True
        else:
            return False
    elif (condition == "GRT"):
        if (item_state > float(value)):
            return True
        else:
            return False
    elif (condition == "GEQ"):
        if (item_state >= float(value)):
            return True
        else:
            return False
    else:
        print ("Error: Condition is not valid!")
        return -1


def check_thing_condition(thing):
    global list_current_items

    if (len(thing) == 0):
        return True

    timer = thing['timer']
    item_global_id = thing['item_global_id']
    item_type = thing['item_type']
    operator = thing['operator']
    value = thing['value']

    result = True

    for item in list_current_items:
        # item_state = item['item_state']

        if (item_global_id == item['item_global_id']):
            past_state = get_past_state_by_global_id(item_global_id, timer)
            if (past_state == []):
                print ("Don't get past state yet!")
                continue
            else:
                print ("past state: ", past_state)
                if (item_type == "light" or item_type == "Number"):
                    try:
                        value = float(value)
                    except:
                        print ("Error: Cannot convert value to float")

                    boo = True
                    result = True
                    for item_state in past_state:
                        boo = check_condition(operator, item_state, value)
                        if (boo == False):
                            result = False
                            break

                elif (item_type == "binary_sensor"):
                    if (operator == "EQ"):
                        boo = True
                        result = True

                        for item_state in past_state:
                            if (item_state != value):
                                boo = False
                                result = False
                                break
                    else:
                        print ("Error: operator is not valid!")
                        return -1
                else:
                    print ("item type is not valid")

                break

    return result


def check_rule_condition(things, bitwise_operator, bitwise):

    thing_condition   = None
    bitwise_condition = None
    result  = None

    if (len(bitwise) == 0):
        thing_condition_1 = check_thing_condition(things[0])

        if (len(things) == 2):
            thing_condition_2 = check_thing_condition(things[1])

        if (bitwise_operator == "None"):
            result = thing_condition_1
        elif (bitwise_operator == "AND"):
            result = thing_condition_1 and thing_condition_2
        elif (bitwise_operator == "OR"):
            result = thing_condition_1 or thing_condition_2
        else:
            print ("Error: bitwise operator is not defined!")

    if (len(bitwise) == 1):
        bitwise_condition = check_rule_condition(bitwise[0]['things'], bitwise[0]['bitwise_operator'], bitwise[0]['bitwise'])
        thing_condition   = check_thing_condition(things[0])

        if (bitwise_operator == "AND"):
            result = thing_condition and bitwise_condition
        elif (bitwise_operator == "OR"):
            result = thing_condition or bitwise_condition
        else:
            print ("Error: bitwise operator is not defined!")


    if (len(bitwise) == 2):
        bitwise_condition_1 = check_rule_condition(bitwise[0]['things'], bitwise[0]['bitwise_operator'], bitwise[0]['bitwise'])
        bitwise_condition_2 = check_rule_condition(bitwise[1]['things'], bitwise[1]['bitwise_operator'], bitwise[1]['bitwise'])

        if (bitwise_operator == "AND"):
            result = bitwise_condition_1 and bitwise_condition_2
        elif (bitwise_operator == "OR"):
            result = bitwise_condition_1 or bitwise_condition_2
        else:
            print ("Error: bitwise operator is not defined!")

    return result


def extract_things_info(list_things):
    platform_id = list_things['platform_id']
    list_items = []
    list_item_global_id = []
    # Extract message's information
    for thing in list_things['things']:
        for item in thing['items']:
            record = {
                'item_global_id': item['item_global_id'],
                'item_state' : item['item_state']
            }
            # print ("item global id: ", item['item_global_id'])
            list_item_global_id.append(item['item_global_id'])
            list_items.append(record)

    return platform_id, list_items, list_item_global_id


def send_alert(item_global_id, item_state, past_state):
    message = {
        'item_global_id' : item_global_id,
        'item_state'     : item_state,
        'past_state'     : past_state
    }

    request_queue = Queue(name='monitor.request.alert', exchange=exchange, routing_key='monitor.request.alert')
    request_routing_key = 'monitor.request.alert'
    producer_connection.ensure_connection()

    with Producer(producer_connection) as producer:
        producer.publish(
            json.dumps(message),
            exchange=exchange.name,
            routing_key=request_routing_key,
            declare=[request_queue],
            retry=False
        )

    print ("Send alert!")


def handle_notification(body, message):
    global list_current_items

    print('Receive message from Collector')
    list_things = json.loads(body)
    platform_id, list_current_items, list_item_global_id = extract_things_info(list_things)

    try:
        # _thread.start_new_thread( monitor, () )
        p = Process(target=monitor, args=())
        p.start()
        p.join()
        time.sleep(5)

    except:
        print ("Error: unable to start thread")


def handle_dbreader_notification(body, message):
    # global list_current_items
    # global list_past_item

    print ("Receive message from DBReader!")
    print (json.loads(body))
    global query_result
    query_result = json.loads(body)['query_result']
    # print (query_result)
    global query_result


def handle_rule(body, message):
    global list_rule
    print ("Get Rule engine notification!")

    list_rule = json.loads(body)
    print (list_rule)


def run():
    queue_get_states = Queue(name='monitor.request.collector', exchange=exchange,
                             routing_key='monitor.request.collector')#, message_ttl=20)
    queue_get_past_states = Queue(name='dbreader.respond.monitor', exchange=exchange,
                                  routing_key='dbreader.respond.monitor')#, message_ttl=20)
    queue_get_rules = Queue(name='monitor.request.rule_engine', exchange=exchange,
                                      routing_key='monitor.request.rule_engine')#, message_ttl=20)
    while 1:
        try:
            consumer_connection.ensure_connection(max_retries=1)
            with nested(Consumer(consumer_connection, queues=queue_get_states,
                                 callbacks=[handle_notification], no_ack=True),
                        Consumer(consumer_connection, queues=queue_get_past_states,
                                 callbacks=[handle_dbreader_notification], no_ack=True),
                        Consumer(consumer_connection, queues=queue_get_rules,
                                                 callbacks=[handle_rule], no_ack=True)):
                while True:
                    consumer_connection.drain_events()
        except (ConnectionRefusedError, exceptions.OperationalError):
            print('Connection lost')
        except consumer_connection.connection_errors:
            print('Connection error')


run()






# import json
# import threading
# from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
# from kombu.utils.compat import nested
#
# BROKER_CLOUD = "localhost"
#
# producer_connection = Connection(BROKER_CLOUD)
# consumer_connection = Connection(BROKER_CLOUD)
# MODE = "PUSH" # PUSH or PULL
#
# exchange = Exchange("IoT", type="direct")
#
# TIME_COLLECT = 5
#
# list_platform_id = []
#
#
# def monitor():
#     print("Monitor the states of the devices")
#     for platform_id in list_platform_id:
#         collect_by_platform_id(platform_id)
#     threading.Timer(TIME_COLLECT, monitor).start()
#
#
# def collect_by_platform_id(platform_id):
#     print('Collect data from platform_id: ', str(platform_id))
#     message_request = {
#         'reply_to': 'driver.response.monitor.api_get_states',
#         'platform_id': platform_id
#     }
#
#     request_queue = Queue(name='driver.request.api_get_states', exchange=exchange, routing_key='driver.request.api_get_states')
#     request_routing_key = 'driver.request.api_get_states'
#     producer_connection.ensure_connection()
#     with Producer(producer_connection) as producer:
#         producer.publish(
#             json.dumps(message_request),
#             exchange=exchange.name,
#             routing_key=request_routing_key,
#             declare=[request_queue],
#             retry=True
#         )
#
#
# def handle_collect_by_platform_id(body, message):
#     print('Recived state from platform_id: ', json.loads(body)['platform_id'])
#
#     list_things = json.loads(body)
#     print(list_things)
#     # request_queue = Queue(name='dbwriter.request.api_write_db', exchange=exchange, routing_key='dbwriter.request.api_write_db')
#     # request_routing_key = 'dbwriter.request.api_write_db'
#     # producer_connection.ensure_connection()
#     # with Producer(producer_connection) as producer:
#     #     producer.publish(
#     #         json.dumps(list_things),
#     #         exchange=exchange.name,
#     #         routing_key=request_routing_key,
#     #         declare=[request_queue],
#     #         retry=True
#     #     )
#     #
#     # print('Send new state to Dbwriter')
#
#
# def get_list_platforms():
#     print("Get list platforms from Registry")
#     message = {
#         'reply_to': 'registry.response.monitor.api_get_list_platforms',
#         'platform_status': "active"
#     }
#
#     queue = Queue(name='registry.request.api_get_list_platforms', exchange=exchange, routing_key='registry.request.api_get_list_platforms')
#     routing_key = 'registry.request.api_get_list_platforms'
#     producer_connection.ensure_connection()
#     with Producer(producer_connection) as producer:
#         producer.publish(
#             json.dumps(message),
#             exchange=exchange.name,
#             routing_key=routing_key,
#             declare=[queue],
#             retry=True
#         )
#
#
# def handle_get_list(body, message):
#     global list_platform_id
#     list_platforms = json.loads(body)['list_platforms']
#     temp = []
#     for platform in list_platforms:
#         temp.append(platform['platform_id'])
#
#     list_platform_id = temp
#
#     print('Updated list of platform_id: ', str(list_platform_id))
#
#
# def handle_notification(body, message):
#     print('Have Notification')
#     if json.loads(body)['notification'] == 'Have Platform_id change':
#         get_list_platforms()
#
#
# # def run():
# #     queue_notification = Queue(name='monitor.request.notification', exchange=exchange,
# #                                routing_key='monitor.request.notification')
# #     queue_list_platforms = Queue(name='registry.response.monitor.api_get_list_platforms', exchange=exchange,
# #                                  routing_key='registry.response.monitor.api_get_list_platforms')
# #     queue_get_states = Queue(name='driver.response.monitor.api_get_states', exchange=exchange,
# #                              routing_key='driver.response.monitor.api_get_states')
# #
# #     # if MODE == 'PULL':
# #     #     print("Monitor use Mode: PULL Data")
# #     #     get_list_platforms()
# #     #     monitor()
# #
# #     while 1:
# #         try:
# #             consumer_connection.ensure_connection(max_retries=1)
# #             with nested(Consumer(consumer_connection, queues=queue_notification, callbacks=[handle_notification],
# #                                  no_ack=True),
# #                         Consumer(consumer_connection, queues=queue_list_platforms, callbacks=[handle_get_list],
# #                                  no_ack=True),
# #                         Consumer(consumer_connection, queues=queue_get_states,
# #                                  callbacks=[handle_collect_by_platform_id], no_ack=True)):
# #                 while True:
# #                     consumer_connection.drain_events()
# #         except (ConnectionRefusedError, exceptions.OperationalError):
# #             print('Connection lost')
# #         except consumer_connection.connection_errors:
# #             print('Connection error')
#
#
# def run():
#     queue_get_states = Queue(name='monitor.request.collector', exchange=exchange,
#                              routing_key='monitor.request.collector')
#
#     request_past_things_info(n_record)
#     get_past_info()
#
#
#     while 1:
#         try:
#             consumer_connection.ensure_connection(max_retries=1)
#             with nested(Consumer(consumer_connection, queues=queue_get_states,
#                         callbacks=[handle_notification], no_ack=True)):
#                 while True:
#                     consumer_connection.drain_events()
#         except (ConnectionRefusedError, exceptions.OperationalError):
#             print('Connection lost')
#         except consumer_connection.connection_errors:
#             print('Connection error')
#
#
#
# run()
#
#
#

# def find_condition(string):
#     condition = None
#     item_global_id = ""
#     value = 0
#
#     if (string == "True"):
#         return True
#
#     if (string == "False"):
#         return False
#
#     for i in range(len(string)):
#         if (string[i] == "="):
#             condition = "="
#             item_global_id  = string[0:i]
#             value = string[i+1::]
#         elif (string[i] == "<"):
#             if (string[i+1] == "="):
#                 condition = "<="
#                 item_global_id = string[0:i]
#                 value = string[i+2::]
#             else:
#                 condition = "<"
#                 item_global_id = string[0:i]
#                 value = string[i+1::]
#         elif (string[i] == ">"):
#             if (string[i+1] == "="):
#                 condition = ">="
#                 item_global_id = string[0:i]
#                 value = string[i+2::]
#             else:
#                 condition = ">"
#                 item_global_id = string[0:i]
#                 value = string[i+1::]
#         # else:
#         #     print ("Error: Condition not found!")
#
#     return condition, item_global_id, value
























































# import paho.mqtt.client as mqtt
# from influxdb import InfluxDBClient
# import ast
# import json
# import threading
# from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
# from kombu.utils.compat import nested
# import _thread
#
# BROKER_CLOUD = "localhost"
#
# producer_connection = Connection(BROKER_CLOUD)
# consumer_connection = Connection(BROKER_CLOUD)
# MODE = "PUSH" # PUSH or PULL
#
# exchange = Exchange("IoT", type="direct")
#
# TIME_COLLECT = 5
#
# list_platform_id = []
# list_past_item = []             # Use to store past items
# list_current_items = []                 # Use to store current items
# n_record = 1
# upper_threshold = 1.5
# lower_threshold = 0.5
#
# action = "Alert"
# rule = "((2fd90a58-ae0f-4400-b561-9f0978fb7184-Temperature-Temperature<20) AND (2fd90a58-ae0f-4400-b561-9f0978fb7184-Temperature-Temperature<40))"
#
# def monitor_without_rule(list_current_items):
#     print ("Monitoring...")
#     # print ("list items: ", list_current_items)
#     while (1):
#         for item in list_current_items:
#             index = list_current_items.index(item)
#             # print ("index: ", index)
#             item_global_id = item['item_global_id']
#             item_state = item['item_state']
#
#
#             # Just monitor for number
#             try:
#                 item_state = float(item_state)
#             except:
#                 continue
#
#             print ("item state: ", item)
#
#             # get past state
#             list_past_item_state = get_item_state_from_item_global_id(item_global_id)
#             if (list_past_item_state == []):
#                 continue
#             print ("list_past_item_state: ", list_past_item_state)
#
#             avg_past_item_state = sum(list_past_item_state) * 1.0 / len(list_past_item_state)
#             print ("avg item state: ", avg_past_item_state)
#             if (item_state < upper_threshold * avg_past_item_state or item_state > lower_threshold * avg_past_item_state):
#                 send_alert_without_rule(item_global_id, item_state, list_past_item_state)
#             else:
#                 print ("item id: " + str(item_global_id) + " NORMAL!")
#
#
# def get_item_state_from_item_global_id(list_item, item_global_id):
#
#     list_item_state = []
#     for item in list_item:
#         if (item['item_global_id'] == item_global_id):
#             list_item_state.append(item['item_state']['item_state'])
#     return list_item_state
#
#
# def request_past_things_info(list_item_global_id, n_record):
#
#     message = {
#         'n_record' : n_record,
#         'reply_to' : 'dbreader.respond.monitor',
#         'list_item_global_id': list_item_global_id
#     }
#
#     producer_connection.ensure_connection()
#     with Producer(producer_connection) as producer:
#         producer.publish(
#             json.dumps(message),
#             exchange=exchange.name,
#             routing_key='dbreader.request.api_get_item_state',
#             retry=True
#         )
#     print ("Send request to DBreader")
#
#
# # def extract_things_info(list_things):
# #     platform_id = list_things['platform_id']
# #     list_items = []
# #     list_item_global_id = []
# #     # Extract message's information
# #     for thing in list_things['things']:
# #         for item in thing['items']:
# #             record = {
# #                 'item_global_id': item['item_global_id'],
# #                 'item_state' : item['item_state']
# #             }
# #             list_item_global_id.append(item['item_global_id'])
# #             list_items.append(record)
# #
# #     return platform_id, list_items, list_item_global_id
#
#
# def send_alert_without_rule(item_global_id, item_state, past_state):
#     message = {
#         'item_global_id' : item_global_id,
#         'item_state'     : item_state,
#         'past_state'     : past_state
#     }
#
#     request_queue = Queue(name='monitor.request.alert', exchange=exchange, routing_key='monitor.request.alert')
#     request_routing_key = 'monitor.request.alert'
#     producer_connection.ensure_connection()
#
#     with Producer(producer_connection) as producer:
#         producer.publish(
#             json.dumps(message),
#             exchange=exchange.name,
#             routing_key=request_routing_key,
#             declare=[request_queue],
#             retry=True
#         )
#
#     print ("Send alert!")
#
#
# def send_alert_with_rule():
#     message = {
#         "content" : "Alert"
#     }
#
#     request_queue = Queue(name='monitor.request.alert', exchange=exchange, routing_key='monitor.request.alert')
#     request_routing_key = 'monitor.request.alert'
#     producer_connection.ensure_connection()
#
#     with Producer(producer_connection) as producer:
#         producer.publish(
#             json.dumps(message),
#             exchange=exchange.name,
#             routing_key=request_routing_key,
#             declare=[request_queue],
#             retry=True
#         )
#
#     print ("Send alert!")
#
#
# # def handle_notification(body, message):
# #     # receive list items
# #     global list_current_items
# #
# #     print('Receive message from Collector')
# #     list_things = json.loads(body)
# #     platform_id, list_current_items, list_item_global_id = extract_things_info(list_things)
# #
# #     # past items state
# #     request_past_things_info(list_item_global_id, n_record)
#
#
# def find_condition(string):
#     condition = None
#     item_global_id = ""
#     value = 0
#
#     if (string == "True"):
#         return True
#
#     if (string == "False"):
#         return False
#
#     for i in range(len(string)):
#         if (string[i] == "="):
#             condition = "="
#             item_global_id  = string[0:i]
#             value = string[i+1::]
#         elif (string[i] == "<"):
#             if (string[i+1] == "="):
#                 condition = "<="
#                 item_global_id = string[0:i]
#                 value = string[i+2::]
#             else:
#                 condition = "<"
#                 item_global_id = string[0:i]
#                 value = string[i+1::]
#         elif (string[i] == ">"):
#             if (string[i+1] == "="):
#                 condition = ">="
#                 item_global_id = string[0:i]
#                 value = string[i+2::]
#             else:
#                 condition = ">"
#                 item_global_id = string[0:i]
#                 value = string[i+1::]
#         # else:
#         #     print ("Error: Condition not found!")
#
#     return condition, item_global_id, value
#
#
# def check_condition(condition, list_item_global_id, value):
#     request_past_things_info(list_item_global_id, n_record)
#
#     list_item = []
#     def handle_dbreader_notification(body, message):
#         # print (message)
#         nonlocal list_item
#         # print (list_item)
#         print ("Receive message from DBReader!")
#         list_item = json.loads(body)['items']
#         print ("list past items: ", list_item)
#
#
#     queue_get_past_states = Queue(name='dbreader.respond.monitor', exchange=exchange,
#                                   routing_key='dbreader.respond.monitor')
#
#     try:
#         consumer_connection.ensure_connection(max_retries=1)
#         with nested(Consumer(consumer_connection, queues=queue_get_past_states,
#                              callbacks=[handle_dbreader_notification], no_ack=True)):
#
#             consumer_connection.drain_events()
#     except (ConnectionRefusedError, exceptions.OperationalError):
#         print('Connection lost')
#     except consumer_connection.connection_errors:
#         print('Connection error')
#
#     item_state = get_item_state_from_item_global_id(list_item, list_item_global_id[0])
#     if (len(item_state) > 0):
#         item_state = sum(item_state) / len(item_state)
#     else:
#         print ("Item state len = 0 !")
#         return False
#
#
#     if (condition == "="):
#         if (item_state == float(value)):
#             return True
#         else:
#             return False
#     elif (condition == "<"):
#         if (item_state < float(value)):
#             return True
#         else:
#             return False
#     elif (condition == "<="):
#         if (item_state <= float(value)):
#             return True
#         else:
#             return False
#     elif (condition == ">"):
#         if (item_state > float(value)):
#             return True
#         else:
#             return False
#     elif (condition == ">="):
#         if (item_state >= float(value)):
#             return True
#         else:
#             return False
#     else:
#         return False
#
#
# def handle_rule(body, message):
#     global rule, action
#
#     rule = json.loads(body)["rule"]
#     action = json.loads(body)["action"]
#
#
#
# def run():
#
#     queue_get_rules = Queue(name='monitor.request.rule_engine', exchange=exchange,
#                                   routing_key='monitor.request.rule_engine')
#
#     while 1:
#         try:
#             consumer_connection.ensure_connection(max_retries=1)
#             with nested(Consumer(consumer_connection, queues=queue_get_rules,
#                                  callbacks=[handle_rule], no_ack=True)):
#                 while True:
#                     consumer_connection.drain_events()
#         except (ConnectionRefusedError, exceptions.OperationalError):
#             print('Connection lost')
#         except consumer_connection.connection_errors:
#             print('Connection error')
#
#
#
#
# # def monitor_with_rule():
# #     global action, rule
# #
# #     print ("Monitoring...")
# #
# #     while (1):
# #         start_condition = -1
# #         end_condition   = -1
# #         item_global_id_1 = ""
# #         item_global_id_2 = ""
# #
# #         # print ("RULE: ", rule)
# #         i=0
# #         global rule
# #         temp_rule = rule
# #
# #         while (i<len(temp_rule)):
# #         # for i in range(len(rule)):
# #             # len_old_rule = len(rule)
# #             print (temp_rule[i])
# #             if (temp_rule[i] == ")"):     # Tim dau ")" dau tien
# #                 end_condition = i
# #                 for j in range(end_condition, -1, -1):   # Duyet nguoc lai cho den khi gap dau "(" dau tien
# #                     if (temp_rule[j] == "("):
# #                         start_condition = j
# #                         break;
# #
# #                 sub_rule = temp_rule[start_condition+1:end_condition]
# #                 # print (sub_rule)
# #
# #                 AND_pos = sub_rule.find("AND")
# #                 OR_pos  = sub_rule.find("OR")
# #                 print ("AND: ", AND_pos)
# #                 print ("OR: ",  OR_pos)
# #
# #                 if (AND_pos != -1):
# #                     exp_start_1 = 0
# #                     exp_end_1   = AND_pos - 1
# #                     exp_start_2 = AND_pos + 4
# #                     exp_end_2   = len(sub_rule)
# #                     print ("sub rule 1: ", sub_rule[exp_start_1:exp_end_1])
# #                     print ("sub rule 2: ", sub_rule[exp_start_2:exp_end_2])
# #
# #                     if (sub_rule[exp_start_1:exp_end_1] != "False" and sub_rule[exp_start_1:exp_end_1] != "True"):
# #                         condition_1, item_global_id_1, value_1 = find_condition(sub_rule[exp_start_1:exp_end_1])
# #                         list_item_global_id_1 = []
# #                         list_item_global_id_1.append(item_global_id_1)
# #                         print ("Item global id 1:", item_global_id_1)
# #                         check_cond_1 = check_condition(condition_1, list_item_global_id_1, value_1)
# #                     else:
# #                         check_cond_1 = bool(sub_rule[exp_start_1:exp_end_1])
# #
# #                     if (sub_rule[exp_start_2:exp_end_2] != "False" and sub_rule[exp_start_2:exp_end_2] != "True"):
# #                         condition_2, item_global_id_2, value_2 = find_condition(sub_rule[exp_start_2:exp_end_2])
# #                         list_item_global_id_2 = []
# #                         list_item_global_id_2.append(item_global_id_2)
# #                         print ("Item global id 2:", item_global_id_2)
# #                         check_cond_2 = check_condition(condition_2, list_item_global_id_2, value_2)
# #                     else:
# #                         check_cond_2 = bool(sub_rule[exp_start_2:exp_end_2])
# #
# #                     check_cond = check_cond_1 and check_cond_2
# #
# #                     if (check_cond == True):
# #                         temp_rule = rule[0:start_condition] + "True" + rule[end_condition+1::]
# #                     elif (check_cond == False):
# #                         temp_rule = rule[0:start_condition] + "False" + rule[end_condition+1::]
# #                     else:
# #                         print ("error in AND: condition must be True or False")
# #                         return -1
# #
# #                 elif (OR_pos != -1):
# #                     exp_start_1 = 0
# #                     exp_end_1   = OR_pos - 1
# #                     exp_start_2 = OR_pos + 3
# #                     exp_end_2   = len(sub_rule) - 1
# #
# #                     print ("sub rule 1: ", sub_rule[exp_start_2:exp_end_2])
# #                     print ("sub rule 2: ", sub_rule[exp_start_2:exp_end_2])
# #
# #                     if (sub_rule[exp_start_1:exp_end_1] != "False" and sub_rule[exp_start_1:exp_end_1] != "True"):
# #                         condition_1, item_global_id_1, value_1 = find_condition(sub_rule[exp_start_1:exp_end_1])
# #                         list_item_global_id_1 = []
# #                         list_item_global_id_1.append(item_global_id_1)
# #                         print ("Item global id 1:", item_global_id_1)
# #                         check_cond_1 = check_condition(condition_1, list_item_global_id_1, value_1)
# #                     else:
# #                         check_cond_1 = bool(sub_rule[exp_start_1:exp_end_1])
# #
# #                     if (sub_rule[exp_start_2:exp_end_2] != "False" and sub_rule[exp_start_2:exp_end_2] != "True"):
# #                         condition_2, item_global_id_2, value_2 = find_condition(sub_rule[exp_start_2:exp_end_2])
# #                         list_item_global_id_2 = []
# #                         list_item_global_id_2.append(item_global_id_2)
# #                         print ("Item global id 2:", item_global_id_2)
# #                         check_cond_2 = check_condition(condition_2, list_item_global_id_2, value_2)
# #                     else:
# #                         check_cond_2 = bool(sub_rule[exp_start_2:exp_end_2])
# #
# #                     check_cond = check_cond_1 or check_cond_2
# #
# #                     if (check_cond == True):
# #                         temp_rule = rule[0:start_condition] + "True" + rule[end_condition+1::]
# #                     elif (check_cond == False):
# #                         temp_rule = rule[0:start_condition] + "False" + rule[end_condition+1::]
# #                     else:
# #                         print ("error in OR: condition must be True or False")
# #                         return -1
# #
# #                 else:
# #                     print ("sub rule: ", sub_rule)
# #
# #                     if (sub_rule != "False" and sub_rule != "True"):
# #                         condition, item_global_id, value = find_condition(sub_rule)
# #                         list_item_global_id = []
# #                         list_item_global_id.append(item_global_id)
# #                         print ("Item global id:", item_global_id)
# #                         check_cond = check_condition(condition, list_item_global_id, value)
# #                     else:
# #                         check_cond = bool(sub_rule)
# #
# #
# #                     if (check_cond == True):
# #                         temp_rule = rule[0:start_condition] + "True" + rule[end_condition+1::]
# #                     elif (check_cond == False):
# #                         temp_rule = rule[0:start_condition] + "False" + rule[end_condition+1::]
# #                     else:
# #                         print ("error check condition must be true or false")
# #                         return -1
# #
# #                 i = i - (len(rule) - len(temp_rule))
# #             else:
# #                 i = i + 1
# #
# #                 # i = i + len_old_rule - len(rule)
# #
# #         if (start_condition == -1 or end_condition == -1):
# #             print ("Syntax error!")
# #             return False
# #
# #         if (rule == "True"):
# #             #Thuc hien hanh dong action
# #             if (action == "Alert"):
# #                 send_alert_with_rule()
# #             else:
# #                 print ("Error: Action is not defined!")
# #         elif (rule == "False"):
# #             pass
# #         else:
# #             print (rule)
#
#
#
#
# # try:
# #     # _thread.start_new_thread( run, () )
# #     _thread.start_new_thread( monitor_with_rule, () )
# # except:
# #     print ("Error: unable to start thread")
# #
# # while (1):
# #     pass