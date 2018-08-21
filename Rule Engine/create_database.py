'''
    install MySQLdb python3: 
        sudo apt install python3-dev libpython3-de
        sudo apt install python3-mysqldb
'''

import MySQLdb
import json
import random
import datetime

db = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root")

# Create a Cursor object to execute queries.
cursor = db.cursor()

cursor.execute("""CREATE DATABASE IF NOT EXISTS Trigger_DB""")

cursor.execute("""USE Trigger_DB""")



cursor.execute("""CREATE TABLE IF NOT EXISTS ItemTable(
    item_id VARCHAR(50),
    item_name VARCHAR(50),
    item_type VARCHAR(50),
    item_state VARCHAR(50), 
    time VARCHAR(50),
    PRIMARY KEY (item_id, time))""")

# cursor.execute("""CREATE TABLE IF NOT EXISTS TriggerTable(
#     trigger_id VARCHAR(100) PRIMARY KEY,
#     trigger_type VARCHAR(100),
#     trigger_content VARCHAR(20000))""")
#
# # #create exam table
# cursor.execute("""CREATE TABLE IF NOT EXISTS ActionTable(
#     action_id VARCHAR(100) PRIMARY KEY,
#     action_type VARCHAR(100),
#     action_content VARCHAR(20000))""")
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS ConditionTable(
#     condition_id VARCHAR(100) PRIMARY KEY,
#     condition_type VARCHAR(100),
#     condition_content VARCHAR(20000))""")
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS RuleTable(
#     rule_id VARCHAR(100) PRIMARY KEY,
#     rule_name VARCHAR(100),
#     rule_status VARCHAR(100),
#     trigger_id VARCHAR(100),
#     condition_id VARCHAR(100),
#     action_id VARCHAR(50),
#     trigger_content VARCHAR(20000),
#     condition_content VARCHAR(20000),
#     action_content VARCHAR(20000),
#     insert_time VARCHAR(100),
#     FOREIGN KEY(trigger_id) REFERENCES TriggerTable(trigger_id),
#     FOREIGN KEY(condition_id) REFERENCES ConditionTable(condition_id),
#     FOREIGN KEY(action_id) REFERENCES ActionTable(action_id))""")






cursor.execute("""INSERT INTO ItemTable(
    item_id, item_name, item_type, item_state, time)
    VALUES ('10239bf5-f0c9-4200-8fe2-522bb3abc4da', 'LedXanh', 'Gauge', 'on', '2018-08-07 23:38:19.571805')""")

# cursor.execute("""INSERT INTO ItemTable(
#     item_id, item_name, item_type, item_state, time)
#     VALUES ('04fa6c2b-6fc3-4c61-ae53-4a9cc2188090', 'light', 'int', '1', '2018-08-07 23:38:20.571805')""")
#
# cursor.execute("""INSERT INTO ItemTable(
#     item_id, item_name, item_type, item_state, time)
#     VALUES ('940347de-8cd8-417f-b0b3-0d63d1d47278', 'temperature', 'int', '50', '2018-08-07 23:38:21.571805')""")
#
# cursor.execute("""INSERT INTO ItemTable(
#     item_id, item_name, item_type, item_state, time)
#     VALUES ('0f3ecd50-c870-464c-a4cf-76b5e8b34874', 'Humidity', 'int', '40', '2018-08-07 23:38:21.571805')""")
#
# cursor.execute("""INSERT INTO ItemTable(
#     item_id, item_name, item_type, item_state, time)
#     VALUES ('31394bf1-dd21-4809-adb1-bd885459852e', 'Motion', 'Gauge', '0', '2018-08-07 23:38:21.571805')""")





trigger_1 = {
    "trigger_id" : "trigger_id_1",
    "trigger_type" : "item_has_given_state",
    "description" : "example of trigger",
    "config" : [
        {
            "constraint" : {
                "time": "60s",
                "item" : {
                    "thing_global_id": "10ac216a-6f51-43bb-86fa-8d7a5a8947ff",
                    "item_global_id": "04fa6c2b-6fc3-4c61-ae53-4a9cc2188090",
                    "item_name": "light",
                    "item_type" : "int",
                    "platform_id": "a3f6e492-5e20-47a4-ace9-5011316974ad"
                },
                "comparation": "LE",
                "value" : "3"
            },
            "bitwise_operator" : "None",
        },
        {
            "constraint" : {
                "time": "10s",
                "item" : {
                    "thing_global_id": "10ac216a-6f51-43bb-86fa-8d7a5a8947ff",
                    "item_global_id": "2cac0319-9aad-4117-a65e-c3a710d2288a",
                    "item_name": "humidity",
                    "item_type" : "int",
                    "platform_id": "a3f6e492-5e20-47a4-ace9-5011316974ad"
                },
                "comparation": "LE",
                "value" : "100"
            },
            "bitwise_operator" : "AND"
        }
    ],
    "outputs" : [
        {
            "event_name" : "event_1",
            "event_id" : "event_id_1",
            "event_source" : "trigger_id_1",
            "description" : "motion detected!"
        },
        {
            "event_name" : "event_2",
            "event_id" : "event_id_2",
            "event_source" : "trigger_id_1",
            "description" : "measure humidity"
        }
    ]
}

trigger_1 = json.dumps(trigger_1)
trigger_id = json.loads(trigger_1)['trigger_id']
trigger_type = json.loads(trigger_1)['trigger_type']


# cursor.execute("""INSERT INTO TriggerTable(trigger_id, trigger_type, trigger_content)
#     VALUES ('%s', '%s', '%s')""" % (trigger_id, trigger_type, trigger_1))



'''
action_1 = {
    "action_name" : "action_name_1",
    "action_id"   : "action_id_1",
    "action_type" : "send_a_command",
    "description" : "Sends a command to a specified item.",
    "config" : {
        "command" : "Motion.turn_on",
        "item" : "item_global_id_1"
    }
}

cursor.execute("""INSERT INTO ActionTable(action_id, action_type, action_content)
    VALUES ('action_id_1', 'send_a_command', '%s')""" % (json.dumps(action_1)))
'''



'''
condition_1 = {
    "condition_id" : "condition_id_1",
    "condition_name" : "condition_name_1",
    "condition_type" : "item_has_given_state",
    "description" : "Compares the item state with the given value",
    "config": {
        "time" : "10s",
        "operator":">",
        "value":"20",
        "item_id" : "item_global_id_1"
    }
}


cursor.execute("""INSERT INTO ConditionTable(condition_id, condition_type, condition_content)
                VALUES ('condition_id_1', 'item_has_given_state', '%s')""" %(json.dumps(condition_1)))
'''




# rule_1 = {
#     "rule_id": str(random.randint(0, 1000000000)),
#     "rule_name": "a toy rule",
#     "rule_status" : "enable",
#     "trigger" : {
#         "trigger_id" : "trigger_id_1",
#         "trigger_type" : "item_has_given_state",
#         "description" : "example of trigger",
#         "config" : [
#             {
#                 "constraint" : {
#                     "time": "60s",
#                     "item" : {
#                         "thing_global_id": "10ac216a-6f51-43bb-86fa-8d7a5a8947ff",
#                         "item_global_id": "04fa6c2b-6fc3-4c61-ae53-4a9cc2188090",
#                         "item_name": "light",
#                         "item_type" : "int",
#                         "platform_id": "a3f6e492-5e20-47a4-ace9-5011316974ad"
#                     },
#                     "comparation": "LE",
#                     "value" : "100"
#                 },
#                 "bitwise_operator" : "None",
#             },
#             {
#                 "constraint" : {
#                     "time": "10s",
#                     "item" : {
#                         "thing_global_id": "10ac216a-6f51-43bb-86fa-8d7a5a8947ff",
#                         "item_global_id": "2cac0319-9aad-4117-a65e-c3a710d2288a",
#                         "item_name": "humidity",
#                         "item_type" : "int",
#                         "platform_id": "a3f6e492-5e20-47a4-ace9-5011316974ad"
#                     },
#                     "comparation": "LE",
#                     "value" : "100"
#                 },
#                 "bitwise_operator" : "AND"
#             }
#         ],
#         "outputs" : [
#             {
#                 "event_name" : "event_1",
#                 "event_id" : "event_id_1",
#                 "event_source" : "trigger_id_1",
#                 "description" : "motion detected!"
#             },
#             {
#                 "event_name" : "event_2",
#                 "event_id" : "event_id_2",
#                 "event_source" : "trigger_id_1",
#                 "description" : "measure humidity"
#             }
#         ]
#     },
#     "trigger_id" : "trigger_id_1",
#     "condition" : {
#         "condition_id" : "condition_id_1",
#         "condition_type" : "item_has_given_state",
#         "description" : "Sample Condition description",
#         "config" : [
#             {
#                 "constraint" : {
#                     "time": "60s",
#                     "item" : {
#                         "thing_global_id": "10ac216a-6f51-43bb-86fa-8d7a5a8947ff",
#                         "item_global_id": "940347de-8cd8-417f-b0b3-0d63d1d47278",
#                         "item_name": "temperature",
#                         "item_type" : "int",
#                         "platform_id": "a3f6e492-5e20-47a4-ace9-5011316974ad"
#                     },
#                     "comparation": "LE",
#                     "value" : "100"
#                 },
#                 "bitwise_operator" : "None"
#             },
#             {
#                 "constraint" : {
#                     "time": "10s",
#                     "item" : {
#                         "thing_global_id": "4152ecef-1458-4427-af61-431f525b6cb8",
#                         "item_global_id": "0f3ecd50-c870-464c-a4cf-76b5e8b34874",
#                         "item_name": "Humidity",
#                         "item_type" : "int",
#                         "platform_id": "ee3b4536-be4d-4539-881a-54bf69958a03"
#                     },
#                     "comparation": "LE",
#                     "value" : "100"
#                 },
#                 "bitwise_operator" : "AND"
#             }
#         ]
#     },
#     "condition_id" : "condition_id_1",
#     "action": {
#         "action_id" : "action_id_1",
#         "action" : [
#             {
#                 "time": "20s",
#                 "action_type": "update",
#                 "sub_action_id" : "sub_action_id_1",
#                 "description" : "this is a action sample",
#                 "config" : {
#                     "item" : {
#                         "platform_id": "ee3b4536-be4d-4539-881a-54bf69958a03",
#                         "item_name" : "Temperature",
#                         "item_global_id": "4f1e9cb2-a8be-4b54-81da-53d8659d4b73",
#                         "thing_global_id" : "6d0bb781-d2cb-4ff7-809e-f69ab1794b91"
#                     },
#                     "value" : "OFF"
#                 }
#             },
#             {
#                 "time": "30s",
#                 "action_type": "update",
#                 "sub_action_id" : "sub_action_id_2",
#                 "description" : "this is a action sample",
#                 "config" : {
#                     "item" : {
#                         "platform_id": "ee3b4536-be4d-4539-881a-54bf69958a03",
#                         "thing_global_id" : "607e994f-6bcc-4c0f-9be0-e11e103712c0",
#                         "item_name" : "Red Light",
#                         "item_global_id": "335dee5e-3dda-46a7-b2e0-63f87a5d7be1"
#                     },
#                     "value" : "OFF"
#                 }
#             }
#         ]
#     },
#     "action_id" : "action_id_1"
# }
#
#
# rule_1 = json.dumps(rule_1)
# rule_id = json.loads(rule_1)['rule_id']
# rule_name = json.loads(rule_1)['rule_name']
# rule_status = json.loads(rule_1)['rule_status']
# trigger_id = json.loads(rule_1)['trigger_id']
# condition_id = json.loads(rule_1)['condition_id']
# action_id = json.loads(rule_1)['action_id']
# trigger_content = json.dumps(json.loads(rule_1)['trigger'])
# condition_content = json.dumps(json.loads(rule_1)['condition'])
# action_content = json.dumps(json.loads(rule_1)['action'])
# insert_time = str(datetime.datetime.now())
#
# sql = """INSERT INTO RuleTable(rule_id, rule_name, rule_status, trigger_id, condition_id, action_id, trigger_content, condition_content, action_content, insert_time)
#                 VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
#                 % (rule_id, rule_name, rule_status, trigger_id, condition_id, action_id, trigger_content, condition_content, action_content, insert_time)
#
# cursor.execute(sql)






'''

rule_2 = {
    "rule_id": str(random.randint(0, 1000000000)),
    "rule_name": "a toy rule",
    "rule_status" : "enable",
    "trigger" : {
        "trigger_id" : "trigger_id_2",
        "trigger_type" : "item_has_given_state",
        "description" : "example of trigger",
        "config" : [
            {
                "constraint" : {
                    "time": "60s",
                    "item" : {
                        "thing_global_id": "10ac216a-6f51-43bb-86fa-8d7a5a8947ff",
                        "item_global_id": "04fa6c2b-6fc3-4c61-ae53-4a9cc2188090",
                        "item_name": "light",
                        "item_type" : "int",
                        "platform_id": "a3f6e492-5e20-47a4-ace9-5011316974ad"
                    },
                    "comparation": "LE",
                    "value" : "100"
                },
                "bitwise_operator" : "None",
            },
            {
                "constraint" : {
                    "time": "10s",
                    "item" : {
                        "thing_global_id": "10ac216a-6f51-43bb-86fa-8d7a5a8947ff",
                        "item_global_id": "2cac0319-9aad-4117-a65e-c3a710d2288a",
                        "item_name": "humidity",
                        "item_type" : "int",
                        "platform_id": "a3f6e492-5e20-47a4-ace9-5011316974ad"
                    },
                    "comparation": "LE",
                    "value" : "100"
                },
                "bitwise_operator" : "AND"
            }
        ],
        "outputs" : [
            {
                "event_name" : "event_1",
                "event_id" : "event_id_1",
                "event_source" : "trigger_id_2",
                "description" : "motion detected!"
            },
            {
                "event_name" : "event_2",
                "event_id" : "event_id_2",
                "event_source" : "trigger_id_2",
                "description" : "measure humidity"
            }
        ]
    },
    "trigger_id" : "trigger_id_2",
    "condition" : {
        "condition_id" : "condition_id_2",
        "condition_type" : "item_has_given_state",
        "description" : "Sample Condition description",
        "config" : [
            {
                "constraint" : {
                    "time": "60s",
                    "item" : {
                        "thing_global_id": "10ac216a-6f51-43bb-86fa-8d7a5a8947ff",
                        "item_global_id": "940347de-8cd8-417f-b0b3-0d63d1d47278",
                        "item_name": "temperature",
                        "item_type" : "int",
                        "platform_id": "a3f6e492-5e20-47a4-ace9-5011316974ad"
                    },
                    "comparation": "LE",
                    "value" : "100"
                },
                "bitwise_operator" : "None"
            },
            {
                "constraint" : {
                    "time": "10s",
                    "item" : {
                        "thing_global_id": "4152ecef-1458-4427-af61-431f525b6cb8",
                        "item_global_id": "0f3ecd50-c870-464c-a4cf-76b5e8b34874",
                        "item_name": "Humidity",
                        "item_type" : "int",
                        "platform_id": "ee3b4536-be4d-4539-881a-54bf69958a03"
                    },
                    "comparation": "LE",
                    "value" : "100"
                },
                "bitwise_operator" : "AND"
            }
        ]
    },
    "condition_id" : "condition_id_2",
    "action": {
        "action_id" : "action_id_2",
        "action" : [
            {
                "time": "20s",
                "action_type": "write_log",
                "sub_action_id" : "sub_action_id_1",
                "description" : "write log",
                "config" : {
                    "file_name": "test_log",
                    "format" : ".txt"
                }
            },
            {
                "time": "30s",
                "action_type": "write_log",
                "sub_action_id" : "sub_action_id_2",
                "description" : "write log",
                "config" : {
                    "file_name": "test_log",
                    "format" : ".logs"
                }
            }
        ]
    },
    "action_id" : "action_id_2"
}

rule_2 = json.dumps(rule_2)
rule_id = json.loads(rule_2)['rule_id']
rule_name = json.loads(rule_2)['rule_name']
rule_status = json.loads(rule_2)['rule_status']
trigger_id = json.loads(rule_2)['trigger_id']
condition_id = json.loads(rule_2)['condition_id']
action_id = json.loads(rule_2)['action_id']
trigger_content = json.dumps(json.loads(rule_2)['trigger'])
condition_content = json.dumps(json.loads(rule_2)['condition'])
action_content = json.dumps(json.loads(rule_2)['action'])
insert_time = str(datetime.datetime.now())

sql = """INSERT INTO RuleTable(rule_id, rule_name, rule_status, trigger_id, condition_id, action_id, trigger_content, condition_content, action_content, insert_time)
                VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
      % (rule_id, rule_name, rule_status, trigger_id, condition_id, action_id, trigger_content, condition_content, action_content, insert_time)

cursor.execute(sql)
'''



db.commit()
cursor.close()