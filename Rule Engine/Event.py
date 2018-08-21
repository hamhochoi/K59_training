class Event:
    event_name = ''
    event_id = ''
    event_source = ''

    def __init__(self, event_name, event_id, event_source):
        self.event_name   = event_name
        self.event_id     = event_id
        self.event_source = event_source


