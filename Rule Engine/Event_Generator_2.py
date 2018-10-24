'''
    Use case:
        When any sensor send it's temperature value greater/smaller/... than a threshold
        then create an event
'''


from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
from kombu.utils.compat import nested
import json
import MySQLdb
from Event_Generator_Base import Event_Generator_Base
from Event import Event
from random import *
from datetime import timedelta, datetime



class event_generator_2(Event_Generator_Base):
    list_event_condition = []         # list_event_condition saved as a mysql table: |condition_id | condition_name | condition |

    def __init__(self, event_generator_name, event_generator_id,
                 description, event_dest_topic):
        Event_Generator_Base.__init__(self, event_generator_name, event_generator_id,
                                      description, event_dest_topic)

        BROKER_CLOUD = "localhost"
        self.producer_connection = Connection(BROKER_CLOUD)
        self.consumer_connection = Connection(BROKER_CLOUD)
        self.exchange = Exchange("IoT", type="direct")
        self.queue_get_states = Queue(name='data_source.to.' + str(self.event_generator_name), exchange=self.exchange,
                                      routing_key='data_source.to.' + str(self.event_generator_name))#, message_ttl=20)
        # self.queue_get_states = Queue(name='dbwriter.request.api_write_db', exchange=self.exchange,
        #                               routing_key='dbwriter.request.api_write_db')#, message_ttl=20)


        self.db = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root", db="Trigger_DB")
        self.cursor = self.db.cursor()


    def read_event_condition(self):
        print ("reading event condition ...")
        request = "Select trigger_id, trigger_type, trigger_content from TriggerTable"

        try:
            # Execute the SQL command
            self.cursor.execute(request)
            result = self.cursor.fetchall()
            self.list_event_condition = result
            # Commit your changes in the database
            self.db.commit()

            return self.list_event_condition
        except:
            # Rollback in case there is any error
            self.db.rollback()
            return None


    # def check_trigger_item_state_change(self, trigger_id, item_id):
    #     print ("checking trigger item state change ...")
    #     request = "Select item_state from ItemTable_2 where item_id='" + str(item_id) + "' order by time desc limit 2"
    #     print (request)
    #     try:
    #         # Execute the SQL command
    #         self.cursor.execute(request)
    #         result = self.cursor.fetchall()
    #         print (result)
    #         current_state = result[0]
    #         previous_state = result[1]
    #
    #         self.db.commit()
    #
    #         if (current_state != previous_state):
    #             return True
    #         else:
    #             return False
    #
    #     except:
    #         # Rollback in case there is any error
    #         self.db.rollback()
    #         print ("error checkTriggerItemStateChange")
    #         return None


    def check_trigger_item_state_update(self, trigger_content, item_id):
        pass


    def check_triger_fix_time_of_day(self, trigger_content, item_id):
        pass


    def check_trigger_item_has_given_state(self, trigger_content):
        print ("checking trigger item_has_given_state ...")
        # print (trigger_content)

        trigger_content = json.loads(trigger_content)
        print ("trigger_id: ", trigger_content['trigger_id'])

        config = trigger_content['config']
        # print ("config: ", config)

        pre_result = False
        total_result = False

        for sub_config in config:
            result = False
            timer = sub_config['constraint']['time']
            # print ("time: ", timer)
            trigger_item_id = sub_config['constraint']['item']['item_global_id']
            # print ("trigger_item_id: ", trigger_item_id)
            operator = sub_config['constraint']['comparation']
            # print ("operator: ", operator)
            value = sub_config['constraint']['value']
            # print ("value: ", value)
            bitwise_operator = sub_config['bitwise_operator']

            if (value.isdigit() == True):
                value = float(value)

            # print ("trigger_item_id: ", trigger_item_id)
            request = "select time from ItemTable_2 where item_id = '%s' order by time asc limit 1" % (trigger_item_id)
            last_insert_time = str(datetime.max)

            try:
                # Execute the SQL command
                self.cursor.execute(request)
                request_result = self.cursor.fetchall()
                last_insert_time = request_result[0][0]
                # Commit your changes in the database
                self.db.commit()
            except:
                # print ("error read time")
                result = False
                pre_result = result
                self.db.rollback()


            last_insert_time = datetime.strptime(last_insert_time, '%Y-%m-%d %H:%M:%S.%f')
            check_time = last_insert_time - timedelta(seconds=float(timer.split('s')[0]))

            request = "select item_state from ItemTable_2 where item_id = '%s' and time >= '%s'" % (trigger_item_id, check_time)

            try:
                # Execute the SQL command
                self.cursor.execute(request)
                request_result = self.cursor.fetchall()
                item_state_list = request_result[0]
                # print (item_state_list)
                # Commit your changes in the database
                self.db.commit()

                for item_state in item_state_list:
                    # print ("item_state: ", item_state)
                    result = True

                    if (item_state.isdigit() == True):
                        item_state = float(item_state)

                    if (operator == "GT"):
                        if (item_state <= value):
                            result = False
                            break
                    elif (operator == "GE"):
                        if (item_state < value):
                            result = False
                            break
                    elif (operator == "LT"):
                        if (item_state >= value):
                            result = False
                            break
                    elif (operator == "LE"):
                        if (item_state > value):
                            result = False
                            break
                    elif (operator == "EQ"):
                        if (item_state != value):
                            result = False
                            break
                    elif (operator == "NE"):
                        if (item_state == value):
                            result = False
                            break
                    else:
                        print ("operator is not valid")
                        result = False
                        break

                # print ("result: ", result)
                if (bitwise_operator.upper() == "NONE"):
                    total_result = result
                    pre_result = result
                elif (bitwise_operator.upper() == "AND"):
                    total_result = pre_result and result
                    pre_result = total_result
                elif (bitwise_operator.upper() == "OR"):
                    total_result = pre_result or result
                    pre_result = total_result
                else:
                    print ("bitwise operator is not pre-defined")

            except:
                # Rollback in case there is any error
                self.db.rollback()
                # print ("error check_trigger_item_has_given_state")
                # return None
                result = False
                pre_result = result

        print ("total result: ", total_result)

        return total_result


    def check_trigger_condition(self, trigger_id, trigger_type, trigger_content, item_id):
        print ("checking trigger condition ...")
        result = False
        if (trigger_type == "item_state_change"):
            # result = self.check_trigger_item_state_change(trigger_content, item_id)
            pass
        elif (trigger_type == "item_state_update"):
            result = self.check_trigger_item_state_update(trigger_content, item_id)
        elif (trigger_type == "item_receive_command"):
            pass
        elif (trigger_type == "fix_time_of_day"):
            result = self.check_triger_fix_time_of_day(trigger_content, item_id)
        elif (trigger_type == "item_has_given_state"):
            result = self.check_trigger_item_has_given_state(trigger_content)
        else:
            print ("trigger_type is not pre-defined")

        return result


    # def checkState(self, item_state, item_type):
    #     self.list_event_condition = self.readEventCondition()
    #
    #     if self.list_event_condition == None:
    #         raise ValueError("Cannot find any condition in EventConditionTable!")
    #
    #
    #     for condition in self.list_event_condition:
    #         condition_item_type = condition["event_type"]        # condition_item_type: temperature, humidity, ...
    #         condition_value     = condition["value"]            # condition_value : 30, 50.0, ....
    #         condition_type      = condition["condition_type"]   # condition_type : <, >, =, ...
    #         condition_id        = condition["condition_id"]
    #
    #         if (item_type == condition_item_type):
    #             if (condition_type == "="):
    #                 if (item_state == condition_value):
    #                     return True, condition_id
    #                 else:
    #                     return False, None
    #             elif (condition_type == "!="):
    #                 if (item_state != condition_value):
    #                     return True, condition_id
    #                 else:
    #                     return False, None
    #             elif (condition_type == ">"):
    #                 if (item_state > condition_value):
    #                     return True, condition_id
    #                 else:
    #                     return False, None
    #             elif (condition_type == ">="):
    #                 if (item_state >= condition_value):
    #                     return True, condition_id
    #                 else:
    #                     return False, None
    #             elif (condition_type == "<"):
    #                 if (item_state < condition_value):
    #                     return True, condition_id
    #                 else:
    #                     return False, None
    #             elif (condition_type == "<="):
    #                 if (item_state <= condition_value):
    #                     return True, condition_id
    #                 else:
    #                     return False, None
    #             else:
    #                 raise ValueError("condition_type is not valid!")
    #
    #     return False, None


    def create_event(self, trigger_id):
        print ("creating Event ...")

        request = "select trigger_content from TriggerTable where trigger_id = '%s'" % (trigger_id)
        # print (request)

        try:
            # Execute the SQL command
            self.cursor.execute(request)
            request_result = self.cursor.fetchall()
            trigger_content = request_result[0][0]
            trigger_content = json.loads(trigger_content)
            # print (trigger_content)
            output_field = trigger_content['outputs']
            # Commit your changes in the database
            self.db.commit()

            for output in output_field:
                event_id = output['event_id']
                event_name = output['event_name']
                event_source = output['event_source']
                description = output['description']

                message = {
                    'event_generator_id' : self.event_generator_id,
                    'event_id' : event_id,
                    'event_name' : event_name,
                    'event_source' : event_source,
                    'trigger_id' : trigger_id,
                    'description' : description,
                    'time' : str(datetime.now())
                }

                self.producer_connection.ensure_connection()
                with Producer(self.producer_connection) as producer:
                    producer.publish(
                        json.dumps(message),
                        exchange=self.exchange.name,
                        routing_key='event_generator.to.' + str(self.event_dest_topic),
                        retry=True
                    )
                print ("Send event to Rule Engine: " + 'event_generator.to.' + str(self.event_dest_topic))


        except:
            print ("error read trigger_content")


    def write_item_to_database(self, item_id, item_name, item_type, item_state, time):
        print ("writting item to database ...")
        request = """INSERT INTO ItemTable_2(item_id, item_name, item_type, item_state, time)
                    VALUES ("%s", "%s", "%s", "%s", "%s")""" \
                  % (item_id, item_name, item_type, item_state, time)

        print (request)
        try:
            # Execute the SQL command
            print (self.cursor.execute(request))
            result = self.cursor.fetchall()
            print ("write item %s to database: %s" % (item_id, result))
            self.db.commit()
            return  True

        except:
            # Rollback in case there is any error
            self.db.rollback()
            print ("error write item to database")
            return False


    def receive_states(self):
        def handle_notification(body, message):
            print ("Receive state!")
            item_id = json.loads(body)["item_id"]
            item_name  = json.loads(body)["item_name"]
            item_type = json.loads(body)["item_type"]
            item_state = json.loads(body)["item_state"]
            # time = json.loads(body)[""]
            time = datetime.now()
            time = str(time)

            # Write new item to the database
            write_result = self.write_item_to_database(item_id, item_name, item_type, item_state, time)

            #if write new item success to the database, consider the trigger with that item
            if (write_result == 1):
                list_event_condition = self.read_event_condition()
                for event_condition in list_event_condition:
                    trigger_id = event_condition[0]
                    trigger_type = event_condition[1]
                    trigger_content = event_condition[2]

                    # Check the item with each trigger condition
                    result = self.check_trigger_condition(trigger_id, trigger_type, trigger_content, item_id)

                    if (result == None):
                        return None

                    # If checkTriggerCondition success, create an event
                    if (result == True):
                        # event_source = item_id
                        # event_name = str(item_name) + "_" + str(datetime.now())
                        # event_id   = randint(1, 1000000)
                        # my_event = Event(event_name, event_id, event_source)
                        self.create_event(trigger_id)

            # End handle_notification

        try:
            self.consumer_connection.ensure_connection(max_retries=1)
            with nested(Consumer(self.consumer_connection, queues=self.queue_get_states,
                                 callbacks=[handle_notification], no_ack=True)
                        ):
                while True:
                    self.consumer_connection.drain_events()
        except (ConnectionRefusedError, exceptions.OperationalError):
            print('Connection lost')
        except self.consumer_connection.connection_errors:
            print('Connection error')
        except:
            print ("some error")


    def run(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS ItemTable_2(
                        item_id VARCHAR(50),
                        item_name VARCHAR(50),
                        item_type VARCHAR(50),
                        item_state VARCHAR(50), 
                        time VARCHAR(50),
                        PRIMARY KEY (item_id, time))""")

        while 1:
            try:
                self.receive_states()
            except (ConnectionRefusedError, exceptions.OperationalError):
                print('Connection lost')
            except self.consumer_connection.connection_errors:
                print('Connection error')


event_generator_2 = event_generator_2(event_generator_name="event_generator_2",
                                      event_generator_id="1", description="",
                                      event_dest_topic="rule_engine_1")
print (event_generator_2.event_generator_id)
event_generator_2.run()
