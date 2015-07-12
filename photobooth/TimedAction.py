import Action

class TimedAction(Action.Action):
    def __init__(self, duration = 1.0):
        Action.Action.__init__(self)

        self.duration = duration
        self.elapsed = 0

    def t(self):
        if self.duration == 0:
            return 1

        return min(self.elapsed / self.duration, 1.0)

    def on_update(self, elapsed):
        Action.Action.on_update(self, elapsed)

        self.elapsed += elapsed

        self.update_timed(self.t())

        if self.elapsed >= self.duration:
            self.succeed()

    def on_init(self):
        Action.Action.on_init(self)

        self.elapsed = 0

    def update_timed(self, t):
        pass