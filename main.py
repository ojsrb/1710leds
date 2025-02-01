# created by Owen Schmidt

# this code takes a while to load, please be patient

# NOTE: file reading isn't working for some reason, please download it and add it in the editor here:
# https://raw.githubusercontent.com/ojsrb/1710leds/refs/heads/main/animation.bmp
# Thanks for your cooperation!
# (This would not happen if this was running locally on a device)

import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import requests
import json
import time

current_length = 0

animation = True

team = None

bitmap = displayio.OnDiskBitmap("animation.bmp")
pixel_shader = bitmap.pixel_shader



def show_scout():
    global team
    print("scouted team " + str(team))

def check_scouts():
    global current_length, animation, team
    r = requests.get("https://scouting.team1710.com/api/key/team")
    data = json.loads(r.text)
    print(data)
    if len(data) > current_length:
        current_length = len(data)
        team = data[-1]
        show_scout()
        animation = False
        return True
    else:
        team = None
        return False

matrix = rgbmatrix.RGBMatrix(
   width=64, height=32, bit_depth=1,
   rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
   addr_pins=[board.A5, board.A4, board.A3, board.A2],
   clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

frame = 0

class Image(displayio.TileGrid):
    def __init__(self):
        super().__init__(bitmap=bitmap, pixel_shader=pixel_shader, width=64, height=32, tile_width=448, tile_height=32)

        self.x = 0
        self.y = 0

image = Image()

g = displayio.Group()
g.append(image)

def start_anim():

    global image, g, frame

    image.x = -frame * 64

    display.root_group = g

def reload_text():
    global team, animation
    group_root = displayio.Group()
    group_text = displayio.Group()

    label_scout = ""

    if animation == False: 
        label_scout = "Scouted:"

    text_0 = adafruit_display_text.label.Label(
     terminalio.FONT,
    color=0x00ffff,
    text=label_scout)
    text_0.x = 0
    text_0.y = 5

    
    text_1 = adafruit_display_text.label.Label(
     terminalio.FONT,
    color=0xffffff,
    text=str(team))
    text_1.x = 0
    text_1.y = 20

    if animation:
        text_0.x = -64
        text_0.y = -32
        text_1.x = -64
        text_1.y = -32
    
    group_text.append(text_0)
    group_text.append(text_1)

    group_root.append(group_text)
    display.root_group = group_root

while True:
    time.sleep(0.125)
    if animation:
        if frame % 180 == 0:
            check_scouts()
    else:
        reload_text()
        display.refresh(minimum_frames_per_second=5)
        time.sleep(5)
        animation = True

    reload_text()
    start_anim()
    display.refresh(minimum_frames_per_second=5)
    frame += 1
