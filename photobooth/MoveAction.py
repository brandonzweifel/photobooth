import TimedAction

class MoveAction(TimedAction.TimedAction):
    def __init__(self, shape, duration=1.0, pos = (0, 0, 0)):
        TimedAction.TimedAction.__init__(self, duration)

        self.end_pos = pos
        self.start_pos = (0, 0, 0)
        self.shape = shape

    def update_timed(self, t):
        TimedAction.TimedAction.update_timed(self, t)

        x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * t
        y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * t
        z = self.start_pos[2] + (self.end_pos[2] - self.start_pos[2]) * t

        self.shape.position(x, y, z)

    def on_init(self):
        TimedAction.TimedAction.on_init(self)

        self.start_pos = (self.shape.x(), self.shape.y(), self.shape.z())
