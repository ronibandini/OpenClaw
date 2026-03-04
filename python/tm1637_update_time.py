#!/usr/bin/env python3
import time
import subprocess

# Local time (system timezone)
now = time.localtime()
hh = now.tm_hour
mm = now.tm_min

cmd = (
    "/home/roni/.local/bin/mpremote connect /dev/ttyACM0 exec "
    "\"import tm1637; from machine import Pin; "
    "disp=tm1637.TM1637(clk=Pin(3), dio=Pin(2)); "
    f"disp.numbers({hh}, {mm}, True)\""
)

subprocess.run(cmd, shell=True, check=False)
