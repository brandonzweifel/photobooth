import Action

class CallableAction(Action.Action):
    def __init__(self, f):
        Action.Action.__init__(self)
        self.f = f

    def on_update(self, elapsed):
        Action.Action.on_update(self, elapsed)

        self.f()

        self.succeed()