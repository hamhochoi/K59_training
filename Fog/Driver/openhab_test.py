
import json
import numpy as np
from openhab import openHAB
from requests import get

base_url = 'http://localhost:8080/rest'
openhab = openHAB(base_url)

# fetch all items
items = openhab.fetch_all_items()	# dict of openHAB items
print (items)
item2 = openhab.get_item("LedVang")
print (item2)

item2.command('OFF')
print (item2)

#items = items.items()	# convert dict into list
#print (items)
#items = items.keys()
items = list(items)
items = np.asarray(items)
# print(items)
#items_list = list(items[:, 0])
items_list = list(items)
# print (items_list)


# check_item = [items_list[0]]
# print ()
# print (check_item)
# remain_item_list = list(set(items_list) - set(check_item))
# print (remain_item_list==items_list)

# for i in range(len(items)):
# 	print (items[i][0])

item1 = openhab.get_item("Temperature")
item2 = openhab.get_item("Humidity")
item3 = openhab.get_item("Light")
# print (str(item.state))
#
# item1.command(25)
# item2.command(18)
# item3.command(1)
# item = openhab.get_item_raw("Switch1")
# print (item1)
# print (item2)
# print (item3)
# print (item["type"])
# state = item.state
# print (state)

# #item.command('OFF')
# item.on()

# state = item.state
# print (state)


# info = openhab.get_item_raw("Switch1")


#print (info)
#print (items["network_pingdevice_192_168_1_79_online"])

#item = openhab.json_to_item(info)
#print (item)
# from requests import get
#
# thing_url = 'http://192.168.60.197:8080/rest/things'
# things = get(thing_url).json()
# print (things)

