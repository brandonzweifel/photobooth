import Action

class WaitAction(Action.Action):
    def __init__(self, duration):
        Action.Action.__init__(self)

        self.duration = duration
        self.elapsed = 0

    def on_init(self):
        Action.Action.on_init(self)

        self.elapsed = 0

    def on_update(self, elapsed):
        Action.Action.on_update(self, elapsed)

        self.elapsed += elapsed

        if self.elapsed >= self.duration:
            self.succeed()