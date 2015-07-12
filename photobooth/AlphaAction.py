import TimedAction

class AlphaAction(TimedAction.TimedAction):
    def __init__(self, shape, duration=1.0, alpha = 1.0):
        TimedAction.TimedAction.__init__(self, duration)

        self.end_alpha = alpha
        self.start_alpha = 1.0
        self.shape = shape

    def update_timed(self, t):
        TimedAction.TimedAction.update_timed(self, t)

        a = self.start_alpha + (self.end_alpha - self.start_alpha) * t
        self.shape.set_alpha(a)

    def on_init(self):
        TimedAction.TimedAction.on_init(self)

        self.start_alpha = self.shape.alpha()