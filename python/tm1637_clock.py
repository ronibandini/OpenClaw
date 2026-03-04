# MicroPython clock loop for TM1637 on RP2040
# Pins: CLK=GP3, DIO=GP2 (LattePanda IOTA header SCLK/SDIO)

import time
from machine import Pin, RTC
import tm1637

clk = Pin(3)
dio = Pin(2)
disp = tm1637.TM1637(clk=clk, dio=dio)
disp.brightness(2)

# If RTC has not been set, you can set it manually here (year, month, day, weekday, hour, minute, second, subseconds)
# Example: RTC().datetime((2026, 3, 3, 1, 10, 45, 0, 0))

rtc = RTC()

while True:
    t = rtc.datetime()  # (year, month, day, weekday, hour, minute, second, subseconds)
    hh = t[4]
    mm = t[5]
    # Toggle the colon every second for a clock-like blink
    disp.numbers(hh, mm, True)
    time.sleep(1)
