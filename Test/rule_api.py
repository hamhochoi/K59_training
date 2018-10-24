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
    rule_content   = data

    rule_status = "enable"
    insert_time = time.time()
    result = None
    # print (rule_condition)

    sql = """INSERT INTO Rule(rule_id,
         rule_status, rule_content, insert_time)
         VALUES ("%s", '%s', "%s", %f)""" % (rule_id, rule_status, rule_content, insert_time)

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
        query_statement = 'SELECT rule_id, rule_status, rule_content FROM Rule WHERE rule_status = "enable" ORDER BY insert_time DESC'
    else:
        query_statement = 'SELECT rule_id, rule_status, rule_content FROM Rule WHERE rule_status = "enable" ORDER BY insert_time DESC LIMIT' + str(n_record)

    # cursor.execute(query_statement)
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()

    try:
        # Execute the SQL command
        cursor.execute(query_statement)
        # Fetch all the rows in a list of lists.
        results = cursor.fetchall()
        print ("2")
        print (results[0])


        for row in results:
            print ("row: ", row)
            print ("\n\n\n\n")
            rule = {
                'rule_id'           : row[0],
                'rule_status'       : row[1],
                'rule_content'      : json.loads(json.dumps(row[2]))
            }


            list_rule.append(rule)
            # print (rule['rule_condition'])

        print ("list rule: ", list_rule)

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

    rule_content   = json.dumps(data)

    sql = """UPDATE Rule SET rule_status = "%s", 
             rule_content = "%s" WHERE rule_id = "%s" """ \
             % (rule_status, rule_content, rule_id)

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

    cursor.execute("""CREATE DATABASE IF NOT EXISTS rule""")
    cursor.execute("""USE rule""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Rule(
        rule_id VARCHAR(100) PRIMARY KEY,
        rule_status VARCHAR(100),
        rule_content VARCHAR(10000),
        -- action_content VARCHAR(10000),
        insert_time VARCHAR(100))  """)

    # print (json.dumps(rule))
    save_data(rule_1)
    # delete_data(rule_1)


    try:
        data_list = load_data_from_db()
        # print ("data_list: ", data_list)
        app.run(host='0.0.0.0')
    except:
        db.commit()
        cursor.close()


