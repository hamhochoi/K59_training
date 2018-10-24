from abc import ABCMeta, abstractmethod


class Driver(object):
    PARAM_PORT = 'port'
    PARAM_HOST = 'host'

    def __init__(self):
        self.port = None
        self.host = None

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_item_by_name(self, name):
        pass

    # @abstractmethod
    # def get_item_by_id(self, id):
    #     pass

    @abstractmethod
    def get_states(self):
        pass

    @abstractmethod
    def get_state_by_name(self, name):
        pass

    @abstractmethod
    # def get_state_by_id(self, id):
    #     pass

    @abstractmethod
    def get_actions(self, id):
        pass

    @abstractmethod
    def get_item_types(self):
        pass

    @abstractmethod
    def set_state_by_id(self, local_id, action, new_state):
        pass

    @abstractmethod
    def transform_data(self, data):
        pass

