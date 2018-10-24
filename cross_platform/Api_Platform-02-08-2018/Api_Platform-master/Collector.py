import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import ast
import json
import threading

# clientDB = InfluxDBClient('localhost', 8086, 'root', 'root', 'Collector_DB')
# clientDB.create_database('Collector_DB')

broker_cloud = "iot.eclipse.org"
broker_fog = "broker.hivemq.com"
client_mqtt_cloud_1 = mqtt.Client()  # client for asynchronous
client_mqtt_cloud_1.connect(broker_cloud)  # connect to broker



client_mqtt_fog_1 = mqtt.Client()
client_mqtt_fog_1.connect(broker_fog)

time_collect = 5
list_platforms = []


def collect():
    print("Collect the states of the devices")
    for platform_id in list_platforms:
        collect_by_platform_id(platform_id)
    threading.Timer(time_collect, collect).start()


def collect_by_platform_id(platform_id):
    print('Collect data from platform_id: ', str(platform_id))
    message = {
        'caller': 'collector'
    }

    def handle_collect_by_platform_id(client, userdata, msg):
        print('Recived state from platform_id: ', platform_id)
        # print(msg.payload.decode('utf-8'))
        # print(ast.literal_eval(msg.payload.decode('utf-8')))
        list_things = json.loads(msg.payload.decode('utf-8'))
        print(list_things)
        client_mqtt_cloud_1.publish('dbwriter/request/api_write_db', json.dumps(list_things))
        print('Send new state to Dbwriter')

    client_mqtt_cloud_1.subscribe('{}/response/collector/api_get_states'.format(platform_id))
    client_mqtt_cloud_1.message_callback_add('{}/response/collector/api_get_states'.format(platform_id), handle_collect_by_platform_id)
    client_mqtt_fog_1.publish('{}/request/api_get_states'.format(platform_id), json.dumps(message))


def get_thing_by_id(thing_global_id):
    print('Get thing by thing_global_id')
    client_mqtt_cloud_2 = mqtt.Client()  # client for synchronous
    client_mqtt_cloud_2.connect(broker_cloud)
    check_response = 0
    thing = {}
    message = {
        'caller': 'collector',
        'thing_global_id': thing_global_id
    }

    def handle_api_get_thing_by_global_id(client, userdata, msg):
        nonlocal check_response, thing
        thing = json.loads(msg.payload.decode('utf-8'))
        # print('Thing nhan duoc: {}'.format(thing))
        check_response = 1
        client_mqtt_cloud_2.message_callback_remove('dbwriter/response/collector/api_get_thing_by_global_id')
        client_mqtt_cloud_2.unsubscribe('dbwriter/response/collector/api_get_thing_by_global_id')

    client_mqtt_cloud_2.subscribe('dbwriter/response/collector/api_get_thing_by_global_id')
    client_mqtt_cloud_2.message_callback_add('dbwriter/response/collector/api_get_thing_by_global_id', handle_api_get_thing_by_global_id)
    client_mqtt_cloud_2.publish('dbwriter/request/api_get_thing_by_global_id', json.dumps(message))
    while check_response == 0:
        client_mqtt_cloud_2.loop()
        continue
    client_mqtt_cloud_2.disconnect()
    return thing


def get_things(list_thing_global_id):
    print('Get all thing state in list thing')
    client_mqtt_cloud_2 = mqtt.Client()  # client for synchronous
    client_mqtt_cloud_2.connect(broker_cloud)
    check_response = 0
    list_thing = []
    message = {
        'caller': 'collector',
        'list_thing_global_id': list_thing_global_id
    }

    def handle_api_get_things(client, userdata, msg):
        nonlocal check_response, list_thing
        list_thing = ast.literal_eval(msg.payload.decode('utf-8'))
        check_response = 1
        client_mqtt_cloud_2.message_callback_remove('dbwriter/response/collector/api_get_things')
        client_mqtt_cloud_2.unsubscribe('dbwriter/response/collector/api_get_things')

    client_mqtt_cloud_2.subscribe('dbwriter/response/collector/api_get_things')
    client_mqtt_cloud_2.message_callback_add('dbwriter/response/collector/api_get_things', handle_api_get_things)
    client_mqtt_cloud_2.publish('dbwriter/request/api_get_things', json.dumps(message))
    while check_response == 0:
        client_mqtt_cloud_2.loop()
        continue
    client_mqtt_cloud_2.disconnect()
    return list_thing


def get_list_platforms():
    print("Get list platforms from Registry")
    message = {
        'caller': 'collector'
    }

    def handle_get_list(client, userdata, msg):
        global list_platforms
        list_platforms = ast.literal_eval(msg.payload.decode('utf-8'))
        print('Updated list of platform_id: ', str(list_platforms))

    client_mqtt_cloud_1.publish('registry/request/api_get_list_platforms', json.dumps(message))
    client_mqtt_cloud_1.subscribe('registry/response/collector/api_get_list_platforms')
    client_mqtt_cloud_1.message_callback_add('registry/response/collector/api_get_list_platforms', handle_get_list)


def handle_notification(client, userdata, msg):
    print('Have Notification')
    if json.loads(msg.payload.decode('utf-8'))['notification'] == 'Have Platform_id change':
        get_list_platforms()


def api_get_things(client, userdata, msg):
    print('API get things')
    caller = json.loads(msg.payload.decode('utf-8'))['caller']
    list_thing_global_id = json.loads(msg.payload.decode('utf-8'))['list_thing_global_id']
    client_mqtt_cloud_1.publish('collector/response/{}/api_get_things'.format(caller), str(get_things(list_thing_global_id)))


def api_get_thing_by_id(client,userdata, msg):
    print('Get thing state by id')
    caller = json.loads(msg.payload.decode('utf-8'))['caller']
    thing_global_id = json.loads(msg.payload.decode('utf-8'))['thing_global_id']
    client_mqtt_cloud_1.publish('collector/response/{}/api_get_thing_by_id'.format(caller), json.dumps(get_thing_by_id(thing_global_id)))

client_mqtt_cloud_1.subscribe('collector/request/notification')
client_mqtt_cloud_1.message_callback_add('collector/request/notification', handle_notification)

client_mqtt_cloud_1.subscribe('collector/request/api_get_things')
client_mqtt_cloud_1.message_callback_add('collector/request/api_get_things', api_get_things)

client_mqtt_cloud_1.subscribe('collector/request/api_get_thing_by_id')
client_mqtt_cloud_1.message_callback_add('collector/request/api_get_thing_by_id', api_get_thing_by_id)

# def on_disconnect(client, userdata, rc):
#     if rc != 0:
#         print ("Disconnect but auto-reconnect")
#         client_mqtt_cloud_2.reconnect()
#
# client_mqtt_cloud_2.on_disconnect = on_disconnect
get_list_platforms()
collect()
client_mqtt_cloud_1.loop_forever()