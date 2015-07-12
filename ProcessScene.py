import photobooth
import pi3d
import os
import subprocess
import constants

class ProcessScene(photobooth.Scene):

    def __init__(self, display, camera, event_queue, camera_utils):
        self.lightning = None
        self.process = None
        photobooth.Scene.__init__(self, display, camera, event_queue, camera_utils)

    def on_create(self):
        background = pi3d.ImageSprite("resources/processing.jpg", shader=self.SHADER, x = 0, y = 0, z=1, w = self.display.width, h = self.display.height)
        self.add_shape(background)

        self.lightning = pi3d.ImageSprite("resources/lightning.png", shader=self.SHADER, x=self.convert_x(490), y=self.convert_y(82), w=self.convert_w(280), h=self.convert_h(170))
        self.add_shape(self.lightning)

        self.flicker_lightning()

    def flicker_lightning(self):
        hide = photobooth.AlphaAction(self.lightning, duration=0, alpha=0)
        wait = photobooth.WaitAction(duration=0.5)
        show = photobooth.AlphaAction(self.lightning, duration=0, alpha=1)
        wait2 = photobooth.WaitAction(duration=0.5)

        hide.attach_child(wait)
        wait.attach_child(show)
        show.attach_child(wait2)
        wait2.attach_child(photobooth.CallableAction(lambda: self.flicker_lightning()))

        self.attach_action(hide)

    def on_show(self):

        # do the thing...
        command = "/usr/bin/python " + os.path.dirname(os.path.realpath(__file__)) + "/photos/process-photos.py"
        self.process = subprocess.Popen(command, shell=True)

    def update(self):
        photobooth.Scene.update(self)

        if self.process is not None:
            if self.process.poll() is not None:
                self.process = None

                wait = photobooth.WaitAction(duration=60)
                wait.attach_child(photobooth.CallableAction(lambda: self.global_event_queue.add_event(photobooth.Event(constants.EVENT_END_SCENE))))

                self.attach_action(wait)