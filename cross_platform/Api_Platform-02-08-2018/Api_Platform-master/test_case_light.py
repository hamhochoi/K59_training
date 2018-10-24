import Api

home_id = "de662f4c-1290-4c67-b983-636714782a41"
openhab_id = "684fed03-b982-4059-a366-005d111d8ed8"

thing_motion_global_id = "{}/binary_sensor.motion_detection".format(home_id)
item_motion_global_id = "{}/binary_sensor.motion_detection/binary_sensor.motion_detection".format(home_id)
last_motion = "off"

thing_red_global_id = "{}/Switch2".format(openhab_id)
item_red_global_id = "{}/Switch2/Switch2".format(openhab_id)

thing_green_global_id = "{}/Switch3".format(openhab_id)
item_green_global_id = "{}/Switch3/Switch3".format(openhab_id)

thing_yellow_global_id = "{}/Switch1".format(openhab_id)
item_yellow_global_id = "{}/Switch1/Switch1".format(openhab_id)

thing_light_global_id = "{}/Light".format(openhab_id)
item_light_global_id = "{}/Light/Light".format(openhab_id)


def check_motion(thing_motion_global_id, item_motion_global_id):
    global last_motion
    now_motion = Api.api_get_item_state_by_id(thing_motion_global_id, item_motion_global_id)
    print(now_motion)
    now_state = now_motion['item_state']
    print(now_state)
    if last_motion == "off" and now_state == "on":
        now_light = Api.api_get_item_state_by_id(thing_light_global_id, item_light_global_id)['item_state']
        now_light = int(now_light)
        last_motion = now_state
        print('now_light: ', now_light)
        if now_light == 0:
            print('Anh Sang 0: Den Vang')
            Api.api_set_state(thing_yellow_global_id, item_yellow_global_id, "ON")
            Api.api_set_state(thing_red_global_id, item_red_global_id, "OFF")
            Api.api_set_state(thing_green_global_id, item_green_global_id, "OFF")
        elif now_light == 1:
            print('Anh Sang 1: Den Do')
            Api.api_set_state(thing_yellow_global_id, item_yellow_global_id, "OFF")
            Api.api_set_state(thing_red_global_id, item_red_global_id, "ON")
            Api.api_set_state(thing_green_global_id, item_green_global_id, "OFF")
        elif now_light == 2:
            print('Anh Sang 1: Den Xanh')
            Api.api_set_state(thing_yellow_global_id, item_yellow_global_id, "OFF")
            Api.api_set_state(thing_red_global_id, item_red_global_id, "OFF")
            Api.api_set_state(thing_green_global_id, item_green_global_id, "ON")
        else:
            print("Loi now_light")
    else:
        last_motion = now_state
while True:
    check_motion(thing_motion_global_id, item_motion_global_id)