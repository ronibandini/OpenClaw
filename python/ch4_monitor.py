#!/usr/bin/env python3
"""
CH4 air quality monitor (host side)
- Reads RP2040 ADC via mpremote
- Logs to CSV
- Evaluates a simple air-quality status message

NOTE: ADC works only on GP26/GP27/GP28. GP4 is not ADC-capable.
"""
import csv
import datetime as dt
import subprocess
import re
import fcntl

LOCK_PATH = "/tmp/rp2040.lock"

MPREMOTE = "/home/roni/.local/bin/mpremote"
PORT = "/dev/ttyACM0"
ADC_PIN = 26  # GP26 = ADC0
CSV_PATH = "/home/roni/.openclaw/workspace/ch4_air_quality.csv"

# Thresholds are placeholders. Calibrate with your sensor baseline.
# raw is 0..65535
THRESH_LOW = 12000
THRESH_MED = 25000
THRESH_HIGH = 40000
ROLLING_N = 5


def read_adc_raw():
    cmd = (
        f"{MPREMOTE} connect {PORT} exec "
        f"\"from machine import ADC,Pin; adc=ADC(Pin({ADC_PIN})); print(adc.read_u16())\""
    )
    with open(LOCK_PATH, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        out = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
    # find last integer in output
    nums = re.findall(r"\d+", out)
    return int(nums[-1]) if nums else None


def classify(raw):
    if raw is None:
        return "sensor read failed"
    if raw < THRESH_LOW:
        return "air quality is good"
    if raw < THRESH_MED:
        return "air quality is average"
    if raw < THRESH_HIGH:
        return "air quality is low, you should open a window"
    return "air quality is poor, ventilate immediately"


def rolling_average(n):
    try:
        with open(CSV_PATH, "r", newline="") as f:
            rows = list(csv.reader(f))
    except FileNotFoundError:
        return None
    values = []
    for row in rows[-n:]:
        if len(row) < 2:
            continue
        try:
            values.append(int(row[1]))
        except ValueError:
            continue
    if not values:
        return None
    return sum(values) / len(values)


def main():
    raw = read_adc_raw()
    avg = rolling_average(ROLLING_N)
    avg_for_status = raw if avg is None else avg
    status = classify(avg_for_status)
    now = dt.datetime.now().isoformat(timespec="seconds")

    with open(CSV_PATH, "a", newline="") as f:
        w = csv.writer(f)
        w.writerow([now, raw, f"{avg_for_status:.1f}", status])

    print(now, raw, f"avg={avg_for_status:.1f}", status)


if __name__ == "__main__":
    main()
