from kombu import Producer, Connection, Consumer, exceptions, Exchange, Queue, uuid
from kombu.utils.compat import nested
import json
import datetime
import MySQLdb
from Actor_Base import Actor_Base

class actor_2(Actor_Base):
    def __init__(self, actor_name, actor_id):
        Actor_Base.__init__(self, actor_name, actor_id)

        BROKER_CLOUD = "localhost"
        self.producer_connection = Connection(BROKER_CLOUD)
        self.consumer_connection = Connection(BROKER_CLOUD)
        self.exchange = Exchange("IoT", type="direct")
        self.queue_get_states = Queue(name='event_generator.to.' + str(self.actor_id), exchange=self.exchange,
                                      routing_key='event_generator.to.' + str(self.actor_id))#, message_ttl=20)

        self.db = MySQLdb.connect(host="0.0.0.0", user="root", passwd="root")
        self.cursor = self.db.cursor()



    def execute(self, action_type, action_id):
        pass


    def receiveCallToAction(self):
        def handle_notification(body, message):
            print ("Receive Event!")
            action_id = json.loads(body)["action_id"]
            action_name = json.loads(body)["action_name"]
            action_type = json.loads(body)["action_type"]

            self.execute(action_type, action_id)
            print ("Executed action: ", action_id)
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