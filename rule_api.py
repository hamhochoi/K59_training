from flask import Flask
from flask import json
from flask import jsonify
from flask import request
import json
import os
import MySQLdb
import time
import random


app = Flask(__name__)

db = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root")
cursor = db.cursor()

save_set_state = []
data_list = []


@app.route('/rule', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api():
    global data_list
    if request.method == 'GET':
        return jsonify(data_list)

    elif request.method == 'POST':
        data = request.json
        print (data)
        rule_status = data['rule_status']

        if (rule_status == "enable"):
            resutl = save_data(data)
            data_list = load_data_from_db()
            print (data_list)
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

    rule_id        = data["rule_id"]
    rule_name      = data["rule_name"]
    rule_condition = data["rule_condition"]
    rule_action    = data["rule_action"]
    rule_condition = json.dumps(rule_condition)
    rule_action    = json.dumps(rule_action)
    rule_status = "enable"
    insert_time = time.time()
    result = None
    # print (rule_condition)

    sql = """INSERT INTO Rule(rule_id,
         rule_name, rule_status, rule_condition, rule_action, insert_time)
         VALUES ("%s", "%s", "%s", '%s', '%s', %f)""" % (rule_id, rule_name, rule_status, rule_condition, rule_action, insert_time)

    # print (sql)
    # result = cursor.execute(sql)
    # print (result)
    # db.commit()

    try:
        # Execute the SQL command
        result = cursor.execute(sql)
        # print ("save result: ", result)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

    return result


def load_data_from_db(n_record=None):
    list_rule = []

    if (n_record == None):
        query_statement = 'SELECT * FROM Rule WHERE rule_status = "enable" ORDER BY insert_time DESC'
    else:
        query_statement = 'SELECT * FROM Rule WHERE rule_status = "enable" ORDER BY insert_time DESC LIMIT' + str(n_record)

    # cursor.execute(query_statement)
    # # Fetch all the rows in a list of lists.
    # results = cursor.fetchall()
    # print (results)

    try:
        # Execute the SQL command
        cursor.execute(query_statement)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        # print (results)
        for row in results:

            rule = {
                'rule_id'           : row[0],
                'rule_name'         : row[1],
                'rule_status'       : row[2],
                'rule_condition'    : json.loads(row[3]),
                'rule_action'       : json.loads(row[4])
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

    rule_id     = data['rule_id']
    rule_status = "disable"

    sql = 'UPDATE Rule SET rule_status = "%s" WHERE rule_id = "%s"' % (rule_status, rule_id)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()


def update_data(data):
    data = json.dumps(data)
    data = json.loads(data)

    rule_id     = data['rule_id']
    rule_status = "enable"
    print (rule_status)
    rule_name   = data['rule_name']
    rule_condition   = json.dumps(data['rule_condition'])
    rule_action = json.dumps(data['rule_action'])

    sql = """UPDATE Rule SET rule_status = "%s", 
             rule_condition = '%s', rule_action = '%s',
             rule_name = "%s" WHERE rule_id = "%s" """ \
             % (rule_status, rule_condition, rule_action, rule_name, rule_id)

    #print (sql)
    try:
        # Execute the SQL command
        result = cursor.execute(sql)
        print ("result: ", result)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        print ("update error")
        db.rollback()

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
                        "thing_global_id": "10ac216a-6f51-43bb-86fa-8d7a5a8947ff",
                        "item_global_id": "04fa6c2b-6fc3-4c61-ae53-4a9cc2188090",
                        "item_name": "light",
                        "item_type" : "int",
                        "platform_id": "a3f6e492-5e20-47a4-ace9-5011316974ad"
                    }
                    "comparation": "LE",
                    "value" : "100"
                },
                "bitwise_operator" : "AND",
                "bitwise" : {
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
                    }
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
    "condition" : {
        "condition_id" : "condition_id_1",
        "condition_type" : "item_has_given_state",
        "description" : "Sample Condition description",
        "config" : {
            "bitwise" : {
                "constraint" : {
                    "time": "60s",
                    "item" : { 
                        "thing_global_id": "10ac216a-6f51-43bb-86fa-8d7a5a8947ff",
                        "item_global_id": "940347de-8cd8-417f-b0b3-0d63d1d47278",
                        "item_name": "temperature",
                        "item_type" : "int",
                        "platform_id": "a3f6e492-5e20-47a4-ace9-5011316974ad"
                    }
                    "comparation": "LE",
                    "value" : "100"
                },
                "bitwise_operator" : "AND",
                "bitwise" : {
                    "constraint" : {
                        "time": "10s",
                        "item" : {
                            "thing_global_id": "4152ecef-1458-4427-af61-431f525b6cb8",
                            "item_global_id": "0f3ecd50-c870-464c-a4cf-76b5e8b34874",
                            "item_name": "Humidity",
                            "item_type" : "int",
                            "platform_id": "ee3b4536-be4d-4539-881a-54bf69958a03"
                        }
                        "comparation": "LE",
                        "value" : "100"
                    },
                    "bitwise_operator" : "None",
                    "bitwise" : []
                }
            }
        }
    },
    "action": [
        {
            "action_type": "update",
            "action_id" : "action_id_1",
            "description" : "this is a action sample",
            "config" : {
                "time": "20s",
                "platform_id": "ee3b4536-be4d-4539-881a-54bf69958a03",
                "item_name" : "Temperature",
                "item_global_id": "93c67f78-2d89-48fa-b016-6969db4cfcd8",
                "thing_global_id" : "5155ed62-5a23-4aa1-94b1-aef53eee25fb",
                "value" : '50'
            }
        },
        {
            "action_type": "update",
            "action_id" : "action_id_2",
            "description" : "this is a action sample",
            "config" : {
                "time": "30s",
                "platform_id": "ee3b4536-be4d-4539-881a-54bf69958a03",
                "thing_global_id" : "607e994f-6bcc-4c0f-9be0-e11e103712c0",
                "item_name" : "Red Light",
                "item_global_id": "607e994f-6bcc-4c0f-9be0-e11e103712c0",
                "value" : 'OFF'
            }
        }
    ]
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
                    "value" : "100"
                },
                "bitwise_operator" : "AND",
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
                "bitwise_operator" : "None"
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
                "bitwise_operator" : "AND"
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
                "bitwise_operator" : "None"
            }
        ]
    },
    "action": {
        "action_id" : "action_id_1",
        "action" : [
            {
                "time": "20s",
                "action_type": "update",
                "action_id" : "action_id_1",
                "description" : "this is a action sample",
                "config" : {
                    "platform_id": "ee3b4536-be4d-4539-881a-54bf69958a03",
                    "item_name" : "Temperature",
                    "item_global_id": "93c67f78-2d89-48fa-b016-6969db4cfcd8",
                    "thing_global_id" : "5155ed62-5a23-4aa1-94b1-aef53eee25fb",
                    "value" : "50"
                }
            },
            {
                "time": "30s",
                "action_type": "update",
                "action_id" : "action_id_1",
                "description" : "this is a action sample",
                "config" : {
                    "platform_id": "ee3b4536-be4d-4539-881a-54bf69958a03",
                    "thing_global_id" : "607e994f-6bcc-4c0f-9be0-e11e103712c0",
                    "item_name" : "Red Light",
                    "item_global_id": "607e994f-6bcc-4c0f-9be0-e11e103712c0",
                    "value" : "OFF"
                }
            }
        ]
    }
}



if __name__ == "__main__":

    cursor.execute("""CREATE DATABASE IF NOT EXISTS rule""")
    cursor.execute("""USE rule""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Rule(
        rule_id VARCHAR(100) PRIMARY KEY,
        rule_name VARCHAR(100),
        rule_status VARCHAR(10),
        trigger_id VARCHAR(100),
        condition_id VARCHAR(100), 
        action_id VARCHAR(100),
        trigger JSON,
        condition JSON,
        action JSON,
        insert_time VARCHAR(100))  """)

    # print (json.dumps(rule))
    #save_data(rule)
    # delete_data(rule_1)


    try:
        data_list = load_data_from_db()
        # print ("data_list: ", data_list)
        app.run(host='0.0.0.0')
    except:
        db.commit()
        cursor.close()


