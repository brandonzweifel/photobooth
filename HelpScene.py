import photobooth
import pi3d
import constants

class HelpScene(photobooth.Scene):

    def on_create(self):
        background = pi3d.ImageSprite("resources/background.jpg", shader=self.SHADER, x = 0, y = 0, z=1, w = self.display.width, h = self.display.height)
        self.add_shape(background)

        help_text = pi3d.ImageSprite("resources/help.png", shader=self.SHADER, x=self.convert_x(636), y=self.convert_y(338), w=self.convert_w(970), h=self.convert_h(336))
        self.add_shape(help_text)

    def on_show(self):
        wait = photobooth.WaitAction(duration=5.0)
        transition = photobooth.CallableAction(lambda: self.global_event_queue.add_event(photobooth.Event(constants.EVENT_PICTURE_SCENE)))
        wait.attach_child(transition)

        self.attach_action(wait)