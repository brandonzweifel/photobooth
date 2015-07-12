class Action:
    STATE_UNINITIALIZED = 0
    STATE_REMOVED = 1
    STATE_RUNNING = 2
    STATE_PAUSED = 3
    STATE_SUCCEEDED = 4
    STATE_FAILED = 5
    STATE_ABORTED  = 6

    def __init__(self):
        self.state = self.STATE_UNINITIALIZED
        self.child = None

    def on_init(self):
        self.state = self.STATE_RUNNING

    def on_update(self, elapsed):
        pass

    def on_succeed(self):
        pass

    def on_fail(self):
        pass

    def on_abort(self):
        self.on_fail()

    def succeed(self):
        self.state = self.STATE_SUCCEEDED

    def fail(self):
        self.state = self.STATE_FAILED

    def pause(self):
        self.state = self.STATE_PAUSED

    def resume(self):
        self.state = self.STATE_RUNNING

    def get_state(self):
        return self.state

    def is_alive(self):
        return self.state == self.STATE_RUNNING or self.state == self.STATE_PAUSED

    def is_dead(self):
        return self.state == self.STATE_SUCCEEDED or self.state == self.STATE_FAILED or self.state == self.STATE_ABORTED

    def is_removed(self):
        return self.state == self.STATE_REMOVED

    def is_paused(self):
        return self.state == self.STATE_PAUSED

    def attach_child(self, child):
        self.child = child

    def remove_child(self):
        self.child = None

    def has_child(self):
        return self.child is not None

    def get_child(self):
        return self.child

    def set_state(self, state):
        self.state = state

    def get_last_action(self):
        last = self
        while last.has_child():
            last = last.get_child()

        return last