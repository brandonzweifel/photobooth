import threading

class Event:
    NONE = 0
    BUTTON = 1
    CAMERA_UPDATED = 2

    def __init__(self, type, data = None):
        self.type = type
        self.data = data

    def get_type(self):
        return self.type

class EventQueue:
    def __init__(self):
        self.events = []
        self.lock = threading.Lock()

    def add_event(self, event):
        with self.lock:
            self.events.append(event)

    def has_events(self):
        return len(self.events) > 0

    def get_event(self):
        with self.lock:
            if self.has_events():
                return self.events.pop(0)

            return None