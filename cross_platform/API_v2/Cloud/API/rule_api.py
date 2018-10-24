from flask import Flask
from flask import json
from flask import jsonify
from flask import request
import json
import os
import MySQLdb
import time
import random
import datetime

app = Flask(__name__)

db_api = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root")
cursor_api = db_api.cursor()

db_rule_engine = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root")
db_trigger = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root")

cursor_rule_engine = db_rule_engine.cursor()
cursor_trigger = db_trigger.cursor()


save_set_state = []
data_list = []


@app.route('/rule', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api():
    global data_list
    if request.method == 'GET':
        data_list = load_data_from_db()
        return jsonify(data_list)

    elif request.method == 'POST':
        data = request.json
        print (data)
        rule_status = data['rule_status']

        if (rule_status == "enable"):
            resutl = save_data(data)
            data_list = load_data_from_db()
            # print (data_list)
        elif (rule_status == "disable"):
            delete_data(data)
            data_list = load_data_from_db()
        elif (rule_status == "edit"):
            update_data(data)
            data_list = load_data_from_db()
        else:
            print ("Error: rule status not defined!")
            return -1

        return jsonify(data_list)

    # elif request.method == 'PATCH':
    #     return "ECHO: PACTH\n"

    # elif request.method == 'PUT':
    #     return "ECHO: PUT\n"

    # elif request.method == 'DELETE':
    #     return "ECHO: DELETE"


@app.route('/api_set_state', methods = ['GET', 'POST'])
def api_set_state():
    global save_set_state
    data = request.json
    save_set_state.append(data)

    return jsonify(save_set_state)


def save_data(data):
    data = json.dumps(data)
    data = json.loads(data)

    # print (type(data))

    rule_id        = data["rule_id"]
    rule_name      = data["rule_name"]
    rule_status    = "enable"
    trigger_id     = data["trigger_id"]
    trigger_type   = data["trigger"]["trigger_type"]
    condition_id   = data["condition_id"]
    action_id      = data["action_id"]

    trigger        = data["trigger"]
    condition      = data["condition"]
    action         = data["action"]

    trigger        = json.dumps(trigger)
    condition      = json.dumps(condition)
    action         = json.dumps(action)
    insert_time    = str(datetime.datetime.now())
    # print (type(trigger))
    result = None
    # print (rule_condition)

    sql = """INSERT INTO RuleTable(rule_id, rule_name, rule_status,
                             trigger_id, condition_id, action_id,
                             trigger_content, condition_content, 
                             action_content, insert_time)
         VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
         % (rule_id, rule_name, rule_status, trigger_id, condition_id, action_id, trigger, condition, action, insert_time)

    # print (sql)
    # result = cursor_api.execute(sql)
    # print (result)
    # db.commit()

    # Write data to rule_api 's database
    try:
        # Execute the SQL command
        result = cursor_api.execute(sql)
        print ("rule api save result: ", result)
        # Commit your changes in the database
        db_api.commit()
    except: 
        print ("error save data to rule_api")
        # Rollback in case there is any error
        db_api.rollback()


    # Write data to Rule Engine 's database
    try:
        # Execute the SQL command
        result = cursor_rule_engine.execute(sql)
        print ("rule engine save result: ", result)
        # Commit your changes in the database
        db_rule_engine.commit()
    except:
        print ("error save data to Rule Engine")
        # Rollback in case there is any error
        db_rule_engine.rollback()


    sql = """INSERT INTO TriggerTable(rule_id, trigger_id, trigger_type, trigger_content)
             VALUES ('%s', '%s', '%s', '%s')""" % (rule_id, trigger_id, trigger_type, trigger)

    print (sql)

    # Write data to Trigger database
    try:
        # Execute the SQL command
        result = cursor_trigger.execute(sql)
        print ("trigger save result: ", result)
        # Commit your changes in the database
        db_trigger.commit()
    except:
        print ("error save data to trigger")
        # Rollback in case there is any error
        db_trigger.rollback()

    return result


def load_data_from_db(n_record=None):
    list_rule = []

    if (n_record == None):
        query_statement = 'SELECT * FROM RuleTable WHERE rule_status = "enable" ORDER BY insert_time DESC'
    else:
        query_statement = 'SELECT * FROM RuleTable WHERE rule_status = "enable" ORDER BY insert_time DESC LIMIT ' + str(n_record)

    # cursor_api.execute(query_statement)
    # # Fetch all the rows in a list of lists.
    # results = cursor_api.fetchall()
    # print (results)

    try:
        # Execute the SQL command
        cursor_api.execute(query_statement)
        # Fetch all the rows in a list of lists.
        results = cursor_api.fetchall()
        # print (results)
        for column in results:
            rule = {
                'rule_id'           : column[0],
                'rule_name'         : column[1],
                'rule_status'       : column[2],
                'trigger_id'        : column[3],
                'condition_id'      : column[4],
                'action_id'         : column[5],
                'trigger'           : json.loads(column[6]),
                'condition'         : json.loads(column[7]),
                'action'            : json.loads(column[8])
            }
            # print (json.loads((json.dumps(rule['rule_condition']))))
            list_rule.append(rule)
            # print (rule['rule_condition'])
    except:
        print ("Error: unable to fecth data")

    # print (list_rule)
    return list_rule


def delete_data(data):
    data = json.dumps(data)
    data = json.loads(data)

    rule_id        = data["rule_id"]
    rule_name      = data["rule_name"]
    rule_status    = "enable"
    trigger_id     = data["trigger_id"]
    print ("trigger_id: ", trigger_id)
    trigger_type   = data["trigger"]["trigger_type"]
    condition_id   = data["condition"]["condition_id"]
    action_id      = data["action"]["action_id"]

    trigger        = data["trigger"]
    condition      = data["condition"]
    action         = data["action"]

    trigger        = json.dumps(trigger)
    condition      = json.dumps(condition)
    action         = json.dumps(action)


    rule_status = "disable"

    sql = 'UPDATE RuleTable SET rule_status = "%s" WHERE rule_id = "%s"' % (rule_status, rule_id)

    # Update to rule api
    try:
        # Execute the SQL command
        cursor_api.execute(sql)
        # Commit your changes in the database
        db_api.commit()
    except:
        print ("Error update to rule api")
        # Rollback in case there is any error
        db_api.rollback()


    # Update to Rule Engine
    try:
        # Execute the SQL command
        cursor_rule_engine.execute(sql)
        # Commit your changes in the database
        db_rule_engine.commit()
    except:
        print ("Error update to Rule Engine")
        # Rollback in case there is any error
        db_rule_engine.rollback()



    sql = 'DELETE FROM TriggerTable WHERE trigger_id = "%s"' % (trigger_id)
    # Update to Trigger
    try:
        # Execute the SQL command
        cursor_trigger.execute(sql)
        # Commit your changes in the database
        db_trigger.commit()
    except:
        print ("Error update to Trigger")
        # Rollback in case there is any error
        db_trigger.rollback()








def update_data(data):
    data = json.dumps(data)
    data = json.loads(data)

    rule_id     = data['rule_id']
    rule_status = "enable"
    trigger_id  = data["trigger_id"]
    condition_id = data["condition_id"]
    action_id = data["action_id"]

    # print ("trigger_id: ", trigger_id)
    trigger_type   = data["trigger"]["trigger_type"]
    # print (rule_status)
    rule_name   = data['rule_name']
    trigger     = json.dumps(data['trigger'])
    condition   = json.dumps(data['condition'])
    action      = json.dumps(data['action'])

    # print (rule_status)
    # print (type(trigger))
    # print (type(condition))
    # print (type(action))
    # print (rule_name)
    # print (rule_id)

    sql = """UPDATE RuleTable SET rule_status = '%s', trigger_id = '%s', trigger_content = '%s', condition_id = '%s', condition_content = '%s', action_id = '%s', action_content = '%s', rule_name = '%s' WHERE rule_id = '%s' """ \
             % (rule_status, trigger_id, trigger, condition_id, condition, action_id, action, rule_name, rule_id)

    print (sql)

    try:
        # Execute the SQL command
        result = cursor_api.execute(sql)
        print ("result: ", result)
        # Commit your changes in the database
        db_api.commit()
    except:
        # Rollback in case there is any error
        print ("update error")
        db_api.rollback()



    sql = """UPDATE RuleTable SET rule_status = '%s', trigger_id = '%s', trigger_content = '%s', condition_id = '%s', condition_content = '%s', action_id = '%s', action_content = '%s', rule_name = '%s' WHERE rule_id = '%s' """ \
             % (rule_status, trigger_id, trigger, condition_id, condition, action_id, action, rule_name, rule_id)

    print (sql)

    try:
        # Execute the SQL command
        result = cursor_rule_engine.execute(sql)
        print ("result: ", result)
        # Commit your changes in the database
        db_rule_engine.commit()
    except:
        # Rollback in case there is any error
        print ("update error")
        db_rule_engine.rollback()



    sql = """UPDATE TriggerTable SET trigger_content = '%s', trigger_id = '%s' where rule_id='%s'""" % (trigger, trigger_id, rule_id)

    print (sql)

    try:
        # Execute the SQL command
        result = cursor_trigger.execute(sql)
        print ("result: ", result)
        # Commit your changes in the database
        db_trigger.commit()
    except:
        # Rollback in case there is any error
        print ("update error")
        db_trigger.rollback()







rule = {
    "rule_id": str(random.randint(0, 1000000000)),
    "rule_name": "a toy rule",
    "rule_status" : "enable",
    "trigger" : {
        "trigger_id" : "trigger_id_1",
        "trigger_type" : "item_has_given_state",
        "description" : "example of trigger",
        "config" : {
            "bitwise" : {
                "constraint" : {
                    "time": "60s",
                    "item" : {
                        "thing_global_id": "Humidity",
                        "item_global_id": "Humidity",
                        "item_name": "Humidity",
                        "item_type" : "Number",
                        "platform_id": "OpenHAB"
                    },
                    "comparation": "LE",
                    "value" : "100"
                },
                "bitwise_operator" : "AND",
                "bitwise" : {
                    "constraint" : {
                        "time": "10s",
                        "item" : {
                            "thing_global_id": "Temperature",
                            "item_global_id": "Temperature",
                            "item_name": "Temperature",
                            "item_type" : "Number",
                            "platform_id": "OpenHAB"
                        },
                        "comparation": "LE",
                        "value" : "100"
                    },
                    "bitwise_operator" : "None",
                    "bitwise" : {}
                }
            }
        },
        "outputs" : [
            {
              "event_name" : "event_1",
              "event_id" : "event_id_1",
              "event_source" : "motion_1",
              "trigger_id" : "trigger_id_1",
              "description" : "motion detected!"
            },
            {
              "event_name" : "event_2",
              "event_id" : "event_id_2",
              "event_source" : "humidity_2",
              "trigger_id" : "trigger_id_1",
              "description" : "measure humidity"
            }
        ]
    },
    "trigger_id" : "trigger_id_1",
    "condition" : {
        "condition_id" : "condition_id_1",
        "condition_type" : "item_has_given_state",
        "description" : "Sample Condition description",
        "config" : {
            "bitwise" : {
                "constraint" : {
                    "time": "0s",
                    "item" : { 
                        "thing_global_id": "LedVang",
                        "item_global_id": "LedVang",
                        "item_name": "LedVang",
                        "item_type" : "Switch",
                        "platform_id": "OpenHAB"
                    },
                    "comparation": "EQ",
                    "value" : "OFF"
                },
                "bitwise_operator" : "AND",
                "bitwise" : {
                    "constraint" : {
                        "time": "0",
                        "item" : {
                            "thing_global_id": "LedXanh",
                            "item_global_id": "LedXanh",
                            "item_name": "LedXanh",
                            "item_type" : "Switch",
                            "platform_id": "OpenHAB"
                        },
                        "comparation": "EQ",
                        "value" : "OFF"
                    },
                    "bitwise_operator" : "None",
                    "bitwise" : []
                }
            }
        }
    },
    "condition_id" : "condition_id_1",
    "action": {
        "action_id" : "action_id_1",
        "action" : [
            {
                "action_type": "write_log",
                "sub_action_id" : "sub_action_id_1",
                "description" : "this is a action sample",
                "config" : {
                    "time": "0s",
                    "platform_id": "OpenHAB",
                    "item_name" : "LedDo",
                    "item_global_id": "LedDo",
                    "thing_global_id" : "LedDo",
                    "value" : 'ON'
                }
            },
            {
                "action_type": "update",
                "sub_action_id" : "sub_action_id_2",
                "description" : "this is a action sample",
                "config" : {
                    "time": "0s",
                    "platform_id": "LedVang",
                    "thing_global_id" : "LedVang",
                    "item_name" : "LedVang",
                    "item_global_id": "LedVang",
                    "value" : 'ON'
                }
            }
        ]
    },
    "action_id" : "action_id_1"
}

# Another way to present the relationship between things in trigger, condition

rule_1 = {
    "rule_id": str(random.randint(0, 1000000000)),
    "rule_name": "a toy rule",
    "rule_status" : "enable",
    "trigger" : {
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
    },
    "trigger_id" : "trigger_id_1",
    "condition" : {
        "condition_id" : "condition_id_1",
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
    "condition_id" : "condition_id_1",
    "action": {
        "action_id" : "action_id_1",
        "action" : [
            {
                "time": "20s",
                "action_type": "write_log",
                "sub_action_id" : "sub_action_id_1",
                "description" : "this is a action sample",
                "config" : {
                    "file_name": "test_log",
                    "format" : ".txt"
                }
            },
            {
                "time": "30s",
                "action_type": "write_log",
                "sub_action_id" : "sub_action_id_2",
                "description" : "this is a action sample",
                "config" : {
                    "file_name": "test_log",
                    "format" : ".logs"
                }
            }
        ]
    },
    "action_id" : "action_id_1"
}



if __name__ == "__main__":

    cursor_rule_engine.execute("""CREATE DATABASE IF NOT EXISTS RuleEngine_DB""")
    cursor_trigger.execute("""CREATE DATABASE IF NOT EXISTS Trigger_DB""")
    cursor_api.execute("""CREATE DATABASE IF NOT EXISTS RuleAPI_DB""")

    cursor_api.execute("""use RuleAPI_DB""")
    cursor_rule_engine.execute("""use RuleEngine_DB""")
    cursor_trigger.execute("""use Trigger_DB""")


    cursor_api.execute("""CREATE TABLE IF NOT EXISTS RuleTable(
        rule_id VARCHAR(100) PRIMARY KEY,
        rule_name VARCHAR(100),
        rule_status VARCHAR(100),
        trigger_id VARCHAR(100),
        condition_id VARCHAR(100), 
        action_id VARCHAR(100),
        trigger_content VARCHAR(20000),
        condition_content VARCHAR(20000),
        action_content VARCHAR(20000),
        insert_time VARCHAR(100))  """)


    cursor_rule_engine.execute("""CREATE TABLE IF NOT EXISTS RuleTable(
        rule_id VARCHAR(100) PRIMARY KEY,
        rule_name VARCHAR(100),
        rule_status VARCHAR(100),
        trigger_id VARCHAR(100),
        condition_id VARCHAR(100), 
        action_id VARCHAR(100),
        trigger_content VARCHAR(20000),
        condition_content VARCHAR(20000),
        action_content VARCHAR(20000),
        insert_time VARCHAR(100))  """)


    cursor_trigger.execute("""CREATE TABLE IF NOT EXISTS TriggerTable(
    rule_id VARCHAR(100),
    trigger_id VARCHAR(100) PRIMARY KEY,
    trigger_type VARCHAR(100),
    trigger_content VARCHAR(20000))""")

    # print (json.dumps(rule))
    # save_data(rule)
    # delete_data(rule_1)


    try:
        data_list = load_data_from_db()
        # print ("data_list: ", data_list)
        app.run(host='0.0.0.0')
    except:
        db_api.commit()
        db_rule_engine.commit()
        db_trigger.commit()
        cursor_api.close()
        cursor_rule_engine.close()
        cursor_trigger.close()


