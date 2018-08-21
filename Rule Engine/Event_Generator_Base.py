from Event import Event

class Event_Generator_Base():

    event_generator_id = ''
    event_generator_name = ''
    description = ''
    event_source_topic = ''
    event_dest_topic = ''
    event_types = []



    def __init__(self, event_generator_name, event_generator_id,
                 description, event_dest_topic):

        self.event_generator_id = event_generator_id
        self.event_generator_name = event_generator_name
        self.description = description
        # self.event_source_topic = event_source_topic
        self.event_dest_topic = event_dest_topic
        # self.event_types = event_types

    def check_trigger_condition(self, trigger_id, trigger_type, trigger_content, item_id):
        pass

    def receive_states(self):
        pass

    event = Event('', '', '')
    def create_event(self, trigger_id):
        pass

    def read_event_condition(self):
        pass


