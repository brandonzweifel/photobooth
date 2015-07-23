import photobooth
import pi3d
import constants

class TitleScene(photobooth.Scene):

    def __init__(self, camera, display, geq, camera_utils):
        self.press_to_start = None

        photobooth.Scene.__init__(self, camera, display, geq, camera_utils)

    def on_create(self):

        background = pi3d.ImageSprite("resources/title.jpg", shader=self.SHADER, x = 0, y = 0, z=1, w = self.display.width, h = self.display.height)
        self.add_shape(background)

        self.press_to_start = pi3d.ImageSprite("resources/press-the-button.png", shader=self.SHADER, x=self.convert_x(643), y=self.convert_y(541), z=1,  w=self.convert_w(521), h=self.convert_h(44))
        self.add_shape(self.press_to_start)

        self.attach_blink()

    def attach_blink(self):
        wait = photobooth.WaitAction(1.0)
        alpha_off = photobooth.AlphaAction(self.press_to_start, duration = 0, alpha = 0.05)
        wait2 = photobooth.WaitAction(1.0)
        alpha_on = photobooth.AlphaAction(self.press_to_start, duration = 0, alpha = 1.0)
        repeat = photobooth.CallableAction(lambda: self.attach_blink())

        alpha_off.attach_child(repeat)
        wait2.attach_child(alpha_off)
        alpha_on.attach_child(wait2)
        wait.attach_child(alpha_on)

        self.attach_action(wait)

    def update(self):
        photobooth.Scene.update(self)

        while self.event_queue.has_events():
            if self.event_queue.get_event().get_type() == photobooth.Event.BUTTON:
                # go to the next scene...
                self.global_event_queue.add_event(photobooth.Event(constants.EVENT_PICTURE_SCENE))
