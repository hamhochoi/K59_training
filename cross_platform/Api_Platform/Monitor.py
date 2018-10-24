import paho.mqtt.client as mqtt
import json
import datetime
import ast

broker_cloud = "iot.eclipse.org"
client_mqtt_cloud_1 = mqtt.Client()
client_mqtt_cloud_1.connect(broker_cloud)

client_mqtt_cloud_2 = mqtt.Client()  # client for synchronous
client_mqtt_cloud_2.connect(broker_cloud)

list_platforms = []
list_things = []
prev_item_state = []
threshold_outlier_high = 2  # a new state is a outlier if it's value > 2 * mean_past_state + 1
threshold_outlier_low = 0.5  # a new state is a outlier if it's value < 0.5 * mean_past_state - 1
n_record = 10
check_response = 0

######################################################################################
#
# Nhiem vu cua Monitor la theo doi du lieu duoc gui tu forwarder len collector
# Du lieu gi forwarder gui len collector thi cung duoc gui len monitor (theo ly thuyet)

def get_things(list_thing_global_id, n_record=10):
    print('Get all thing state in list thing')

    message = {
        'caller': 'monitor',
        'list_thing_global_id': list_thing_global_id,
        'n_record': n_record
    }

    def handle_api_get_things(client, userdata, msg):
        global check_response, list_things

        list_things = ast.literal_eval(msg.payload.decode('utf-8'))
        check_response = 1
        client_mqtt_cloud_2.message_callback_remove('dbwriter/response/monitor/api_get_things')
        client_mqtt_cloud_2.unsubscribe('dbwriter/response/monitor/api_get_things')

    client_mqtt_cloud_2.publish('dbwriter/request/api_get_things', json.dumps(message))
    client_mqtt_cloud_2.subscribe('dbwriter/response/monitor/api_get_things')
    client_mqtt_cloud_2.message_callback_add('dbwriter/response/monitor/api_get_things', handle_api_get_things)

    # global list_things

    # print ("list things: ", list_things)
    # print (check_response)
    while check_response == 0:
        client_mqtt_cloud_2.loop()
        continue

    return list_things


def get_few_item_state_in_past(thing_global_id, item_global_id):
    prev_item_state = []
    # n_record = 10
    things = get_things(thing_global_id, n_record)  # Lay du lieu 1 thing tu DBwritter
    # print ("things: ", things)
    items = things[0]['items']

    # print ("few items: ", items)

    # Tim lay ra item co id=item_global_id trong danh sach cach items
    for item in items:
        if (item['item_global_id'] == item_global_id):
            item_state = item['item_state']
            if (isinstance(item_state, float) or isinstance(item_state, int)):
                prev_item_state.append(float(item_state))


    print ("thing global id " + str(thing_global_id) +  "few item state: " + str(prev_item_state))

    return prev_item_state


def get_list_platforms():
    print("Get list platforms from Registry")
    message = {
        'caller': 'monitor'
    }

    def hand_get_list(client, userdata, msg):
        global list_platforms
        list_platforms = ast.literal_eval(msg.payload.decode('utf-8'))
        print('Updated list of platform_id: ', str(list_platforms))
        monitor_things_states()

    client_mqtt_cloud_1.publish('registry/request/api_get_list_platforms', json.dumps(message))
    client_mqtt_cloud_1.subscribe('registry/response/monitor/api_get_list_platforms')
    client_mqtt_cloud_1.message_callback_add('registry/response/monitor/api_get_list_platforms', hand_get_list)


def handle_notification(client, userdata, msg):
    print('Have Notification')
    if json.loads(msg.payload.decode('utf-8'))['notification'] == 'Have Platform_id change':
        get_list_platforms()


def alarm_outlier(platform_id, thing_global_id, item_global_id, item_name, now_item_state):
    file_path = './alarm_outlier.txt'
    file = open(file_path, 'a')
    file.write('Alarm at platform_id: ' + str(platform_id) + ' thing_global_id: ' + str(thing_global_id)
               + ' item_global_id: ' + str(item_global_id) + ' item name: ' + str(item_name)
               +' Time: ' + str(datetime.datetime.now()))

    file.write("\n\n")

    print ('Alarm at platform_id: ' + str(platform_id) + ' thing_global_id: ' + str(thing_global_id)
           + ' item_global_id: ' + str(item_global_id) + ' item name: ' + str(item_name)
           +' Time: ' + str(datetime.datetime.now()))

    print ("\n\n")

    file.close()


def get_things_from_registry():
    message = {
        'caller': "monitor"
    }

    def handle_get_things_from_registry():
        global list_things
        print ("Get list things from Registry")
        list_things = json.loads(message.payload.decode('utf-8'))

    print(list_things)

    # Yeu cau registry gui danh sach things + states cua things
    client_mqtt_cloud_1.publish('registry/request/api_get_things', json.dumps(message))
    client_mqtt_cloud_1.subscribe('registry/response/monitor/api_get_things')
    client_mqtt_cloud_1.message_callback_add('registry/response/monitor/api_get_things',
                                             handle_get_things_from_registry)


# Lay thing states cua tung platform 
def monitor_things_states():
    print("Collect the states of the devices")

    for platform_id in list_platforms:
        print (platform_id)
        monitor_thing_state_by_platform_id(platform_id)


# threading.Timer(time_collect, collect).start()


def monitor_thing_state_by_platform_id(platform_id):
    print('Collect data from platform_id: ', str(platform_id))

    def handle_monitor_by_platform_id(client, userdata, msg):
        print('Recived state from platform_id: ', platform_id)
        list_things_by_platform_id = json.loads(msg.payload.decode('utf-8'))
        # print(list_things_by_platform_id)
        things = list_things_by_platform_id['things']  # Tat ca cac things
        thing_global_id= []
        # Lay ra state cua tat ca cac items co trong 1 thing
        for i in range(len(things)):
            list_items_per_thing = things[i]['items']  # Tat ca items cua 1 thing
            thing_global_id.append(things[i]['thing_global_id'])

            for j in range(len(list_items_per_thing)):
                item_type = list_items_per_thing[j]['item_type']
                item_name = list_items_per_thing[j]['item_name']
                item_global_id = list_items_per_thing[j]['item_global_id']

                # prev_item_state = get_few_item_state_in_past(thing_global_id, item_global_id)

                try:
                    prev_item_state = get_few_item_state_in_past(thing_global_id, item_global_id)  # lay ra mot so state cua item trong qua khu
                    print ("prev item state: ", prev_item_state)
                except Exception as e:
                    print (e)
                    prev_item_state = [0]

                if (prev_item_state == []):
                    prev_item_state = [0]

                now_item_state = list_items_per_thing[j]['item_state']
                print ("Monitor now item state: ", now_item_state)

                print ("Item type: ", item_type)

                if (item_type == "Number" and now_item_state != 'None'):
                    now_item_state = float(now_item_state)
                    mean_item_state = sum(prev_item_state) / len(prev_item_state)

                    if ( now_item_state > threshold_outlier_high * mean_item_state + 1 or
                         now_item_state < threshold_outlier_low * mean_item_state - 1):
                        alarm_outlier(platform_id, thing_global_id, item_global_id, item_name, now_item_state)
                    else:
                        prev_item_state = prev_item_state[1::] + [float(now_item_state)]  # Update lai danh sach state cua item trong qua khu
                        print ("Not outlier")

    client_mqtt_cloud_1.subscribe('{}/response/monitor/api_get_states'.format(platform_id))
    client_mqtt_cloud_1.message_callback_add('{}/response/monitor/api_get_states'.format(platform_id), handle_monitor_by_platform_id)


client_mqtt_cloud_1.subscribe('monitor/request/notification')
client_mqtt_cloud_1.message_callback_add('monitor/request/notification', handle_notification)

def on_disconnect(client, userdata, rc):
    print("DISCONNECT")
client_mqtt_cloud_2.on_disconnect = on_disconnect
get_list_platforms()

client_mqtt_cloud_1.loop_forever()
