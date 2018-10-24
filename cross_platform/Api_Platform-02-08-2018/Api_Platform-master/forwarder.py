
import paho.mqtt.client as mqtt
import json
import ast
# The callback for when the client receives a CONNACK response from the server.)

broker_cloud = 'iot.eclipse.org'
broker_fog = 'broker.hivemq.com'


#create Client
client_fog = mqtt.Client()
client_fog.connect(broker_fog)

client_cloud = mqtt.Client()
client_cloud.connect(broker_cloud)


def on_messageRegistry(client, userdata, msg):
    print("Forward to Registry api_check_configurtion_changes")
    data = ast.literal_eval(msg.payload.decode('utf-8'))
    platform_id = data[2]
    topic_name = platform_id + "/response/registry/api_check_configuration_changes"
    client_cloud.publish(topic_name, str(data))


#On message for sub on /driver/response/filter/..

def on_messageFilter(client, userdata, msg):
    print('Forward to Collector api_get_states')
    data = json.loads(msg.payload.decode("utf-8"))
    platform_id = data['platform_id']
    data = json.dumps(data)
    topic_name = platform_id + "/response/collector/api_get_states"
    client_cloud.publish(topic_name, data)


#On message for registry/request/api-add-platform
def on_messageAPIAddPlatform(client, userdata, msg):
    print('Forward to Registry api_add_platform')
    data = msg.payload.decode('utf-8')
    data = json.loads(data)
    data = json.dumps(data)
    client_cloud.publish("registry/request/api_add_platform", data)

client_fog.message_callback_add("driver/response/forwarder/api_check_configuration_changes", on_messageRegistry)
client_fog.message_callback_add("filter/response/forwarder/api_get_states", on_messageFilter)
client_fog.message_callback_add("registry/request/api_add_platform", on_messageAPIAddPlatform)


client_fog.subscribe("driver/response/forwarder/api_check_configuration_changes")
client_fog.subscribe("filter/response/forwarder/api_get_states")
client_fog.subscribe("registry/request/api_add_platform")

client_fog.loop_start()
client_cloud.loop_start()

while True:
    continue
