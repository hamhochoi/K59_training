

class Action_Base():
    actor_name = ''
    actor_id = ''

    def __init__(self, actor_name, actor_id):
        self.actor_name = actor_name
        self.actor_id = actor_id


    def receiveCallToAction(self):
        pass

    def execute(self, action_id):
        pass