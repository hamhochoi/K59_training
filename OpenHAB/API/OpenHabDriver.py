from Driver import Driver
import requests


class OpenHabDriver(Driver):

    def __init__(self, port, host):
        self.port = port
        self.host = host
        self.items = None
        self.item = None
        self.url = None
        self.states = None
        self.state = None

    def get_items(self):
        self.url = 'http://' + str(self.host) + ':' + str(self.port) + '/rest/items?recursive=false'
        self.items = requests.get(self.url)
        self.items = self.items.json()
        return self.items

    def get_item_by_name(self, name):
        self.url = 'http://' + str(self.host) + ':' + str(self.port) + '/rest/items/' + str(name)
        self.item = requests.get(self.url)
        self.item = self.item.json()
        return self.item

    def get_states(self):
        self.states = []
        self.items = self.get_items()

        for _item in self.items:
            self.states.append([_item['name'], _item['state']])

        return self.states

    def get_state_by_name(self, name):
        self.item = self.get_item_by_name(name)
        self.state = self.item['state']

        return self.state

    def get_item_types(self):
        pass




if __name__ == "__main__":
    host = 'localhost'
    port = 8080
    name = 'airquality_aqi_428c4d92_aqiDescription'
    openhab = OpenHabDriver(port, host)
    items = openhab.get_items()
    item = openhab.get_item_by_name(name)
    print (item)
    states = openhab.get_states()
    # print (states)
    state = openhab.get_state_by_name(name)
    # print (state)