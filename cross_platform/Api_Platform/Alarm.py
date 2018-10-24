import datetime
import paho.mqtt.client as mqtt
import json
import ast

broker_cloud = "iot.eclipse.org"
client_mqtt_cloud_1 = mqtt.Client()
client_mqtt_cloud_1.connect(broker_cloud)

list_platforms = []
list_things = []
threshold_item_broken_up = 2  # new state is see as outlier and cause of item broken when now_state > 2 * mean_state + 1
threshold_item_broken_low = 0.5  # new state is see as outlier and cause of item broken when now_state < 0.5 * mean_state - 1
threshold_sensor_broken_up = 5  # new state is see as outlier and cause of sensor broken when now_state > 5 * mean_state + 1
threshold_sensor_broken_low = 0.1  # new state is see as outlier and cause of sensor broken when now_state < 0.1 * mean_state - 1
n_record = 10


#############################################################################################################
#
# Nhiem vu cua Alarm la theo doi du lieu duoc gui tu forwarder len collector va canh bao khi state bat thuong
# Du lieu gi forwarder gui len collector thi cung duoc gui len monitor (theo ly thuyet)


def get_list_platforms():
    print("Get list platforms from Registry")
    message = {
        'caller': 'alarm'
    }

    def hand_get_list(client, userdata, msg):
        global list_platforms
        list_platforms = ast.literal_eval(msg.payload.decode('utf-8'))
        print('Updated list of platform_id: ', str(list_platforms))
        alarm_things_states()

    client_mqtt_cloud_1.publish('registry/request/api_get_list_platforms', json.dumps(message))
    client_mqtt_cloud_1.subscribe('registry/response/alarm/api_get_list_platforms')
    client_mqtt_cloud_1.message_callback_add('registry/response/alarm/api_get_list_platforms', hand_get_list)


def handle_notification(client, userdata, msg):
    print('Have Notification')
    if json.loads(msg.payload.decode('utf-8'))['notification'] == 'Have Platform_id change':
        get_list_platforms()


def get_things(list_thing_global_id, n_record=10):
    print('Get all thing state in list thing')
    check_response = 0
    list_thing = []
    message = {
        'caller': 'alarm',
        'list_thing_global_id': list_thing_global_id,
        'n_record': n_record
    }

    def handle_api_get_things(client, userdata, msg):
        # nonlocal check_response, list_thing
        list_thing = ast.literal_eval(msg.payload.decode('utf-8'))
        check_response = 1
        client_mqtt_cloud_1.message_callback_remove('dbwriter/response/alarm/api_get_things')
        client_mqtt_cloud_1.unsubscribe('dbwriter/response/alarm/api_get_things')

    client_mqtt_cloud_1.subscribe('dbwriter/response/alarm/api_get_things')
    client_mqtt_cloud_1.message_callback_add('dbwriter/response/alarm/api_get_things', handle_api_get_things)
    client_mqtt_cloud_1.publish('dbwriter/request/api_get_things', json.dumps(message))
    while check_response == 0:
        client_mqtt_cloud_1.loop()
        continue
    return list_thing


def get_few_item_state_in_past(thing_global_id, item_global_id):
    prev_item_state = []
    # n_record = 10
    thing = get_things(thing_global_id, n_record)  # Lay du lieu 1 thing tu DBwritter
    items = thing['items']

    # Tim lay ra item co id=item_global_id trong danh sach cach items
    for item in items:
        if (item['item_global_id'] == item_global_id):
            item_state = item['item_state']
            prev_item_state.append(item_state)

    return prev_item_state


def alarm_outlier(platform_id, thing_global_id, item_global_id, now_item_state, message):
    file_path = './alarm_outlier.txt'
    file = open(file_path, 'a')
    file.write('Alarm at platform_id: ' + str(platform_id) + ' thing_global_id: ' + str(thing_global_id)
               + ' item_global_id: ' + str(item_global_id) + ' Time: ' + str(datetime.datetime.now())
               + ' message: ' + message)
    file.write("\n\n")
    print ('Alarm at platform_id: ' + str(platform_id) + ' thing_global_id: ' + str(thing_global_id)
           + ' item_global_id: ' + str(item_global_id) + ' Time: ' + str(datetime.datetime.now())
           + ' message: ' + message)
    print ("\n\n")
    file.close()


def get_things_from_registry():
    message = {
        'caller': "alarm"
    }

    def handle_get_things_from_registry():
        global list_things
        print ("Get list things from Registry")
        list_things = json.loads(message.payload.decode('utf-8'))

    print(list_things)

    # Yeu cau registry gui danh sach things + states cua things
    client_mqtt_cloud_1.publish('registry/request/api_get_things', json.dumps(message))
    client_mqtt_cloud_1.subscribe('registry/response/alarm/api_get_things')
    client_mqtt_cloud_1.message_callback_add('registry/response/alarm/api_get_things', handle_get_things_from_registry)


# Lay thing states cua tung platform 
def alarm_things_states():
    print("Collect the states of the devices")
    for platform_id in list_platforms:
        alarm_thing_state_by_platform_id(platform_id)
    # threading.Timer(time_collect, collect).start()


def alarm_thing_state_by_platform_id(platform_id):
    print('Collect data from platform_id: ', str(platform_id))

    def handle_monitor_by_platform_id(client, userdata, msg):
        prev_item_state = [0]
        print('Recived state from platform_id: ', platform_id)
        # print(msg.payload.decode('utf-8'))
        # print(ast.literal_eval(msg.payload.decode('utf-8')))
        list_things_by_platform_id = json.loads(msg.payload.decode('utf-8'))
        # print(list_things_by_platform_id)

        things = list_things_by_platform_id['things']  # Tat ca cac things

        # Lay ra state cua tat ca cac items co trong 1 thing	
        for i in range(len(things)):
            list_items_per_thing = things[i]['items']  # Tat ca items cua 1 thing
            thing_global_id = things[i]['thing_global_id']

            try:
                prev_item_state = get_few_item_state_in_past(thing_global_id,
                                                             item_global_id)  # lay ra mot so state cua item trong qua khu
            except:
                prev_item_state = [0]

            for j in range(len(list_items_per_thing)):
                item_type = list_items_per_thing[j]['item_type']
                item_global_id = list_items_per_thing[j]['item_global_id']
                now_item_state = list_items_per_thing[j]['item_state']

                if (item_type == "Number"):
                    mean_item_state = sum(prev_item_state) / len(prev_item_state)

                    if (now_item_state > threshold_item_broken_up * mean_item_state + 1 or
                            now_item_state < threshold_item_broken_low * mean_item_state - 1
                    ):
                        message = "Item broken"
                        alarm_outlier(platform_id, thing_global_id, item_global_id, now_item_state, message)
                    elif (now_item_state > threshold_sensor_broken_up * mean_item_state + 1 or
                          now_item_state < threshold_sensor_broken_low * mean_item_state - 1
                    ):
                        message = "Sensor broken"
                        alarm_outlier(platform_id, thing_global_id, item_global_id, now_item_state, message)
                    else:
                        prev_item_state = prev_item_state[1::] + [
                            float(now_item_state)]  # Update lai danh sach state cua item trong qua khu

    # Nhan du lieu do forwarder gui len

    client_mqtt_cloud_1.subscribe('{}/response/alarm/api_get_states'.format(platform_id))
    client_mqtt_cloud_1.message_callback_add('{}/response/alarm/api_get_states'.format(platform_id),
                                             handle_monitor_by_platform_id)


client_mqtt_cloud_1.subscribe('alarm/request/notification')
client_mqtt_cloud_1.message_callback_add('alarm/request/notification', handle_notification)

get_list_platforms()

client_mqtt_cloud_1.loop_forever()
