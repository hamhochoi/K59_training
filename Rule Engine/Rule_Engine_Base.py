

class Rule_Engine_Base():
    rule_engine_id = ''
    rule_engine_name = ''
    description = ''
    input_topic = ''
    output_topic = ''
    condition_types = []

    def __init__(self, rule_engine_name, rule_engine_id,
                 description, input_topic, output_topic):

        self.rule_engine_name = rule_engine_name
        self.rule_engine_id = rule_engine_id
        self.description = description
        self.input_topic = input_topic
        self.output_topic = output_topic

    def mapping(self, event_id):
        pass

    def check_condition(self, condition_id, condition_type, condition_content):
        pass

    def call_to_action(self, action_id, action_content):
        pass

    def receive_event(self):
        pass
