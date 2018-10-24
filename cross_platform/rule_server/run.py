from flask import Flask  
from flask import json
from flask import jsonify
from flask import request
import json
import os
import MySQLdb
import time

app = Flask(__name__)

db = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root")
cursor = db.cursor()
cursor.execute("""USE rule""")


data_list = []


@app.route('/rule', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api():
    global data_list
    if request.method == 'GET':
        return jsonify(data_list)

    elif request.method == 'POST':
        data = request.json
        # print (data)
        rule_status = data['rule_status']

        if (rule_status == "active"):
            resutl = save_data(data)
            data_list = load_data_from_db()
            print (data_list)
        elif (rule_status == "inactive"):
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


def save_data(data):
    data = json.dumps(data) 
    data = json.loads(data)
    
    rule_id     = data["rule_id"]
    rule_name   = data["rule_name"]
    rule_condition   = data["rule_condition"]
    rule_condition = json.dumps(rule_condition)
    rule_status = "active"
    insert_time = time.time()
    result = None
    # print (rule_condition)

    sql = """INSERT INTO Rule(rule_id,
         rule_name, rule_status, rule_condition, insert_time)
         VALUES ("%s", "%s", "%s", '%s', %f)""" % (rule_id, rule_name, rule_status, rule_condition, insert_time)

    print (sql)
    result = cursor.execute(sql)
    print (result)
    db.commit()

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
        query_statement = 'SELECT * FROM Rule WHERE rule_status = "active" ORDER BY insert_time DESC'
    else:
        query_statement = 'SELECT * FROM Rule WHERE rule_status = "active" ORDER BY insert_time DESC LIMIT' + str(n_record)
    
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
                'rule_condition'    : json.loads(row[3])
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
    rule_status = "inactive"

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
    rule_status = data['rule_status']
    print (rule_status)
    rule_name   = data['rule_name']
    rule_condition   = json.dumps(data['rule_condition'])

    sql = """UPDATE Rule SET rule_status = "%s", rule_condition = '%s', rule_name = "%s" WHERE rule_id = "%s" """% (rule_status, rule_condition, rule_name, rule_id)
    print (sql)
    try:
        # Execute the SQL command
        result = cursor.execute(sql)
        print (result)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        print ("update error")
        db.rollback()

rule = {
        "rule_id": "21351c35dfdsf",
        "rule_name": "Motion light off",
        "rule_status" : "active", 
        "rule_condition" : {
            "bitwise" : {
                "things" : [
                    {
                        "timer": "60",
                        "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9.light",
                        "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-binary_sensor.motion_detection-binary_sensor.motion_detection",
                        "item_name": "Motion Detection",
                        "item_type" : "Switch",
                        "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
                        "operator": "EQ", 
                        "value" : "off"
                    }
                ],
                        
                "bitwise_operator" : "AND", 

                "bitwise" : [
                    {
                        "things" : [
                            {
                                "timer": "60",
                                "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
                                "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-binary_sensor.motion_detection-binary_sensor.motion_detection",
                                "item_name": "Motion Detection",
                                "item_type" : "Switch",
                                "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
                                "operator": "EQ", 
                                "value" : "off"
                            }
                        ],
                        "bitwise_operator" : "None", 
                        "bitwise" : []
                    } 
                ]
            }
        },
        "action": [
            {
                "timer": 0,
                "action_name": "light_off",
                "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
                "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light-sensor.light",
                "new_state" : "off"
            }, 
            {
                "timer": 0,
                "action_name": "light_off",
                "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
                "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light-sensor.light",
                "new_state" : "off"
            }
        ]
    }


rule_1 = {
        "rule_id": "asdfasdfhlajsd",
        "rule_name": "Motion light off",
        "rule_status" : "active", 
        "rule_condition" : {
            "bitwise" : {
                "things" : [
                    {
                        "timer": "60",
                        "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9.light",
                        "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-binary_sensor.motion_detection-binary_sensor.motion_detection",
                        "item_name": "Motion Detection",
                        "item_type" : "Switch",
                        "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
                        "operator": "EQ", 
                        "value" : "off"
                    }
                ],
                        
                "bitwise_operator" : "AND", 

                "bitwise" : [
                    {
                        "things" : [
                            {
                                "timer": "60",
                                "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
                                "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-binary_sensor.motion_detection-binary_sensor.motion_detection",
                                "item_name": "Motion Detection",
                                "item_type" : "Switch",
                                "platform_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9",
                                "operator": "EQ", 
                                "value" : "off"
                            }
                        ],
                        "bitwise_operator" : "None", 
                        "bitwise" : []
                    } 
                ]
            }
        },
        
        "action": [
            {
                "timer": 0,
                "action_name": "light_off",
                "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
                "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light-sensor.light",
                "new_state" : "off"
            }, 
            {
                "timer": 0,
                "action_name": "light_off",
                "thing_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light",
                "item_global_id": "d7fefe33-2f39-47f8-a229-18cf4376a3c9-sensor.light-sensor.light",
                "new_state" : "off"
            }
        ]
    }



if __name__ == "__main__":

    cursor.execute("""CREATE TABLE IF NOT EXISTS Rule(
        rule_id VARCHAR(100) PRIMARY KEY,
        rule_name TEXT(100) ,
        rule_status VARCHAR(10),
        rule_condition VARCHAR(10000),
        insert_time INT)  """)

    # print (json.dumps(rule))
    save_data(rule)
    # delete_data(rule_1)
    update_data(rule_1)

    try:
        data_list = load_data_from_db()
        # print ("data_list: ", data_list)
        app.run()
    except:
        db.commit()
        cursor.close()




