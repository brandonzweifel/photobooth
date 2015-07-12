import pi3d
from ActionManager import ActionManager
import EventQueue

class Scene:
    SHADER = None

    def __init__(self, display, camera, event_queue, camera_utils):
        if self.SHADER is None:
            self.SHADER = pi3d.Shader("uv_flat")

        self.objects = []
        self.action_manager = ActionManager()
        self.display = display
        self.event_queue = EventQueue.EventQueue()
        self.global_event_queue = event_queue
        self.camera = camera
        self.camera_utils = camera_utils

        self.on_create()

    def add_event(self, event):
        self.event_queue.add_event(event)

    def attach_action(self, action):
        self.action_manager.attach_action(action)

    def add_actions(self, actions):
        for action in actions:
            self.attach_action(action)

    def convert_x(self, x):
        return self.convert_w(x) - self.display.width / 2

    def convert_y(self, y):
        return self.display.height / 2 - self.convert_h(y)

    def convert_w(self, w):
        return w / 1280.0 * self.display.width

    def convert_h(self, h):
        return h / 734.0 * self.display.height

    def on_create(self):
        pass

    def add_shape(self, shape):
        self.objects.append(shape)

    def add_shape_under(self, shape, under_shape):
        index = self.objects.index(under_shape)
        self.objects.insert(index, shape)

    def remove_shape(self, shape):
        self.objects.remove(shape)

    def remove_shapes(self):
        self.objects = []

    def draw(self):
        for shape in self.objects:
            shape.draw()

    def update(self):
        self.action_manager.update_actions(0.033)

    def on_show(self):
        pass