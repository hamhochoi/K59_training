
import json
import numpy as np
from openhab import openHAB

base_url = 'http://localhost:8080/rest'
openhab = openHAB(base_url)

# fetch all items
items = openhab.fetch_all_items()	# dict of openHAB items
#print (items)
#items = items.items()	# convert dict into list
#print (items)
#items = items.keys()
items = list(items)
#items = np.asarray(items)
#items_list = list(items[:, 0])
items_list = list(items)
print (items_list)
# check_item = [items_list[0]]
# print ()
# print (check_item)
# remain_item_list = list(set(items_list) - set(check_item))
# print (remain_item_list==items_list)

# for i in range(len(items)):
# 	print (items[i][0])

item1 = openhab.get_item("LedVang")
item2 = openhab.get_item("LedXanh")
item3 = openhab.get_item("LedDo")
item4 = openhab.get_item("Motion")
item5 = openhab.get_item("Temperature")
item6 = openhab.get_item("Light")
item7 = openhab.get_item("Humidity")

# print (str(item.state))

item1.command("ON")
item2.command("ON")
item3.command("ON")
item4.command(1)
item5.command(1000)
item6.command(1)
item7.command(10)

# item = openhab.get_item_raw("Switch1")
print (item1)
print (item2)
print (item3)
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
