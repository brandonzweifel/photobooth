import photobooth
import pi3d
import constants

class EndScene(photobooth.Scene):

    def on_create(self):
        background = pi3d.ImageSprite("resources/end.jpg", shader=self.SHADER, x = 0, y = 0, z=1, w = self.display.width, h = self.display.height)
        self.add_shape(background)

    def on_show(self):
        wait = photobooth.WaitAction(duration=60)
        go = photobooth.CallableAction(lambda: self.global_event_queue.add_event(photobooth.Event(constants.EVENT_TITLE_SCENE)))
        wait.attach_child(go)

        self.attach_action(wait)