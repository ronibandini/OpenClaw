# MicroPython: MAX7219 8x8 LED matrix scroll
# Wiring: CLK->GP2, CS->GP1, DIN(DOUT)->GP0

import time
import framebuf
from machine import Pin, SoftSPI
import max7219

NUM_MATRICES = 1  # change to 4 if you have a 4-in-1 module
ROTATE_90 = True  # rotate 90° clockwise (only works for 1 matrix)

spi = SoftSPI(baudrate=1000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(0), miso=Pin(4))
cs = Pin(1)

display = max7219.Matrix8x8(spi, cs, NUM_MATRICES)
display.brightness(6)
# hard clear to avoid all-lit state
for _ in range(2):
    display.fill(0)
    display.show()
    time.sleep(0.1)

width = 8 * NUM_MATRICES
_temp = bytearray(8 * NUM_MATRICES)
_temp_fb = framebuf.FrameBuffer(_temp, width, 8, framebuf.MONO_HLSB)

def rotate_90():
    if not ROTATE_90 or NUM_MATRICES != 1:
        return
    _temp_fb.fill(0)
    for x in range(8):
        for y in range(8):
            _temp_fb.pixel(x, y, display.pixel(y, 7 - x))
    display.buffer[:] = _temp

def scroll_text(msg, delay=0.12):
    # total scroll length: message width + display width
    for x in range(len(msg) * 8 + width):
        display.fill(0)
        display.text(msg, width - x, 0, 1)
        rotate_90()
        display.show()
        time.sleep(delay)

# quick sanity pattern: single pixel
for i in range(width):
    display.fill(0)
    display.pixel(i, 0, 1)
    rotate_90()
    display.show()
    time.sleep(0.05)

while True:
    scroll_text("Hello Open Claw ")
