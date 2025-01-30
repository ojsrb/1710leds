import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio

bitmap = displayio.OnDiskBitmap("pixilart-sprite.bmp")
pixel_shader = bitmap.pixel_shader

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

class image(displayio.TileGrid):
    def __init__(self):
        super().__init__(bitmap=bitmap, pixel_shader=pixel_shader, width=64, height=32, tile_width=8704, tile_height=32)

        self.x = 0
        self.y = 0
        


g = displayio.Group()

image = image()
g.append(image)

display.root_group = g

frame = 0;

while True:
    image.x = frame * 64
    frame -= 1
    display.refresh(minimum_frames_per_second=5)
