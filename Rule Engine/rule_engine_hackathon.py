from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
from kombu.utils.compat import nested
import json
import MySQLdb
from Rule_Engine_Base import Rule_Engine_Base
from Action import Action
from datetime import timedelta, datetime
import os
import time
from sinchsms import SinchSMS


class Rule_Engine_1(Rule_Engine_Base):
    def __init__(self, rule_engine_name, rule_engine_id,
                 description, input_topic, output_topic):

        Rule_Engine_Base.__init__(self, rule_engine_name, rule_engine_id,
                                  description, input_topic, output_topic)

        BROKER_CLOUD = "localhost"
        self.host_api_set_state = "http://192.168.43.30:5000/api/metric"
        self.producer_connection = Connection("192.168.43.30")
        self.consumer_connection = Connection("localhost")
        self.exchange = Exchange("IoT", type="direct")
        self.queue_get_states = Queue(name='event_generator.to.' + str(self.input_topic), exchange=self.exchange,
                                      routing_key='event_generator.to.' + str(self.input_topic))#, message_ttl=20)


        self.db = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root", db='rule')
        self.cursor = self.db.cursor()



    def mapping(self, trigger_id):
        print ("mapping ...")
        request = "select rule_content from RuleTable where trigger_id = '" + str(trigger_id) + "'"
        print (request)

        try:
            # Execute the SQL command
            self.cursor.execute(request)
            result = self.cursor.fetchall()
            rule_content = result[0]
            rule_content = json.loads(rule_content)
            action_content = rule_content["action"]


            return  action_content
        except:
            # Rollback in case there is any error
            print ("error mapping trigger_id")
            self.db.rollback()
            return None


    ############################################################
    ############### ACTION #####################################



    def call_to_action(self, action_id, action_content):
        print ("call to action")

        # Send alert to user
        send_sms()


        result = False
        action_type = "call_cross_platform_api"


        for action in action_content:

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



    def call_cross_platform_api(self, action_content):
        print("call_cross_platform_api ...")


        for action in action_content:
            print ("action: ", action)

            # thing_global_id = action['thing_global_id']
            item_global_id  = action['item_global_id']
            value           = action['value']

            message = {
                "SourceId"  : thing_global_id,
                "MetricId"  : item_global_id,
                "new_value" : value
            }

            request = "curl -H \"Content-type: application/json\" -X POST " + self.host_api_set_state + " -d " + "\'" + json.dumps(message) + "\'"

            # print (request)
            os.system(request)
            time.sleep(1)



    def send_sms():
        # number = '+841626118018'
        number = '+841626630681'
        message = "Alert!"
        client = SinchSMS("ce7ec38a-2ba2-47e8-aaf1-419a59809eca", "75jYmrdsG0aVAFUQu5AlIQ==")
        print("Sending '%s' to %s" % (message, number))
        response = client.send_message(number, message)
        message_id = response['messageId']
        response = client.check_status(message_id)

        while response['status'] != 'Successful':
            print(response['status'])
            time.sleep(1)
            response = client.check_status(message_id)
            print(response['status'])




    ###############################################################
    ###############################################################


    ###############################################################
    ############## RECEIVE EVENT ##################################

    def receive_event(self):
        def handle_notification(body, message):
            print ("Receive Event!")

            action_content = self.mapping(trigger_id)

            action_id = ''
            
            self.call_to_action(action_id, action_content)


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