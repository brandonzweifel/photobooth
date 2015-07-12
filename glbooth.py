from __future__ import absolute_import, division, print_function, unicode_literals

import pi3d
import random
import constants
import picamera
import time

from TitleScene import TitleScene
from PictureScene import PictureScene
from HelpScene import HelpScene
from ProcessScene import ProcessScene
from EndScene import EndScene
from photobooth import EventQueue, Event, CameraUtils
from RPi import GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, GPIO.PUD_UP)
button_down_frames = 0
button_down_to_process = False

camera = picamera.PiCamera()

# we're upside down right now, maybe we won't be eventually
camera.resolution = (1024, 768)
camera.framerate = 5
camera.rotation = 180
camera.color_effects = (128, 128)
camera.iso = 800

BACKGROUND = (0.0, 0.0, 0.0, 1.0)

DISPLAY =  pi3d.Display.create(background = BACKGROUND, depth=0, frames_per_second = 30)
CAMERA = pi3d.Camera(is_3d = False)

global_event_queue = EventQueue()
camera_utils = CameraUtils(camera, global_event_queue)

title_scene = TitleScene(DISPLAY, camera, global_event_queue, camera_utils)
picture_scene = PictureScene(DISPLAY, camera, global_event_queue, camera_utils)
help_scene = HelpScene(DISPLAY, camera, global_event_queue, camera_utils)
process_scene = ProcessScene(DISPLAY, camera, global_event_queue, camera_utils)
end_scene = EndScene(DISPLAY, camera, global_event_queue, camera_utils)

current_scene = title_scene
current_scene.on_show()

grain_shader = pi3d.Shader("uv_flat")

grain_images = [
    pi3d.ImageSprite("resources/grain1.jpg", shader=grain_shader, x=0, y=0, z=1, w=DISPLAY.width, h=DISPLAY.height)
]

grain_images[0].set_alpha(0.05)
# grain_images[1].set_alpha(0.1)

camera_utils.start_capturing_image()

while DISPLAY.loop_running():
    # graphics stuff
    current_scene.update()
    current_scene.draw()

    if random.randrange(0, 100) < 50:
        grain_images[0].draw()

    # button stuff
    if GPIO.input(17) == 0:
        button_down_frames += 1

        if button_down_frames > 3:
            if not button_down_to_process:
                current_scene.add_event(Event(Event.BUTTON))
                button_down_to_process = True
    else:
        button_down_to_process = False
        button_down_frames = 0

    # application stuff
    while global_event_queue.has_events():
        event = global_event_queue.get_event()

        if event.get_type() == constants.EVENT_PICTURE_SCENE:
            current_scene = picture_scene
            current_scene.on_show()
        elif event.get_type() == constants.EVENT_TITLE_SCENE:
            current_scene = title_scene
            current_scene.on_show()
        elif event.get_type() == constants.EVENT_HELP_SCENE:
            current_scene = help_scene
            current_scene.on_show()
        elif event.get_type() == constants.EVENT_PROCESS_SCENE:
            current_scene = process_scene
            current_scene.on_show()
        elif event.get_type() == constants.EVENT_END_SCENE:
            current_scene = end_scene
            current_scene.on_show()
        elif event.get_type() == Event.CAMERA_UPDATED:
            current_scene.add_event(event)
        elif event.get_type() == constants.TAKE_PICTURE:
            picture_index = event.data
            file_name = "photos/image" + str(picture_index) + ".jpg"
            camera_utils.stop_capturing_image()
            camera.color_effects = None
            time.sleep(0.25)
            camera.capture(file_name)
            camera.color_effects = (128, 128)
            camera_utils.start_capturing_image()