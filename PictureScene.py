import photobooth
from photobooth import CameraUtils
import pi3d
import numpy as np
import constants

class PictureScene(photobooth.Scene):

    def __init__(self, display, camera, event_queue, camera_utils):
        self.preview_texture = pi3d.Texture(np.zeros((CameraUtils.PREVIEW_HEIGHT, CameraUtils.PREVIEW_WIDTH, 3), dtype='uint8'))
        self.number1 = None
        self.number2 = None
        self.number3 = None
        self.number4 = None
        self.number5 = None

        self.preview1 = None
        self.preview2 = None
        self.preview3 = None
        self.preview4 = None

        self.removable_shapes = []

        self.flash = None

        photobooth.Scene.__init__(self, display, camera, event_queue, camera_utils)

    def on_create(self):
        background = pi3d.ImageSprite("resources/background.jpg", shader=self.SHADER, x = 0, y = 0, z=1, w = self.display.width, h = self.display.height)
        self.add_shape(background)

        hold_still = pi3d.ImageSprite("resources/hold-still.png", shader=self.SHADER, x=self.convert_x(906), y=self.convert_y(220), w=self.convert_w(303), h=self.convert_h(68))
        self.add_shape(hold_still)

        preview_box_texture = pi3d.Texture("resources/preview-box.png")
        preview_background = pi3d.Texture("resources/preview-background.png")

        preview_background1 = pi3d.ImageSprite(preview_background, shader = self.SHADER, x = self.convert_x(201), y = self.convert_y(245), w=self.convert_w(190), h=self.convert_h(141))
        preview_background2 = pi3d.ImageSprite(preview_background, shader = self.SHADER, x = self.convert_x(456), y = self.convert_y(245), w=self.convert_w(190), h=self.convert_h(141))
        preview_background3 = pi3d.ImageSprite(preview_background, shader = self.SHADER, x = self.convert_x(201), y = self.convert_y(503), w=self.convert_w(190), h=self.convert_h(141))
        preview_background4 = pi3d.ImageSprite(preview_background, shader = self.SHADER, x = self.convert_x(456), y = self.convert_y(503), w=self.convert_w(190), h=self.convert_h(141))

        self.add_shape(preview_background1)
        self.add_shape(preview_background2)
        self.add_shape(preview_background3)
        self.add_shape(preview_background4)

        self.preview1 = pi3d.ImageSprite(preview_box_texture, shader = self.SHADER, x = self.convert_x(201), y = self.convert_y(245), w=self.convert_w(192), h=self.convert_h(175))
        self.preview2 = pi3d.ImageSprite(preview_box_texture, shader = self.SHADER, x = self.convert_x(456), y = self.convert_y(245), w=self.convert_w(192), h=self.convert_h(175))
        self.preview3 = pi3d.ImageSprite(preview_box_texture, shader = self.SHADER, x = self.convert_x(201), y = self.convert_y(503), w=self.convert_w(192), h=self.convert_h(175))
        self.preview4 = pi3d.ImageSprite(preview_box_texture, shader = self.SHADER, x = self.convert_x(456), y = self.convert_y(503), w=self.convert_w(192), h=self.convert_h(175))

        self.add_shape(self.preview1)
        self.add_shape(self.preview2)
        self.add_shape(self.preview3)
        self.add_shape(self.preview4)

        self.number1 = pi3d.ImageSprite("resources/1.png", shader=self.SHADER, x=0, y=0, w=self.convert_w(25), h=self.convert_h(71))
        self.number2 = pi3d.ImageSprite("resources/2.png", shader=self.SHADER, x=0, y=0, w=self.convert_w(43), h=self.convert_h(72))
        self.number3 = pi3d.ImageSprite("resources/3.png", shader=self.SHADER, x=0, y=0, w=self.convert_w(42), h=self.convert_h(89))
        self.number4 = pi3d.ImageSprite("resources/4.png", shader=self.SHADER, x=0, y=0, w=self.convert_w(51), h=self.convert_h(72))
        self.number5 = pi3d.ImageSprite("resources/5.png", shader=self.SHADER, x=0, y=0, w=self.convert_w(40), h=self.convert_h(75))

        self.add_shape(self.number1)
        self.add_shape(self.number2)
        self.add_shape(self.number3)
        self.add_shape(self.number4)
        self.add_shape(self.number5)

        camera_preview = pi3d.ImageSprite(self.preview_texture, shader = self.SHADER, x = self.convert_x(920), y = self.convert_y(420), w = self.convert_w(428), h = self.convert_h(302))
        self.add_shape(camera_preview)

        camera_window = pi3d.ImageSprite("resources/camera-window.png", shader=self.SHADER, x = self.convert_x(918), y = self.convert_y(418), w = self.convert_w(438), h = self.convert_h(316))
        self.add_shape(camera_window)

        self.flash = pi3d.ImageSprite("resources/white.jpg", shader = self.SHADER, x = 0, y = 0, w = self.display.width, h = self.display.height)
        self.flash.set_alpha(0)
        self.add_shape(self.flash)

    def on_show(self):
        photobooth.Scene.on_show(self)

        for shape in self.removable_shapes:
            self.remove_shape(shape)

        self.removable_shapes = []

        self.number1.set_alpha(0)
        self.number2.set_alpha(0)
        self.number3.set_alpha(0)
        self.number4.set_alpha(0)
        self.number5.set_alpha(0)

        countdown1 = self.action_countdown(1)
        countdown1.get_last_action().attach_child(self.action_take_picture(1))

        countdown2 = self.action_countdown(2)
        countdown2.get_last_action().attach_child(self.action_take_picture(2))

        countdown3 = self.action_countdown(3)
        countdown3.get_last_action().attach_child(self.action_take_picture(3))

        countdown4 = self.action_countdown(4)
        countdown4.get_last_action().attach_child(self.action_take_picture(4))

        countdown1.get_last_action().attach_child(countdown2)
        countdown2.get_last_action().attach_child(countdown3)
        countdown3.get_last_action().attach_child(countdown4)

        wait = photobooth.WaitAction(2)
        wait.attach_child(photobooth.CallableAction(lambda: self.global_event_queue.add_event(photobooth.Event(constants.EVENT_PROCESS_SCENE))))
        countdown4.get_last_action().attach_child(wait)

        self.attach_action(countdown1)

    def action_countdown(self, picture_number):

        position = self.position_for_picture_preview(picture_number)

        move1 = photobooth.MoveAction(self.number1, duration=0, pos=(position[0], position[1], 0))
        move2 = photobooth.MoveAction(self.number2, duration=0, pos=(position[0], position[1], 0))
        move3 = photobooth.MoveAction(self.number3, duration=0, pos=(position[0], position[1], 0))
        move4 = photobooth.MoveAction(self.number4, duration=0, pos=(position[0], position[1], 0))
        move5 = photobooth.MoveAction(self.number5, duration=0, pos=(position[0], position[1], 0))

        move1.attach_child(move2)
        move2.attach_child(move3)
        move3.attach_child(move4)
        move4.attach_child(move5)

        wait_duration = 0.66

        show1 = photobooth.AlphaAction(self.number1, duration=0, alpha=1)
        wait1 = photobooth.WaitAction(duration=wait_duration)
        hide1 = photobooth.AlphaAction(self.number1, duration=0, alpha=0)
        show1.attach_child(wait1)
        wait1.attach_child(hide1)

        show2 = photobooth.AlphaAction(self.number2, duration=0, alpha=1)
        wait2 = photobooth.WaitAction(duration=wait_duration)
        hide2 = photobooth.AlphaAction(self.number2, duration=0, alpha=0)
        show2.attach_child(wait2)
        wait2.attach_child(hide2)

        show3 = photobooth.AlphaAction(self.number3, duration=0, alpha=1)
        wait3 = photobooth.WaitAction(duration=wait_duration)
        hide3 = photobooth.AlphaAction(self.number3, duration=0, alpha=0)
        show3.attach_child(wait3)
        wait3.attach_child(hide3)

        show4 = photobooth.AlphaAction(self.number4, duration=0, alpha=1)
        wait4 = photobooth.WaitAction(duration=wait_duration)
        hide4 = photobooth.AlphaAction(self.number4, duration=0, alpha=0)
        show4.attach_child(wait4)
        wait4.attach_child(hide4)

        show5 = photobooth.AlphaAction(self.number5, duration=0, alpha=1)
        wait5 = photobooth.WaitAction(duration=wait_duration)
        hide5 = photobooth.AlphaAction(self.number5, duration=0, alpha=0)
        show5.attach_child(wait5)
        wait5.attach_child(hide5)

        hide5.attach_child(show4)
        hide4.attach_child(show3)
        hide3.attach_child(show2)
        hide2.attach_child(show1)

        move5.attach_child(show5)

        return move1

    def action_take_picture(self, picture_number):
        flash = photobooth.AlphaAction(self.flash, duration=0, alpha=1.0)
        flash.get_last_action().attach_child(photobooth.CallableAction(lambda: self.global_event_queue.add_event(photobooth.Event(constants.TAKE_PICTURE, data=picture_number))))
        flash.get_last_action().attach_child(photobooth.CallableAction(lambda: self.update_from_picture(picture_number)))
        flash.get_last_action().attach_child(photobooth.AlphaAction(self.flash, duration=0, alpha=0.0))
        return flash

    def position_for_picture_preview(self, picture_number):
        if picture_number == 1:
            return self.convert_x(201), self.convert_y(245)
        elif picture_number == 2:
            return self.convert_x(456), self.convert_y(245)
        elif picture_number == 3:
            return self.convert_x(201), self.convert_y(503)
        elif picture_number == 4:
            return self.convert_x(456), self.convert_y(503)

    def update_from_picture(self, picture_number):
        position = self.position_for_picture_preview(picture_number)

        if picture_number == 1:
            target_shape = self.preview1
        elif picture_number == 2:
            target_shape = self.preview2
        elif picture_number == 3:
            target_shape = self.preview3
        else:
            target_shape = self.preview4

        picture_preview = pi3d.ImageSprite("photos/image" + str(picture_number) + ".jpg", shader=self.SHADER, x=position[0], y=position[1] + 1, w=self.convert_w(190), h=self.convert_h(141))
        picture_preview.set_alpha(0)
        self.add_shape_under(picture_preview, target_shape)
        self.attach_action(photobooth.AlphaAction(picture_preview, 2.0, 1.0))
        self.removable_shapes.append(picture_preview)

    def update(self):
        photobooth.Scene.update(self)

        while self.event_queue.has_events():
            event = self.event_queue.get_event()

            if event.get_type() == photobooth.Event.CAMERA_UPDATED:
                self.preview_texture.update_ndarray(event.data)
