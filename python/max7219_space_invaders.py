
# MicroPython: MAX7219 8x8 LED matrix - Space Invaders (rotated 90°)
# Wiring: CLK->GP2, CS->GP1, DIN(DOUT)->GP0

import time
import framebuf
from machine import Pin, SoftSPI
import max7219

NUM_MATRICES = 1

spi = SoftSPI(baudrate=1000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(0), miso=Pin(4))
cs = Pin(1)

display = max7219.Matrix8x8(spi, cs, NUM_MATRICES)
display.brightness(6)

width = 8 * NUM_MATRICES
_temp = bytearray(8 * NUM_MATRICES)
_temp_fb = framebuf.FrameBuffer(_temp, width, 8, framebuf.MONO_HLSB)

def rotate_90():
    _temp_fb.fill(0)
    for x in range(8):
        for y in range(8):
            _temp_fb.pixel(x, y, display.pixel(y, 7 - x))
    display.buffer[:] = _temp

# Space Invaders 8x8 sprite (classic)
INVADER = [
    0b00100100,
    0b00011000,
    0b00111100,
    0b01111110,
    0b11111111,
    0b10111101,
    0b00100100,
    0b01000010,
]

# Draw sprite into frame buffer
for y, row in enumerate(INVADER):
    for x in range(8):
        if row & (1 << (7 - x)):
            display.pixel(x, y, 1)

rotate_90()
display.show()

# keep it visible
while True:
    time.sleep(1)
