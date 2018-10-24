import paho.mqtt.client as mqtt
import json
import configparser
import threading
#from Performance_Monitoring.message_monitor import MessageMonitor
import logging
import time
from ast import literal_eval
import os
import copy
import requests


class Driver:

    def __init__(self, config_path, time_push):
            self.now_info = []
            self.now_metric_domain = {}
            self.list_mapping_id = {}
            self.info_receive_from_registry = []
            config = configparser.ConfigParser()
            config.read(config_path)
            self.time_push = int(time_push)
            self.host = config['PLATFORM']['host']
            self.port = config['PLATFORM']['port']
            self.platform_name = config['PLATFORM']['platform_name']
            self.platform_type = config['PLATFORM']['platform_type']
            self.platform_id = None

            my_path = os.path.dirname(__file__)
            filename = os.path.join(my_path, '../../Semantic_Analysis/metric_domain.json')

            with open(filename) as json_file:
                self.metric_domain_file = json.load(json_file)

            broker_fog = config['BROKER']['host']
            self.clientMQTT = mqtt.Client()
            self.clientMQTT.connect(broker_fog)
            self.clientMQTT.on_connect = self.on_connect
            self.clientMQTT.on_disconnect = self.on_disconnect

            registration = {
                "header": {},
                "body": {
                    'PlatformHost': self.host,
                    'PlatformPort': self.port,
                    'PlatformType': self.platform_type,
                    'PlatformName': self.platform_name
                }
            }

            if 'platform_id' in config['PLATFORM']:
                logging.info("Platform have a platform_id")
                registration["header"]["registered"] = True
                registration["header"]["PlatformId"] = config['PLATFORM']['platform_id']
            else:
                logging.info("Platform don't have a platform_id")
                registration["header"]["registered"] = False

            topic_response = 'registry/response/' + self.host + "/" + self.port

            check_response = 0

            def handle_init(client, userdata, msg):

                nonlocal check_response
                logging.debug("Response from Registry "+str(json.loads(msg.payload.decode('utf-8'))))
                header = json.loads(msg.payload.decode('utf-8'))['header']
                body = json.loads(msg.payload.decode('utf-8'))['body']
                self.platform_id = header['PlatformId']
                if 'platform_id' not in config['PLATFORM']:
                    with open(config_path, 'w') as file:
                        config['PLATFORM']['platform_id'] = self.platform_id
                        config.write(file)

                logging.info('Platform_id: ' + self.platform_id)
                self.handle_info_from_registry(info_receive_from_registry=body['sources'], init_time=True)
                self.clientMQTT.unsubscribe(topic_response)
                check_response = 1

            self.clientMQTT.subscribe(topic_response)
            self.clientMQTT.message_callback_add(topic_response, handle_init)

            logging.debug('Registration: ' + str(registration))
            self.clientMQTT.publish('registry/request/api_add_platform', json.dumps(registration))
            while self.platform_id is None or check_response == 0:
                logging.debug("Wait for Registry response")
                self.clientMQTT.loop()

            self.clientMQTT.subscribe(str(self.platform_id) + '/request/api_get_states')
            self.clientMQTT.message_callback_add(str(self.platform_id) + '/request/api_get_states', self.api_get_states)

            self.clientMQTT.subscribe(str(self.platform_id) + '/request/api_update_now_configuration')
            self.clientMQTT.message_callback_add(str(self.platform_id) + '/request/api_update_now_configuration', self.api_update_now_configuration)

            self.clientMQTT.subscribe(str(self.platform_id) + '/request/api_check_platform_active')
            self.clientMQTT.message_callback_add(str(self.platform_id) + '/request/api_check_platform_active', self.api_check_platform_active)

            self.clientMQTT.subscribe(str(self.platform_id) + '/request/api_check_configuration_changes')
            self.clientMQTT.message_callback_add(str(self.platform_id) + '/request/api_check_configuration_changes', self.api_check_configuration_changes)

            self.clientMQTT.subscribe(str(self.platform_id) + '/request/api_set_state', qos=2)
            self.clientMQTT.message_callback_add(str(self.platform_id) + '/request/api_set_state', self.api_set_state)

            #self.message_monitor = MessageMonitor('0.0.0.0', 8086)

    def handle_info_from_registry(self, info_receive_from_registry, init_time=False):
        # "local_id":"global_id"
        new_info = []
        print('info_receive_from_registry: {}'.format(info_receive_from_registry))
        for source in info_receive_from_registry:
            temp_source = {}
            self.list_mapping_id[source['information']['LocalId']] = source['information']['SourceId']
            temp_source['information'] = copy.deepcopy(source['information'])
            del temp_source['information']['SourceId']
            if "SourceStatus" in temp_source['information']:
                # print("Co Nhe")
                del temp_source['information']['SourceStatus']
            metrics = []
            for metric in source['metrics']:
                self.list_mapping_id[metric['MetricLocalId']] = metric['MetricId']
                self.now_metric_domain[metric['MetricLocalId']] = metric['MetricDomain']
                temp_metric = copy.deepcopy(metric)
                del temp_metric['MetricId']
                if "MetricStatus" in metric:
                    # print("Co Metric Status")
                    del temp_metric["MetricStatus"]
                metrics.append(temp_metric)

            temp_source['metrics'] = metrics
            new_info.append(temp_source)
        if init_time is False:
            self.now_info = new_info
        else:
            self.now_info = []

    def mapping_id(self, info, ids, is_config=True):
        if is_config is True:
            for source in info:
                if source['information']['LocalId'] in ids:
                    source['information']['SourceId'] = ids[source['information']['LocalId']]

                for metric in source['metrics']:
                    if metric['MetricLocalId'] in ids:
                        metric['MetricId'] = ids[metric['MetricLocalId']]
        else:
            for metric in info:
                if metric['MetricLocalId'] in ids:
                    metric['MetricId'] = ids[metric['MetricLocalId']]

    def api_get_states(self, client, userdata, msg):
        message = json.loads(msg.payload.decode('utf-8'))
        states = self.get_states()

        message_response = {
            "header": message['header'],
            "body": {}
        }

        self.mapping_id(states, copy.deepcopy(self.list_mapping_id), is_config=False)
        message_response['body']['states'] = states
        #message_response['message_monitor'] = self.message_monitor.monitor(body, 'driver', 'api_get_states')
        self.clientMQTT.publish('driver/response/filter/api_get_states', json.dumps(message_response))

    def api_check_configuration_changes(self, client, userdata, msg):
        print('api_check_configuration_changes')
        message = json.loads(msg.payload.decode('utf-8'))
        message_response = {
            "header": message['header'],
            "body": {}
        }

        config = self.check_configuration_changes()
        self.mapping_id(config['new_info'], copy.deepcopy(self.list_mapping_id))
        message_response['body'] = config
        #message_response['message_monitor'] = self.message_monitor.monitor(body, 'driver', 'api_check_configuration_changes')
        self.clientMQTT.publish('driver/response/forwarder/api_check_configuration_changes', json.dumps(message_response))

    def api_update_now_configuration(self, client, userdata, msg):
        message = json.loads(msg.payload.decode('utf-8'))
        print("API update: {}".format(message))
        self.handle_info_from_registry(info_receive_from_registry=message['body']['active_sources'])

    def api_set_state(self, client, userdata, msg):
        print("API SET STATE")
        message = json.loads(msg.payload.decode('utf-8'))
        body = message['body']
        metric_local_id = body['metric']['MetricLocalId']
        metric_name = body['metric']['MetricName']
        metric_domain = body['metric']['MetricDomain']
        new_value = body['new_value']
        self.set_state(metric_local_id, metric_name, metric_domain, new_value)
        #self.message_monitor.end_message(message, 'driver', 'api_set_state')

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logging.WARNING("Disconnected to BROKER_FOG.")

    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected to BROKER_FOG.")
        if self.platform_id is not None:
            self.clientMQTT.subscribe(str(self.platform_id) + '/request/api_get_states')
            self.clientMQTT.message_callback_add(str(self.platform_id) + '/request/api_get_states', self.api_get_states)

            self.clientMQTT.subscribe(str(self.platform_id) + '/request/api_check_configuration_changes')
            self.clientMQTT.message_callback_add(str(self.platform_id) + '/request/api_check_configuration_changes', self.api_check_configuration_changes)

            self.clientMQTT.subscribe(str(self.platform_id) + '/request/api_update_now_configuration')
            self.clientMQTT.message_callback_add(str(self.platform_id) + '/request/api_update_now_configuration',self.api_update_now_configuration)

            self.clientMQTT.subscribe(str(self.platform_id) + '/request/api_check_platform_active')
            self.clientMQTT.message_callback_add(str(self.platform_id) + '/request/api_check_platform_active', self.api_check_platform_active)

            self.clientMQTT.subscribe(str(self.platform_id) + '/request/api_set_state', qos=2)
            self.clientMQTT.message_callback_add(str(self.platform_id) + '/request/api_set_state', self.api_set_state)

    def run(self):
        self.push_configuration_changes()
        #
        # check_config = threading.Thread(target=self.test)
        # check_config.setDaemon(True)
        # check_config.start()
        self.push_get_state()
        self.clientMQTT.loop_forever()

    # def test(self):
    #     while 1:
    #         self.push_get_state()

    def push_configuration_changes(self):
        message = {
            "header":{},
            "body": {}
        }
        config = self.check_configuration_changes()
        self.mapping_id(config['new_info'], copy.deepcopy(self.list_mapping_id))
        message['body'] = config
        if message['body']['is_change'] is True:
            message['header']['reply_to'] = 'driver.response.registry.api_check_configuration_changes'
            message['header']['PlatformId'] = self.platform_id
            message['header']['mode'] = "PUSH"
            print("PUSHHHHHHHHH: {}".format(message))

            self.clientMQTT.publish('driver/response/forwarder/api_check_configuration_changes', json.dumps(message))
        threading.Timer(self.time_push, self.push_configuration_changes).start()

    def push_get_state(self):
        states = self.get_states()

        message = {
            "header":{},
            "body": {}
        }

        message['header']['reply_to'] = 'driver.response.collector.api_get_states'
        message['header']['PlatformId'] = self.platform_id
        message['header']['mode'] = "PUSH"
        print("PUSH STATE no MetricID: {}".format(states))
        self.mapping_id(states, copy.deepcopy(self.list_mapping_id), is_config=False)
        message['body']['states'] = states

        #message['message_monitor'] = self.message_monitor.monitor({}, 'driver', 'push_get_state')
        self.clientMQTT.publish('driver/response/filter/api_get_states', json.dumps(message))
        threading.Timer(self.time_push, self.push_get_state).start()

    def get_states(self):
        pass

    def set_state(self, metric_local_id, metric_name, metric_domain, new_value):
        pass

    def check_configuration_changes(self):
        pass

    def create_registration(self, driver_id, driver_type, driver_host):
        logging.info("create_registration")

        registration = {
            "header": {},
            "body": {
                'driver_host': driver_host,
                'driver_type': driver_type
            }
        }

        if driver_id is None:
            logging.info("Driver don't have a driver_id")
            registration["header"]["registered"] = False
        else:
            logging.info("Driver have a driver_id")
            registration["header"]["registered"] = True
            registration["header"]["DriverId"] = driver_id

        return registration

    def api_check_platform_active(self, client, userdata, msg):
        print('api_check_platform_active')
        body = json.loads(msg.payload.decode('utf-8'))
        message_response = {
            "header": body['header'],
            "body": {}
        }

        try:
            response = requests.get('http://' + self.host + ':' + self.port)
            if response.status_code == 200:
                message_response['body']['active'] = True

            else:
                return
        except:
            return

        self.clientMQTT.publish('driver/response/forwarder/api_check_platform_active', json.dumps(message_response))

    def detect_metric_domain(self, sentence, value):
        # value must casted to the corresponding type before pass to function
        max_score = 0
        domain = "unknown"
        sentence = sentence.lower()

        for key in self.metric_domain_file.keys():
            score_domain = 0
            # Count words
            for word in sentence.split(" "):
                for word_domain in self.metric_domain_file[key]["words"]:
                    if word_domain in word:
                        score_domain = score_domain + 1

            # Check if value in value domain
            value_domain = self.metric_domain_file[key]["value"]
            if isinstance(value_domain, list):
                if value in value_domain:
                    score_domain = score_domain + 1
                if 'mapping' in self.metric_domain_file[key]:
                    if str(value) in self.metric_domain_file[key]['mapping']:
                        score_domain = score_domain + 1

            elif value_domain == "number":
                if isinstance(value, int) or isinstance(value, float):
                    score_domain = score_domain + 1

            if score_domain > max_score:
                max_score = score_domain
                domain = key
            print("sentence {} domain {} score {}".format(sentence, key, score_domain))
        return domain

    def mapping_data_value(self, domain_name, value, datatype):
        print("value : {}, datatype: {}".format(value, datatype))
        value_domain = self.metric_domain_file[domain_name]["value"]
        if isinstance(value_domain, list):
            if value in value_domain:
                return [value, datatype]
            elif 'mapping' in self.metric_domain_file[domain_name]:
                if value in self.metric_domain_file[domain_name]['mapping']:
                    value_mapped = self.metric_domain_file[domain_name]['mapping'][value]
                    return [value_mapped, self.detect_data_type(value_mapped)[0]]
            else:
                return "ERROR typedata"

        elif value_domain == "number":
            if datatype == "float" or datatype == "int":
                return [value, datatype]
            else:
                return "ERROR typedata"


    @staticmethod
    def detect_data_type(value):

        try:
            number = literal_eval(value)
        except ValueError:
            return ["string", value]

        if isinstance(number, int) or (isinstance(number, float) and number.is_integer()):
            return ["int", int(number)]
        elif isinstance(number, float):
            return ["float", float(number)]
        else:
            return ["unknown", value]

    def ordered(self, obj):
        if isinstance(obj, dict):
            return sorted((k, self.ordered(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(self.ordered(x) for x in obj)
        else:
            return obj