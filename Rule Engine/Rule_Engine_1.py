from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
from kombu.utils.compat import nested
import json
import MySQLdb
from Rule_Engine_Base import Rule_Engine_Base
from Action import Action
from datetime import timedelta, datetime
import os
import time

class Rule_Engine_1(Rule_Engine_Base):
    def __init__(self, rule_engine_name, rule_engine_id,
                  description, input_topic, output_topic):

        Rule_Engine_Base.__init__(self, rule_engine_name, rule_engine_id,
                                  description, input_topic, output_topic)

        BROKER_CLOUD = "localhost"
        self.host_api_set_state = "http://25.14.206.65:5000/api/metric"
        self.producer_connection = Connection("25.14.206.65")
        self.consumer_connection = Connection("25.14.206.65")
        self.exchange = Exchange("IoT", type="direct")
        self.queue_get_states = Queue(name='event_generator.to.' + str(self.input_topic), exchange=self.exchange,
                                      routing_key='event_generator.to.' + str(self.input_topic))#, message_ttl=20)

        self.db = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root", db='RuleEngine_DB')
        self.cursor = self.db.cursor()

        self.db_item = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root", db='Trigger_DB')
        self.cursor_item = self.db_item.cursor()


    def mapping(self, trigger_id):
        print ("mapping ...")
        request = "select condition_id, condition_content, action_id, action_content from RuleTable where trigger_id = '" + str(trigger_id) + "'"
        print (request)

        try:
            # Execute the SQL command
            self.cursor.execute(request)
            result = self.cursor.fetchall()
            condition_id, condition_content, action_id, action_content = result[0]

            condition_content = json.loads(condition_content)
            condition_type = condition_content['condition_type']
            action_content = json.loads(action_content)


            return condition_id, condition_type, condition_content, action_id, action_content
        except:
            # Rollback in case there is any error
            print ("error mapping trigger_id")
            self.db.rollback()
            return None


####################################################################
#################### CONDITION #####################################


    def check_condition(self, condition_id, condition_type, condition_content):
        print ("checking condition ...")
        print (condition_type)
        result = False
        if (condition_type == "item_has_given_state"):
            result = self.check_condition_item_has_given_state(condition_id, condition_type, condition_content)
        elif (condition_type == "given_script_is_true"):
            result = self.check_condition_given_script_is_true(condition_id, condition_type, condition_content)
        elif (condition_type == "certain_day_of_week"):
            result = self.check_condition_certain_day_of_week(condition_id, condition_type, condition_content)
        else:
            print ("condition_type is not pre-defined!")


        return result


    def check_condition_item_has_given_state(self, condition_id, condition_type, condition_content):
        print ("checking condition item_has_given_state ...")
        print (condition_id)

        condition_content = json.dumps(condition_content)
        condition_content = json.loads(condition_content)
        config = condition_content['config']

        pre_result = False
        total_result = False

        for sub_config in config:
            result = False
            condition_item_id = sub_config['constraint']['item']['item_global_id']
            print ("condition_item_id: ", condition_item_id)
            timer = sub_config['constraint']['time']
            operator = sub_config['constraint']['comparation']
            value = sub_config['constraint']['value']

            if (value.isdigit() == True):
                value = float(value)

            bitwise_operator = sub_config['bitwise_operator']

            request = "select time from ItemTable where item_id = '%s' order by time asc limit 1" % (condition_item_id)
            print (request)

            last_insert_time = str(datetime.max)

            try:
                # Execute the SQL command
                self.cursor_item.execute(request)
                request_result = self.cursor_item.fetchall()
                print ("request result: ", request_result)
                last_insert_time = request_result[0][0]
                # Commit your changes in the database
                self.db_item.commit()
            except:
                print ("error read time")
                result = False
                pre_result = result
                self.db_item.rollback()


            last_insert_time = datetime.strptime(last_insert_time, '%Y-%m-%d %H:%M:%S.%f')
            check_time = last_insert_time - timedelta(seconds=float(timer.split('s')[0]))

            request = "select item_state from ItemTable where item_id = '%s' and time >= '%s'" % (condition_item_id, check_time)
            # print (request)

            try:
                # Execute the SQL command
                self.cursor_item.execute(request)
                result = self.cursor_item.fetchall()
                item_state_list = result[0]
                # Commit your changes in the database
                self.db_item.commit()

                for item_state in item_state_list:
                    if (item_state.isdigit() == True):
                        item_state = float(item_state)
                    # elif (item_state == "on"):
                    #     item_state = 1
                    # elif (item_state == "off"):
                    #     item_state = 0

                    result = True

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

                print ("result: ", result)

                if (bitwise_operator.upper() == "NONE"):
                    pre_result = result
                    total_result = result
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
                result = False
                pre_result = result


        print ("total result: ", total_result)

        return total_result


    def check_condition_given_script_is_true(self, condition_id, condition_type, condition_content):
        pass


    def check_condition_certain_day_of_week(self, condition_id, condition_type, condition_content):
        pass


    # def call_to_action(self, action_type, action_id, action_content):
    #     message = {
    #         'rule_engine_name' : self.rule_engine_name,
    #         'rule_engine_id' : self.rule_engine_id,
    #         'action_id' : action_id,
    #         'action_type' : action_type,
    #         "action_content" : action_content
    #     }
    #
    #     self.producer_connection.ensure_connection()
    #     with Producer(self.producer_connection) as producer:
    #         producer.publish(
    #             json.dumps(message),
    #             exchange=self.exchange.name,
    #             routing_key='event_generator.to.' + str(self.output_topic),
    #             retry=True
    #         )
    #     print ("Send event to Actor: ", self.output_topic)



############################################################
############### ACTION #####################################


    def call_to_action(self, action_id, action_content):
        print ("call to action")
        print (action_content['action_id'])
        result = False

        for action in action_content['action']:
            action_type = action['action_type']

            if (action_type == "send_a_command"):
                result = self.send_a_command(action_content)
            elif (action_type == "enable_or_disable_rule"):
                result = self.enable_or_disable_rule(action_content)
            elif (action_type == "run_rule"):
                result = self.run_rule(action_content)
            elif (action_type == "exec_given_script"):
                result = self.exec_given_script(action_content)
            elif (action_type == "write_log"):
                result = self.write_log(action_content)
            elif (action_type == "call_cross_platform_api" or action_type == "update"):
                result = self.call_cross_platform_api(action_content)
            else:
                print ("action_type is not pre-defined")
                result = False      # error

            if (result == False):
                print ("Error execute action")
                break

        return result


    def send_a_command(self, action_content):
        pass

    def enable_or_disable_rule(self, action_content):
        pass


    def run_rule(self, action_content):
        pass


    def exec_given_script(self, action_content):
        pass


    def write_log(self, action_content):
        print ("writing log ...")

        action_content = json.dumps(action_content)
        action_content = json.loads(action_content)
        print (action_content)

        for action in action_content["action"]:
            config = action["config"]
            print (config)
            file_name = config["file_name"]
            file_format = config["format"]


            f = open(file_name + "" + file_format, "a")
            f.write(str(action_content))
            f.write("\n")


    def call_cross_platform_api(self, action_content):
        print("call_cross_platform_api ...")
        # print (action_content["action"][1])

        for action in action_content['action']:
            print ("action: ", action)
            thing_global_id = action['config']['item']['thing_global_id']
            item_global_id  = action['config']['item']['item_global_id']
            value           = action['config']['value']

            message = {
                "SourceId"  : thing_global_id,
                "MetricId"  : item_global_id,
                "new_value" : value
            }

            request = "curl -H \"Content-type: application/json\" -X POST " + self.host_api_set_state + " -d " + "\'" + json.dumps(message) + "\'"

            # print (request)
            os.system(request)
            time.sleep(3)

        # time.sleep(1)


###############################################################
###############################################################


###############################################################
############## RECEIVE EVENT ##################################

    def receive_event(self):
        def handle_notification(body, message):
            print ("Receive Event!")

            # print (json.loads(body))

            # event_name = json.loads(body)["event_name"]
            event_id  = json.loads(body)["event_id"]
            event_source = json.loads(body)["event_source"]
            trigger_id = json.loads(body)["trigger_id"]
            # event_generator_id = json.loads(body)["event_generator_id"]
            time = json.loads(body)["time"]

            # mapping trigger_id to condition_id and action_id
            condition_id, condition_type, condition_content, action_id, action_content = self.mapping(trigger_id)

            # Check if condition has condition_id is true
            is_condition_satisfice = self.check_condition(condition_id, condition_type, condition_content)

            print ("check condition result: ", is_condition_satisfice)

            if (is_condition_satisfice == True):
                    # Execute an action
                    self.call_to_action(action_id, action_content)
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
        while 1:
            try:
                self.receive_event()

            except (ConnectionRefusedError, exceptions.OperationalError):
                print('Connection lost')
            except self.consumer_connection.connection_errors:
                print('Connection error')
            except:
                print ("some error")




###########################################################
####################### MAIN ##############################

rule_engine_1 = Rule_Engine_1("rule_engine_1", "rule_engine_id_1", "", "rule_engine_1", "")
print (rule_engine_1.rule_engine_name)
rule_engine_1.run()