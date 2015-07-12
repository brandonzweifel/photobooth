import io
import numpy as np
import threading
from EventQueue import Event

lock = threading.Lock()

class CameraUtils:
    PREVIEW_WIDTH = 320
    PREVIEW_HEIGHT = 240

    def __init__(self, camera, event_queue):

        self.event_queue = event_queue
        self.camera = camera
        self.camera_thread = None

    def start_capturing_image(self):
        self.camera_thread = CameraThread(self.camera, self)

    def stop_capturing_image(self):
        self.camera_thread.terminated = True

class CameraThread(threading.Thread):
    def __init__(self, camera, camera_utils):
        super(CameraThread, self).__init__()
        self.camera = camera
        self.terminated = False
        self.stream = io.BytesIO()
        self.rgb = bytearray(CameraUtils.PREVIEW_WIDTH * CameraUtils.PREVIEW_HEIGHT * 3)
        self.camera_utils = camera_utils

        self.start()

    def run(self):
        while not self.terminated:

            self.camera.capture(self.stream, format = 'rgb', use_video_port=True, resize=(CameraUtils.PREVIEW_WIDTH, CameraUtils.PREVIEW_HEIGHT))

            self.stream.seek(0)
            self.stream.readinto(self.rgb)

            self.stream.seek(0)
            self.stream.truncate()

            self.camera_utils.event_queue.add_event(Event(Event.CAMERA_UPDATED, data=np.frombuffer(self.rgb, 'uint8')))
