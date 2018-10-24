# import os
# import json

# message = {
#         #this rule is to turn off a light if there is no movement
#         "rule_id": "1351c35dfdsf",
#         "name": "Motion light off",
#         # bitwise like (    (temperature<10)     and     ((humidity<50) or (humidity>90))     )
#         "bitwise": [
#             {
#                 "things" : [
#                     {
#                         # there is one timer by condition/action
#                         # for now it is the number of seconds the condition has to be met (here it's no movements for 60 seconds)
#                         "timer": 60,
#                         # we take a thing as defined in the API
#                         "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
#                         "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-binary_sensor.motion_detection-binary_sensor.motion_detection",
#                         "item_name": "Motion Detection",
#                         "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
#                         # the operator is stored as a function name
#                         "operator": "EQ('off')"
#                     }
#                 ],
                
#                 "bitwise_operator" : "AND", 

#                 "bitwise" : [
#                     {
#                         "things" : [
#                             {
#                                 # there is one timer by condition/action
#                                 # for now it is the number of seconds the condition has to be met (here it's no movements for 60 seconds)
#                                 "timer": 60,
#                                 # we take a thing as defined in the API
#                                 "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
#                                 "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-binary_sensor.motion_detection-binary_sensor.motion_detection",
#                                 "item_name": "Motion Detection",
#                                 "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
#                                 # the operator is stored as a function name
#                                 "operator": "EQ('off')"
#                             }
#                         ],
#                         # if bitwise operator == None then bitwise == NULL
#                         "bitwise_operator" : "None", 
#                         "bitwise" : []

#                     }, 

#                 ]
                
#             }
#         ],
#         "action": [
#             {
#                 #here the timer define the difference between the moment the conditions are met and the moment the action take place
#                 "timer": 0,
#                 "action": "light_off",
#                 "things": [
#                     {
#                         "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
#                         "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light-sensor.light",
#                         "new_state" : "off"
#                     }, 
#                     {
#                         "thing_global_id": "35665-2f39-47f8-a229-18cf4376a3c9-sensor.temperature",
#                         "item_global_id": "35665-2f39-47f8-a229-18cf4376a3c9-sensor.temperature-sensor.temperature",
#                         "new_state" : "70"
#                     }
#                 ],
#             }, 
#             {
#                 "timer": 0,
#                 "action": "light_off",
#                 "things": [
#                     {
#                         "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
#                         "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light-sensor.light",
#                         "new_state" : "off"
#                     }, 
#                     {
#                         "thing_global_id": "35665-2f39-47f8-a229-18cf4376a3c9-sensor.light",
#                         "item_global_id": "35665-2f39-47f8-a229-18cf4376a3c9-sensor.light-sensor.light",
#                         "new_state" : "off"
#                     }
#                 ],
#             }
#         ]
#     }

# # print (message)
# print("curl -H  \"Content-type: application/json\" -X POST http://127.0.0.1:5000/rule -d " + "\'" + str(message) + "\'")

"""

from influxdb import InfluxDBClient
import json
from kombu import Connection, Consumer, Exchange, Queue, exceptions

clientDB = InfluxDBClient('localhost', 8086, 'root', 'root', 'Collector_DB')
clientDB.create_database('Rule')
clientDB.switch_database('Rule')
rule = {
        'rule_id': '1351c35dfdsf',
        'rule_name': 'Motion_light_off',
        'bitwise': [
            {
                # "timer": 60,
                # "things": [
                #     {
                #         "items": [
                #             {
                #                 "can_set_state": "no",
                #                 "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-binary_sensor.motion_detection-binary_sensor.motion_detection",
                #                 "item_local_id": "binary_sensor.motion_detection",
                #                 "item_name": "Motion Detection",
                #                 "item_status": "active",
                #                 "item_type": "binary_sensor"
                #           }
                #         ],
                #         "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
                #         "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-binary_sensor.motion_detection",
                #         "thing_local_id": "binary_sensor.motion_detection",
                #         "thing_name": "Motion Detection",
                #         "thing_status": "active",
                #         "thing_type": "binary_sensor"
                #     }
                # ],
                # "operator": "EQ('off')",

                # "bitwise_operator": "AND",

                # "bitwise": [
                #     {
                #         "timer": 60,
                #         "things": [
                #             {
                #                 "items": [
                #                     {
                #                         "can_set_state": "no",
                #                         "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light-sensor.light",
                #                         "item_local_id": "sensor.light",
                #                         "item_name": "Light",
                #                         "item_state": 1,
                #                         "item_status": "active",
                #                         "item_type": "sensor",
                #                         "last_changed": "2018-05-23T14:02:40Z"
                #                     }
                #                 ],
                #                 "location": "",
                #                 "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
                #                 "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
                #                 "thing_local_id": "sensor.light",
                #                 "thing_name": "Light",
                #                 "thing_status": "active",
                #                 "thing_type": "sensor"
                #             }
                #         ],
                #         "operator": "LT(1)",

                #         "bitwise_operator": "None",
                #         "bitwise": []
                #     }

                # ]

            }
        ],
        'action': [
            # {
            #     "timer": 0,
            #     "action": "light_off",
            #     "things": [
            #         {
            #             "items": [
            #                 {
            #                     "can_set_state": "no",
            #                     "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light-sensor.light",
            #                     "item_local_id": "sensor.light",
            #                     "item_name": "Light",
            #                     "item_status": "active",
            #                     "item_type": "sensor",
            #                     "last_changed": "2018-05-23T14:02:40Z"
            #                 }
            #             ],
            #             "location": "",
            #             "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
            #             "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
            #             "thing_local_id": "sensor.light",
            #             "thing_name": "Light",
            #             "thing_status": "active",
            #             "thing_type": "sensor"
            #         }
            #     ]
            # }
        ]
    }

rule = json.dumps(rule)
data = json.loads(rule)

# print (data["rule_name"])
# print (data["rule_id"])
# print (data)

record = {
            'measurement': data["rule_name"],
            'tags': {
                'rule_id': data["rule_id"]
            },
            'fields': {
                'data': str(data),
            }
        }


# print (record["measurement"])

data_to_db = []
data_to_db.append(record)

clientDB.write_points(data_to_db)
measurement = record["measurement"]
query_statement = 'SELECT * FROM ' + measurement
print (query_statement)
query_result = clientDB.query(query_statement) 

print (query_result)



"""
import os
import json

# rule = {
#         "rule_id": "21351c35dfdsf",
#         "rule_name": "Motion light off",
#         "rule_status" : "active", 
#         "rule_condition" : {
#             "bitwise": {
#                     "things" : [
#                         {
#                             "timer": "60",
#                             "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9.light",
#                             "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-binary_sensor.motion_detection-binary_sensor.motion_detection",
#                             "item_name": "Motion Detection",
#                             "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
#                             "operator": "EQ(\"off\")"
#                         }
#                     ],
                    
#                     "bitwise_operator" : "AND", 

#                     "bitwise" : [
#                         {
#                             "things" : [
#                                 {
#                                     "timer": "60",
#                                     "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
#                                     "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-binary_sensor.motion_detection-binary_sensor.motion_detection",
#                                     "item_name": "Motion Detection",
#                                     "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
#                                     "operator": "EQ(\"off\")"
#                                 }
#                             ],
#                             "bitwise_operator" : "None", 
#                             "bitwise" : "None"
#                         } 
#                     ]
                    
                    
#             },
#             "action": [
#                 {
#                     "timer": 0,
#                     "action": "light_off",
#                     "things": [
#                         {
#                             "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
#                             "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light-sensor.light",
#                             "new_state" : "off"
#                         }, 
#                         {
#                             "thing_global_id": "35665-2f39-47f8-a229-18cf4376a3c9-sensor.temperature",
#                             "item_global_id": "35665-2f39-47f8-a229-18cf4376a3c9-sensor.temperature-sensor.temperature",
#                             "new_state" : "70"
#                         }
#                     ]
#                 }, 
#                 {
#                     "timer": 0,
#                     "action": "light_off",
#                     "things": [
#                         {
#                             "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
#                             "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light-sensor.light",
#                             "new_state" : "off"
#                         }, 
#                         {
#                             "thing_global_id": "35665-2f39-47f8-a229-18cf4376a3c9-sensor.light",
#                             "item_global_id": "35665-2f39-47f8-a229-18cf4376a3c9-sensor.light-sensor.light",
#                             "new_state" : "off"
#                         }
#                     ]
#                 }
#             ]
#         }
#     }

# print (json.dumps(rule))



import requests
from flask import jsonify

# r = requests.get('http://127.0.0.1:5000/rule')
# r = r.json()
# rule_condition = r[0]['rule_condition']['bitwise']['bitwise']
# print (rule_condition)
# rule_condition = "\'" + rule_condition + "\'"
# rule_condition = json.dumps(rule_condition)
# rule_condition = json.loads(rule_condition)
# print (type(rule_condition))
# print (rule_condition['action'])


message = {
        "thing_global_id" : "1",
        "item_global_id"  : "2",
        "new_state"       : "3"
    }

print (json.dumps(message))

os.system("curl -H \"Content-type: application/json\" -X POST http://127.0.0.1:5000/api_set_state -d " + "\'" + json.dumps(message) + "\'")


# r = requests.post('http://127.0.0.1:5000/api_set_state', data="\'" + json.dumps(message) + "\'")
# print (r)
