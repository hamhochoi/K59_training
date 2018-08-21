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
    "rule_name": "send alert",
    "rule_status" : "enable",
    "rule_condition" : {
        "bitwise" : {
            "things" : [
                {
                    "timer": "60s",
                    "thing_global_id": "dd9b371b-44f2-44d8-96d2-a9e22bc013a7-Temperature",
                    "item_global_id": "dd9b371b-44f2-44d8-96d2-a9e22bc013a7-Temperature-Temperature",
                    "item_name": "Humidity",
                    "item_type" : "binary_sensor",
                    "platform_id": "dd9b371b-44f2-44d8-96d2-a9e22bc013a7",
                    "comparation": "LE",
                    "value" : "100"
                }
            ],

            "bitwise_operator" : "AND",

            "bitwise" : [
                {
                    "things" : [
                        {
                            "timer": "10s",
                            "thing_global_id": "73364ce9-7edb-454c-9e1a-4c5f44dcdaf2-Humidity",
                            "item_global_id": "73364ce9-7edb-454c-9e1a-4c5f44dcdaf2-Humidity-Humidity",
                            "item_name": "Temperature",
                            "item_type" : "binary_sensor",
                            "platform_id": "73364ce9-7edb-454c-9e1a-4c5f44dcdaf2",
                            "comparation": "LE",
                            "value" : "100"
                        }
                    ],
                    "bitwise_operator" : "None",
                    "bitwise" : []
                }
            ]
        }
    },

    "rule_action": [
        {
            "timer": "20s",
            "action_type": "update",
            "platform_id": "73364ce9-7edb-454c-9e1a-4c5f44dcdaf2",
            "item_name" : "Humidity",
            "item_global_id": "dd9b371b-44f2-44d8-96d2-a9e22bc013a7-Humidity-Humidity",
            "new_state" : '50'
        },
        {
            "timer": "30s",
            "action_type": "update",
            "platform_id": "dd9b371b-44f2-44d8-96d2-a9e22bc013a7",
            "item_name" : "LedVang",
            "item_global_id": "dd9b371b-44f2-44d8-96d2-a9e22bc013a7-LedVang-LedVang",
            "new_state" : 'OFF'
        }
    ]
}


rule_1 = {
    "rule_id": "606078797",
    "rule_name": "send alert",
    "rule_status" : "disable",
    "rule_condition" : {
        "bitwise" : {
            "things" : [
                {
                    "timer": "60s",
                    "thing_global_id": "f3fe8c9a-f524-481e-acff-fb2791f0a0b5-Temperature",
                    "item_global_id": "f3fe8c9a-f524-481e-acff-fb2791f0a0b5-Temperature-Temperature",
                    "item_name": "Motion Detection",
                    "item_type" : "Number",
                    "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
                    "comparation": "LEQ",
                    "value" : "100"
                }
            ],

            "bitwise_operator" : "AND",

            "bitwise" : [
                {
                    "things" : [
                        {
                            "timer": "60s",
                            "thing_global_id": "f3fe8c9a-f524-481e-acff-fb2791f0a0b5-Humidity",
                            "item_global_id": "f3fe8c9a-f524-481e-acff-fb2791f0a0b5-Humidity-Humidity",
                            "item_name": "Motion Detection",
                            "item_type" : "Number",
                            "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
                            "comparation": "LEQ",
                            "value" : "100"
                        }
                    ],
                    "bitwise_operator" : "None",
                    "bitwise" : []
                }
            ]
        }
    },

    "rule_action": [
        {
            "timer": "0s",
            "action_name": "update",
            "thing_global_id": "7ad2c82e-1036-4da7-8ccc-63d2dc52fb89-light.green_light",
            "item_global_id": "7ad2c82e-1036-4da7-8ccc-63d2dc52fb89-light.green_light-light.green_light",
            "new_state" : 'ON'
        },
        {
            "timer": "0s",
            "action_name": "send_alert",
            "thing_global_id": "a674ce40-8fc6-4f57-912c-d4679e189023-Switch3-Switch2",
            "item_global_id": "a674ce40-8fc6-4f57-912c-d4679e189023-Switch3-Switch2",
            "new_state" : 'OFF'
        }
    ]
}



if __name__ == "__main__":

    cursor.execute("""CREATE DATABASE IF NOT EXISTS rule""")
    cursor.execute("""USE rule""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Rule(
        rule_id VARCHAR(100) PRIMARY KEY,
        rule_name TEXT(100) ,
        rule_status VARCHAR(10),
        rule_condition VARCHAR(10000),
        rule_action VARCHAR(10000),
        insert_time INT)  """)

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


