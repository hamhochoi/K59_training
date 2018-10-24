# import Api
#
# thing_global_id = '7d6e5d0a-d31a-45a9-91dc-cd7d51f89f70/binary_sensor.motion_detection'
# item_global_id = '7d6e5d0a-d31a-45a9-91dc-cd7d51f89f70/binary_sensor.motion_detection/binary_sensor.motion_detection'
# platform_id = '7d6e5d0a-d31a-45a9-91dc-cd7d51f89f70'
# print(Api.api_get_thing_state_by_id(thing_global_id))
# print(Api.api_get_thing_state_by_id(thing_global_id))
# print(Api.api_get_things_state())
# print(Api.api_get_item_state_by_id(thing_global_id, item_global_id))
# print(Api.api_get_things_state_in_platform(platform_id))
# print(Api.api_get_thing_info_in_platform(platform_id))
# print(Api.api_get_things_info())
#


# import paho.mqtt.client as mqtt
# import json
# broker_address = "iot.eclipse.org"
# clientMQTT = mqtt.Client("test")  # create new instance
# clientMQTT.connect(broker_address)  # connect to broker
# global_id = 'f2b99574-8585-4cac-935f-d53ada871086/binary_sensor.motion_detection'
# message = {
#     'caller': 'collector',
#     'thing_global_id': global_id
# }
#
# clientMQTT.publish('dbwriter/request/api_get_thing_by_global_id', json.dumps(message))
# clientMQTT.publish('dbwriter/request/api_get_thing_by_global_id', json.dumps(message))
# clientMQTT.publish('dbwriter/request/api_get_thing_by_global_id', json.dumps(message))
# from influxdb import InfluxDBClient
# clientDB = InfluxDBClient('localhost', 8086, 'root', 'root', 'Collector_DB')
# clientDB.create_database('Collector_DB')
# thing_global_id = '684fed03-b982-4059-a366-005d111d8ed8/Switch1'
# temp = "SELECT *, item_global_id FROM collector WHERE thing_global_id =\'" + thing_global_id + "\' GROUP BY item_global_id ORDER BY time DESC LIMIT 2"
# query_result = clientDB.query(temp)
# print(query_result)
#
# for item in query_result:
#     print(item)

import Api

host_homeAssistant = "192.168.60.199"
port_homeAssistant = "8123"
import requests
def hihi():
    while True:
        try:
            url = 'http://' + host_homeAssistant + ':' + port_homeAssistant + '/api/states'
            print(requests.get(url).status_code)
            response = requests.get(url).json()
            print(response)
            return response
        except:
            print("Loi")
            continue

hihi()