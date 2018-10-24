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

db_trigger = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root")
cursor_trigger = db_trigger.cursor()

db_engine = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root")
cursor_engine = db_engine.cursor()




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



@app.route('/api_set_state', methods = ['GET', 'POST'])
def api_set_state():
    global save_set_state
    data = request.json
    save_set_state.append(data)

    return jsonify(save_set_state)



def save_data(data):
    data = json.dumps(data)
    data = json.loads(data)

    print ("data :", data)

    rule_id        = data["rule_id"]
    rule_name      = data["rule_name"]

    trigger_id     = data["trigger_id"]
    trigger_content= data["trigger"]
    condition_id   = data["condition_id"]
    condition_content = data["condition"]
    action_id      = data["action_id"]
    action_content = data["action"]

    # print ("\n\ntrigger_content: ", trigger_content)

    trigger_content = json.dumps(trigger_content)
    # trigger_content = json.loads(trigger_content)

    trigger_type = json.loads(trigger_content)["trigger_type"]
    # print ("\ntrigger_type: ", trigger_type)

    condition_content = json.dumps(condition_content)
    # condition_content = json.loads(condition_content)
    # print ("\ncondition_content: ", condition_content)

    action_content = json.dumps(action_content)
    # action_content = json.loads(action_content)
    # print ("\naction_content: ", action_content)


    rule_status = "enable"
    insert_time = time.time()
    result = None


    sql = """INSERT INTO RuleTable(rule_id, rule_name,
         rule_status, trigger_id, trigger_content, 
         condition_id, condition_content,
         action_id, action_content, insert_time)
         VALUES ("%s", "%s", "%s", "%s", '%s', "%s", '%s', "%s", '%s', %f)""" % (rule_id, rule_name, rule_status, trigger_id, trigger_content, condition_id, condition_content, action_id, action_content, insert_time)

    print ("sql: ", sql)

    try:
        # Execute the SQL command
        result = cursor.execute(sql)
        print ("save result: ", result)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        print ("error save rule api")
        db.rollback()





    sql = """INSERT INTO RuleTable(rule_id, rule_name,
         rule_status, trigger_id, trigger_content, 
         condition_id, condition_content,
         action_id, action_content, insert_time)
         VALUES ("%s", "%s", "%s", "%s", '%s', "%s", '%s', "%s", '%s', %f)""" % (rule_id, rule_name, rule_status, trigger_id, trigger_content, condition_id, condition_content, action_id, action_content, insert_time)

    print ("sql rule engine: ", sql)

    try:
        # Execute the SQL command
        result = cursor_engine.execute(sql)
        print ("save rule engine result: ", result)
        # Commit your changes in the database
        db_engine.commit()
    except:
        # Rollback in case there is any error
        db_engine.rollback()





    sql = """INSERT INTO TriggerTable(rule_id,
         trigger_id, trigger_type, trigger_content)
         VALUES ("%s", "%s", "%s", '%s')""" % (rule_id, trigger_id, trigger_type, trigger_content)


    print ("trigger sql: ", sql)

    try:
        # Execute the SQL command
        result = cursor_trigger.execute(sql)
        print ("save trigger result: ", result)
        # Commit your changes in the database
        db_trigger.commit()
    except:
        # Rollback in case there is any error
        db_trigger.rollback()


    return result


def load_data_from_db(n_record=None):
    list_rule = []

    if (n_record == None):
        query_statement = 'SELECT rule_id, rule_status, rule_name, trigger_id, trigger_content, condition_id, condition_content, action_id, action_content FROM RuleTable WHERE rule_status = "enable" ORDER BY insert_time DESC'
    else:
        query_statement = 'SELECT rule_id, rule_status, rule_name, trigger_id, trigger_content, condition_id, condition_content, action_id, action_content FROM RuleTable WHERE rule_status = "enable" ORDER BY insert_time DESC LIMIT' + str(n_record)

    cursor.execute(query_statement)
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()

    # print (query_statement)

    # print (results)

    try:
        # Execute the SQL command
        cursor.execute(query_statement)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        # print (results)


        for row in results:
            # print ("row: ", row)
            # print ("\n\n\n\n")
            rule = {
                'rule_id'           : row[0],
                'rule_status'       : row[1],
                'rule_name'         : row[2],
                'trigger_id'        : row[3],
                'trigger'           : json.loads(row[4]),
                'condition_id'      : row[5],
                'condition'         : json.loads(row[6]),
                'action_id'         : row[7],
                'action'            : json.loads(row[8])
            }


            list_rule.append(rule)
            # print (rule['rule_condition'])

        # print ("list rule: ", list_rule)

    except:
        print ("Error: unable to fecth data")

    # print (list_rule)
    return list_rule


def delete_data(data):
    data = json.dumps(data)
    data = json.loads(data)

    rule_id     = data['rule_id']
    rule_status = "disable"

    trigger_id  = data["trigger_id"]

    sql = 'UPDATE RuleTable SET rule_status = "%s" WHERE rule_id = "%s"' % (rule_status, rule_id)
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()





    sql = 'UPDATE RuleTable SET rule_status = "%s" WHERE rule_id = "%s"' % (rule_status, rule_id)
    try:
        # Execute the SQL command
        cursor_engine.execute(sql)
        # Commit your changes in the database
        db_engine.commit()
    except:
        # Rollback in case there is any error
        db_engine.rollback()


    sql = "delete from TriggerTable where trigger_id='%s' " % (trigger_id)
    try:
        # Execute the SQL command
        cursor_trigger.execute(sql)
        # Commit your changes in the database
        db_trigger.commit()
    except:
        # Rollback in case there is any error
        db_trigger.rollback()



def update_data(data):
    data = json.dumps(data)
    data = json.loads(data)

    rule_id        = data["rule_id"]
    rule_name      = data["rule_name"]

    trigger_id     = data["trigger_id"]
    trigger_content= data["trigger"]
    condition_id   = data["condition_id"]
    condition_content = data["condition"]
    action_id      = data["action_id"]
    action_content = data["action"]

    trigger_content = json.dumps(trigger_content)
    condition_content = json.dumps(condition_content)
    action_content = json.dumps(action_content)

    trigger_type = trigger_content["trigger_type"]
    # print ("trigger_type: ", trigger_type)

    rule_status = "enable"
    # print (rule_status)

    rule_content   = json.dumps(data)

    sql = """UPDATE RuleTable SET rule_status = "%s", 
             rule_name = "%s", trigger_id="%s", trigger_content="%s",
             condition_id="%s", condition_content="%s", 
             action_id="%s", action_content="%s" WHERE rule_id = "%s" """ \
          % (rule_status, rule_name, trigger_id, trigger_content, condition_id, condition_content, action_id, action_content, rule_id)

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



    sql = """UPDATE RuleTable SET rule_status = "%s", 
             rule_name = "%s", trigger_id="%s", trigger_content="%s",
             condition_id="%s", condition_content="%s", 
             action_id="%s", action_content="%s" WHERE rule_id = "%s" """ \
          % (rule_status, rule_name, trigger_id, trigger_content, condition_id, condition_content, action_id, action_content, rule_id)


    try:
        # Execute the SQL command
        result = cursor_engine.execute(sql)
        print ("result: ", result)
        # Commit your changes in the database
        db_engine.commit()
    except:
        # Rollback in case there is any error
        print ("update error")
        db_engine.rollback()




    sql = """UPDATE TriggerTable SET trigger_id="%s", trigger_type="%s", trigger_content="%s" WHERE rule_id = "%s" """ \
          % (trigger_id, trigger_type, trigger_content, rule_id)







rule = {
    "action": {
        "action":[
            {
                "action_type":"call_cross_platform_api",
                "config":{
                    "item":
                        {
                            "item_global_id":"9ca7eae3-babb-4160-aeef-4a2af2967357",
                            "item_name":"LedXanh",
                            "item_type":"Gauge",
                            "platform_id":"80001edf-1e80-42dc-bb5a-3c88a64e47df",
                            "thing_global_id":"61e7e36c-c937-44ed-8409-16f751fb0240"
                        },
                    "value":"on"
                },
                "sub_action_id":"zos1veotg",
                "time":"00s"
            }
        ],
        "action_id":"aa8z847i8"
    },
    "action_id":"aa8z847i8",
    "condition":{
        "condition_id":"dbikelbi4",
        "condition_type":"item_has_given_state",
        "config":[
            {
                "bitwise_operator":"None",
                "constraint":{
                    "comparation":"GT",
                    "item":{
                        "item_global_id":"375b63de-b3f4-4332-8fea-d07d4d9fac97",
                        "item_name":"Temperature",
                        "item_type":"Gauge",
                        "platform_id":"0e3486ee-cfea-4219-820c-0aca41e1539a",
                        "thing_global_id":"05602528-0686-49f8-accd-a0de0f3753a0"
                    },
                    "time":"00s",
                    "value":"10"
                }
            }
        ],
        "description":"fix item_type for now"
    },
    "condition_id":"dbikelbi4",
    "rule_id":"asflasdfj",
    "rule_name":"demo_1",
    "rule_status":"enable",
    "trigger":{
        "config":[
            {
                "bitwise_operator":"None",
                "constraint":{
                    "comparation":"EQ",
                    "item":{
                        "item_global_id":"6d5a7af0-d96a-42ea-bdd9-87d05a01ea30",
                        "item_name":"motion",
                        "item_type":"Gauge",
                        "platform_id":"88507d0f-9e85-403e-b92b-10e9280d2491",
                        "thing_global_id":"7b9e1813-20bd-4414-b2b4-f2cad9ea3451"
                    },
                    "time":"00s",
                    "value":"1"
                },
                "trigger_config_id":1
            }
        ],
        "description":"fix item_type for now",
        "outputs":[
            {
                "description":"event created by trigger 84nf2jc4r",
                "event_id":"vwtqv1ea8",
                "event_source":"84nf2jc4r"}
        ],
        "trigger_id":"84nf2jc4r",
        "trigger_type":"item_has_given_state"
    },
    "trigger_id":"84nf2jc4r"
}

# Another way to present the relationship between things in trigger, condition

rule_1 = {
    "rule_id" : "rule_id_2",
    "rule_status" : "enable",
    "rule_name" : "rule_1",
    "trigger_bitwise":"AND",
    "trigger_type" : "item_has_given_state",
    "trigger_content":[
        {
            "id":"temperature",
            "field":"temperature",
            "type":"double",
            "input":"number",
            "operator":"less",
            "value":1111
        },
        {
            "id":"humidiy",
            "field":"humidiy",
            "type":"double",
            "input":"number",
            "operator":"less",
            "value":10.25
        }
    ],
    "action_type" : "call_cross_platform_api",
    "action":[
        {
            "item_global_id":"Den 1",
            "value":"On"
        },
        {
            "item_global_id":"Den 1",
            "value":"On"
        }
    ]

}





if __name__ == "__main__":

    cursor.execute("""CREATE DATABASE IF NOT EXISTS RuleAPI_DB""")
    cursor.execute("""USE RuleAPI_DB""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS RuleTable(
        rule_id VARCHAR(100) PRIMARY KEY,
        rule_name VARCHAR(100),
        rule_status VARCHAR(100),
        trigger_id VARCHAR(100),
        trigger_content VARCHAR(20000),
        condition_id VARCHAR(100),
        condition_content VARCHAR(20000),
        action_id VARCHAR(100),
        action_content VARCHAR(20000),
        insert_time VARCHAR(100))  """)




    cursor_engine.execute("""CREATE DATABASE IF NOT EXISTS RuleEngine_DB""")
    cursor_engine.execute("""USE RuleEngine_DB""")

    cursor_engine.execute("""CREATE TABLE IF NOT EXISTS RuleTable(
        rule_id VARCHAR(100) PRIMARY KEY,
        rule_name VARCHAR(100),
        rule_status VARCHAR(100),
        trigger_id VARCHAR(100),
        trigger_content VARCHAR(20000),
        condition_id VARCHAR(100),
        condition_content VARCHAR(20000),
        action_id VARCHAR(100),
        action_content VARCHAR(20000),
        insert_time VARCHAR(100))  """)




    cursor_trigger.execute("""CREATE DATABASE IF NOT EXISTS Trigger_DB""")
    cursor_trigger.execute("""USE Trigger_DB""")

    cursor_trigger.execute("""CREATE TABLE IF NOT EXISTS TriggerTable(
        rule_id VARCHAR(100) PRIMARY KEY,
        trigger_id VARCHAR(100),
        trigger_type VARCHAR(100),
        trigger_content VARCHAR(20000))  """)



    # print (json.dumps(rule))
    # save_data(rule)
    # delete_data(rule)


    try:
        data_list = load_data_from_db()
        # print ("data_list: ", data_list)
        app.run(host='0.0.0.0')
    except:
        db.commit()
        cursor.close()


