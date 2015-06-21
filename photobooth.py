import io
import picamera
import pygame
import os
import sys
import time
from RPi import GPIO

button = 17
FPS = 30

GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)

pygame.init()
pygame.mouse.set_visible(False)

disp_no = os.getenv("DISPLAY")
if disp_no:
    print "I'm running under X display = {0}".format(disp_no)

drivers = ['fbcon', 'directfb', 'svgalib']
found = False
for driver in drivers:
    # Make sure that SDL_VIDEODRIVER is set
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
    try:
        pygame.display.init()
    except pygame.error:
        print 'Driver: {0} failed.'.format(driver)
        continue
    found = True
    break

if not found:
    raise Exception('No suitable video driver found!')

# print pygame.display.list_modes(32, pygame.FULLSCREEN)

titleScreen = pygame.image.load("resources/title.jpg")
previewBackground = pygame.image.load("resources/background.jpg")
previewPreviewWindow = pygame.image.load("resources/preview-window.png")
previewImageWindow = pygame.image.load("resources/preview.png")
previewGetReady = pygame.image.load("resources/get-ready.png")
previewHoldStill = pygame.image.load("resources/hold-still.png")
preview1 = pygame.image.load("resources/1.png")
preview2 = pygame.image.load("resources/2.png")
preview3 = pygame.image.load("resources/3.png")

size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
# size = (1024, 768)
print "Framebuffer size: %d x %d" % (size[0], size[1])

def coords(x, y):
    return int(x / 1024.0 * size[0]), int(y / 768.0 * size[1])

def millis():
    return int(time.time() * 1000)

previewBackground = pygame.transform.scale(previewBackground, coords(previewBackground.get_size()[0], previewBackground.get_size()[1]))
previewImageWindow = pygame.transform.scale(previewImageWindow, coords(previewImageWindow.get_size()[0], previewImageWindow.get_size()[1]))
previewPreviewWindow = pygame.transform.scale(previewPreviewWindow, coords(previewPreviewWindow.get_size()[0], previewPreviewWindow.get_size()[1]))
previewGetReady = pygame.transform.scale(previewGetReady, coords(previewGetReady.get_size()[0], previewGetReady.get_size()[1]))
previewHoldStill = pygame.transform.scale(previewHoldStill, coords(previewHoldStill.get_size()[0], previewHoldStill.get_size()[1]))
preview1 = pygame.transform.scale(preview1, coords(preview1.get_size()[0], preview1.get_size()[1]))
preview2 = pygame.transform.scale(preview2, coords(preview2.get_size()[0], preview2.get_size()[1]))
preview3 = pygame.transform.scale(preview3, coords(preview3.get_size()[0], preview3.get_size()[1]))

targetOffset = coords(1, 18)
targetFrame = coords(190, 141)

preview1FramePos = coords(105, 162)
preview1ImagePos = (preview1FramePos[0] + targetOffset[0], preview1FramePos[1] + targetOffset[1])

preview2FramePos = coords(312, 162)
preview2ImagePos = (preview2FramePos[0] + targetOffset[0], preview2FramePos[1] + targetOffset[1])

preview3FramePos = coords(522, 162)
preview3ImagePos = (preview3FramePos[0] + targetOffset[0], preview3FramePos[1] + targetOffset[1])

preview4FramePos = coords(733, 162)
preview4ImagePos = (preview4FramePos[0] + targetOffset[0], preview4FramePos[1] + targetOffset[1])

screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

def showCameraWithImage(image, durationInMillis):
    cameraPosition = coords(368, 452)
    cameraSize = (320, 240)#coords(315, 227)

    rgb = bytearray(cameraSize[0] * cameraSize[1] * 3)

    drawPreviewScreen(())

    imageSize = image.get_size()
    adjustedBottom = coords(0, 428)
    screen.blit(image, (size[0] / 2 - imageSize[0] / 2, adjustedBottom[1] - imageSize[1]))

    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.rotation = 180
        camera.crop = (0.0, 0.0, 1.0, 1.0)

        clock = pygame.time.Clock()

        start = millis()

        while millis() - start < durationInMillis:
            stream = io.BytesIO()
            camera.capture(stream, use_video_port=True, format='rgb', resize=cameraSize)
            stream.seek(0)
            stream.readinto(rgb)
            stream.close()

            img = pygame.image.frombuffer(rgb[0:(cameraSize[0] * cameraSize[1] * 3)], cameraSize, 'RGB')
            screen.blit(pygame.transform.scale(img, coords(291, 205)), cameraPosition)
            screen.blit(previewPreviewWindow, coords(357, 443))
            pygame.display.update()

            clock.tick(60)

def drawPreviewScreen(existingImages):
    # show the preview screen
    screen.blit(previewBackground, (0, 0))

    # image windows
    if(len(existingImages) > 0):
        screen.blit(existingImages[0], preview1ImagePos)
    screen.blit(previewImageWindow, preview1FramePos)

    if(len(existingImages) > 1):
        screen.blit(existingImages[1], preview2ImagePos)
    screen.blit(previewImageWindow, preview2FramePos)

    if(len(existingImages) > 2):
        screen.blit(existingImages[2], preview3ImagePos)
    screen.blit(previewImageWindow, preview3FramePos)

    if(len(existingImages) > 3):
        screen.blit(existingImages[3], preview4ImagePos)
    screen.blit(previewImageWindow, preview4FramePos)

def showCameraWithCountDown(existingImages):
    cameraPosition = coords(368, 452)
    cameraSize = (320, 240)#coords(315, 227)

    rgb = bytearray(cameraSize[0] * cameraSize[1] * 3)

    drawPreviewScreen(existingImages)

    image = previewHoldStill
    imageSize = image.get_size()
    adjustedBottom = coords(0, 428)
    screen.blit(image, (size[0] / 2 - imageSize[0] / 2, adjustedBottom[1] - imageSize[1]))

    transform1 = preview1
    transform2 = preview2
    transform3 = preview3
    adjustedCenter = coords(515, 551)

    lastPicture = None

    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.rotation = 180
        camera.crop = (0.0, 0.0, 1.0, 1.0)

        clock = pygame.time.Clock()

        start = millis()

        while millis() - start < 3000:
            now = millis()

            stream = io.BytesIO()
            camera.capture(stream, use_video_port=True, format='rgb', resize=cameraSize)
            stream.seek(0)
            stream.readinto(rgb)
            stream.close()

            if now - start < 1000:
                overlay = transform3
            elif now - start < 2000:
                overlay = transform2
            else:
                overlay = transform1

            img = pygame.image.frombuffer(rgb[0:(cameraSize[0] * cameraSize[1] * 3)], cameraSize, 'RGB')
            lastPicture = img
            screen.blit(pygame.transform.scale(img, coords(291, 205)), cameraPosition)
            screen.blit(previewPreviewWindow, coords(357, 443))
            screen.blit(overlay, (adjustedCenter[0] - overlay.get_size()[0] / 2, adjustedCenter[1] - overlay.get_size()[1] / 2))
            pygame.display.update()

            clock.tick(60)

    return lastPicture

def takePicture(pic, index, existingImages):
    screen.fill((255, 255, 255))
    pygame.display.update()

    startPos = coords(368, 452)

    if index == 1:
        endPos = preview1ImagePos
    elif index == 2:
        endPos = preview2ImagePos
    elif index == 3:
        endPos = preview3ImagePos
    else:
        endPos = preview4ImagePos

    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.rotation = 180

        camera.capture("image" + str(index) + ".jpg")

    clock = pygame.time.Clock()

    # Move this picture up!
    start = millis()
    while True:
        now = millis()

        t = float(now - start) / 2000.0

        if t >= 1.0:
            t = 1.0

        drawPreviewScreen(existingImages)
        screen.blit(pic, (int(startPos[0] + (endPos[0] - startPos[0]) * t), int(startPos[1] + (endPos[1] - startPos[1]) * t)))
        pygame.display.update()

        if t >= 1.0:
            break

        clock.tick(30)

while True:
    # Show the title screen...
    screen.blit(pygame.transform.scale(titleScreen, size), (0, 0))

    pygame.display.update()

    # Wait for a button press
    GPIO.add_event_detect(button, GPIO.FALLING)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                sys.exit()

        if GPIO.event_detected(button):
            GPIO.remove_event_detect(button)
            break

    showCameraWithImage(previewGetReady, 2000)
    firstPicture = showCameraWithCountDown(())
    firstPicture = pygame.transform.scale(firstPicture, targetFrame)
    takePicture(firstPicture, 1, ())

    secondPicture = showCameraWithCountDown((firstPicture,))
    secondPicture = pygame.transform.scale(secondPicture, targetFrame)
    takePicture(secondPicture, 2, (firstPicture,))

    thirdPicture = showCameraWithCountDown((firstPicture, secondPicture))
    thirdPicture = pygame.transform.scale(thirdPicture, targetFrame)
    takePicture(thirdPicture, 3, (firstPicture, secondPicture))

    fourthPicture = showCameraWithCountDown((firstPicture, secondPicture, thirdPicture))
    fourthPicture = pygame.transform.scale(fourthPicture, targetFrame)
    takePicture(fourthPicture, 4, (firstPicture, secondPicture, thirdPicture))

    drawPreviewScreen((firstPicture, secondPicture, thirdPicture, fourthPicture))
    pygame.display.update()

    time.sleep(10)