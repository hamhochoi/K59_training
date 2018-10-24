import paho.mqtt.client as mqtt
import json
from requests import get
import hashlib

platform_id = 'Quan'

host_homeAssistant = 'localhost'
port_homeAssistant = '8123'

pre_info = []

broker_address = "127.0.0.1"
clientMQTT = mqtt.Client("HomeAssistant_Driver")  # create new instance
clientMQTT.connect(broker_address)  # connect to broker


def get_states():
    print('Get state of all things')

    url = 'http://' + host_homeAssistant + ':' + port_homeAssistant + '/api/states'
    response = get(url).json()

    states = []

    for thing in response:
        # print(thing['entity_id'])
        thing_type = thing['entity_id'].split(".")[0]
        if (thing_type != 'group' and thing_type != 'automation'):
            # Trong HomeAssistant do quản lý chỉ đến mức Thing nên ta coi các item của 1 thing là chính nó.
            # VD: đèn là một thing và có item chính là bản thân cái đèn đó



            state = {
                'thing_type': thing_type,
                'thing_name': thing['attributes']['friendly_name'],
                'thing_global_id': platform_id + '/' + thing['entity_id'],
                'thing_local_id': thing['entity_id'],
                'location': get_location_of_thing(response, thing['entity_id']),
                'state': [
                    {
                        'item_type': thing_type,
                        'item_name': thing['attributes']['friendly_name'],
                        'item_global_id': platform_id + '/' + thing['entity_id'] + '/' + thing['entity_id'],
                        'item_local_id': thing['entity_id'],
                        'item_state': thing['state'],
                        'can_set_state': check_can_set_state(thing_type),

                    }
                ]
            }
            states.append(state)

    return states


def check_can_set_state(item_type):
    url = 'http://' + host_homeAssistant + ':' + port_homeAssistant + '/api/services'
    response = get(url).json()
    for service in response:
        if service['domain'] == item_type:
            return True
    return False


def get_location_of_thing(list_things, thing_id):
    for temp in list_things:
        if temp['entity_id'].split(".")[0] == 'group':
            for thing_in_group in temp['attributes']['entity_id']:
                if thing_in_group == thing_id:
                    return temp['entity_id'].split(".")[1]
    return None


def check_configuration_changes():
    global pre_info
    print('Check for changes')

    url = 'http://' + host_homeAssistant + ':' + port_homeAssistant + '/api/states'
    response = get(url).json()

    now_info = []

    for thing in response:
        # print(thing['entity_id'])
        thing_type = thing['entity_id'].split(".")[0]
        if (thing_type != 'group' and thing_type != 'automation'):
            # Trong HomeAssistant do quản lý chỉ đến mức Thing nên ta coi các item của 1 thing là chính nó.
            # VD: đèn là một thing và có item chính là bản thân cái đèn đó

            state = {
                'thing_type': thing_type,
                'thing_name': thing['attributes']['friendly_name'],
                'thing_global_id': platform_id + '/' + thing['entity_id'],
                'thing_local_id': thing['entity_id'],
                'location': get_location_of_thing(response, thing['entity_id']),
                'state': [
                    {
                        'item_type': thing_type,
                        'item_name': thing['attributes']['friendly_name'],
                        'item_global_id': platform_id + '/' + thing['entity_id'] + '/' + thing['entity_id'],
                        'item_local_id': thing['entity_id'],
                        'can_set_state': check_can_set_state(thing_type),

                    }
                ]
            }
            now_info.append(state)

    hash_now = hashlib.md5(str(now_info).encode())
    hash_pre = hashlib.md5(str(pre_info).encode())
    if hash_now.hexdigest() == hash_pre.hexdigest():
        return [True, 'No Change']
    else:
        pre_info = now_info
        return [False, now_info]


def set_state(thing_local_id, item_local_id, state):
    print('Set state of item')
    clientMQTT.publish("test2", "haha")


def init():
    print('Init and get platform_id from Registry')
    message = {
        'platform': 'Home Assistant',
        'host': host_homeAssistant,
        'port': port_homeAssistant,
    }

    clientMQTT.publish('registry/request/api_add_platform', json.dumps(message))
    topic_response = 'registry/response/' + host_homeAssistant + '/' + port_homeAssistant

    def handle_init(client, userdata, msg):
        print('Handle_init')
        global platform_id
        platform_id = json.loads(msg.payload.decode('utf-8'))['platform_id']
        print ('Platform_id recived: ', platform_id)
        clientMQTT.unsubscribe(topic_response)

        clientMQTT.subscribe(str(platform_id) + '/request/api_get_states')
        clientMQTT.message_callback_add(str(platform_id) + '/request/api_get_states', api_get_states)

        clientMQTT.subscribe(str(platform_id) + '/request/api_check_configuration_changes')
        clientMQTT.message_callback_add(str(platform_id) + '/request/api_check_configuration_changes', api_check_configuration_changes)

        clientMQTT.subscribe(str(platform_id) + '/request/api_set_state')
        clientMQTT.message_callback_add(str(platform_id) + '/request/api_set_state', api_set_state)

    clientMQTT.subscribe(topic_response)
    clientMQTT.message_callback_add(topic_response, handle_init)


def api_get_states(client, userdata, msg):
    caller = json.loads(msg.payload.decode('utf-8'))['caller']
    clientMQTT.publish('{}/response/{}/api_get_states'.format(platform_id, caller), str(get_states()))



def api_check_configuration_changes(client, userdata, msg):
    caller = json.loads(msg.payload.decode('utf-8'))['caller']
    print ('api_check_configuration_changes')
    clientMQTT.publish('{}/response/{}/api_check_configuration_changes'.format(platform_id,caller),str(check_configuration_changes()))


def api_set_state(client, userdata, msg):
    set_state()



# def handle_platform(client, userdata, msg):
#     print('Chac la Duoc')


# def on_message(client, userdata, msg):
#     print ('da co message')
#
# client.on_message = on_message
clientMQTT.subscribe("test")


# client.subscribe("test2")
#
def handle_test(client, userdata, msg):
    print('platform_id = ', platform_id)


#
# def handle_test2(client, userdata, msg):
#     print ('handle test2')
#
#
#
#
clientMQTT.message_callback_add("test", handle_test)
# client.message_callback_add("test2",handle_test2)
#
# init()
# set_state(1,2,2)
#
# get_states()

init()

# print('Ket qua check 1: {}'.format(check_configuration_changes()))
# print('Ket qua check 2: {}'.format(check_configuration_changes()))

clientMQTT.loop_forever()
