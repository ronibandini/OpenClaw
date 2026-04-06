# Made by OpenClaw 
# Running on a LattePanda IOTA
# Roni Bandini, 03/2026

#!/usr/bin/env python3
import os
import re
import json
import math
import time
import datetime as dt
from pathlib import Path
import requests
import xml.etree.ElementTree as ET
from escpos.printer import File
from PIL import Image, ImageDraw, ImageFont

PRINTER_DEV = "/dev/usb/lp0"
OUT_TXT = Path("/home/roni/.openclaw/workspace/openclaw_ticket_news.txt")

# ---------- Helpers ----------

def days_lived(birth=dt.date(1974, 6, 17)):
    return (dt.date.today() - birth).days


def fetch_weather_ba():
    data = requests.get("https://wttr.in/Buenos_Aires?format=j1", timeout=10).json()
    today = data["weather"][0]
    desc = today["hourly"][4]["weatherDesc"][0]["value"]
    return f"{desc}, {today['maxtempC']}°C/{today['mintempC']}°C"


def fetch_finance():
    spy = requests.get("https://stooq.pl/q/l/?s=spy.us&f=sd2t2ohlcv&h&e=csv", timeout=10).text.strip().splitlines()[-1].split(',')
    spy_price = spy[6]
    btc = requests.get("https://api.coinbase.com/v2/prices/spot?currency=USD", timeout=10).json()["data"]["amount"]
    fx = requests.get("https://open.er-api.com/v6/latest/USD", timeout=10).json()["rates"]["ARS"]
    return spy_price, btc, fx


def fetch_clarin_headlines(limit=3):
    try:
        response = requests.get("https://www.clarin.com/rss/tecnologia/", timeout=30)
        root = ET.fromstring(response.content)
        out = []
        for item in root.findall(".//item"):
            title = item.find("title").text
            if title:
                out.append(title.strip())
            if len(out) >= limit:
                break
        return out
    except Exception:
        return ["(sin datos — error en RSS de Clarín)"]


def system_status():
    st = os.statvfs('/')
    free_gb = (st.f_bavail * st.f_frsize) / (1024**3)
    meminfo = Path('/proc/meminfo').read_text()
    m = re.search(r"MemAvailable:\s+(\d+)", meminfo)
    mem_mb = int(m.group(1)) / 1024 if m else 0
    up = float(Path('/proc/uptime').read_text().split()[0])
    up_h = up / 3600
    return free_gb, mem_mb, up_h


def build_text():
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    lived = days_lived()
    wx = fetch_weather_ba()
    spy, btc, ars = fetch_finance()
    headlines = fetch_clarin_headlines()
    free_gb, mem_mb, up_h = system_status()
    quote = "“La inteligencia artificial es la nueva electricidad.” — Andrew Ng"

    lines = []
    lines.append(f"Fecha: {now}")
    lines.append(f"Días vividos: {lived}")
    lines.append(f"Clima en Buenos Aires: {wx}")
    lines.append("")
    lines.append(f"SPY: {spy} | BTC: {btc} USD")
    lines.append(f"USD/ARS: {ars:.2f}")
    lines.append("")
    lines.append("Titulares (Clarín Tecnología):")
    for h in headlines:
        lines.append(f"- {h}")
    lines.append("")
    lines.append(f"Disco libre: {free_gb:.1f} GB")
    lines.append(f"RAM disponible: {mem_mb:.0f} MB")
    lines.append(f"Uptime: {up_h:.1f} h")
    lines.append("")
    lines.append(quote)
    return "\n".join(lines)


def print_ticket(text):
    if not os.path.exists(PRINTER_DEV):
        OUT_TXT.write_text(text + "\n\n[ERROR] Printer device not found: /dev/usb/lp0\n")
        return False
    
    IMAGE_PATH = "/home/roni/.openclaw/workspace/ticketnews.jpg"
    MAX_WIDTH = 384

    img = Image.open(IMAGE_PATH).convert("L")
    w, h = img.size
    if w > MAX_WIDTH:
        new_h = int(h * (MAX_WIDTH / w))
        img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)

    printer = File(PRINTER_DEV)

    printer.set(align="center")
    printer.text("OpenClaw Ticket News\n\n")
    printer.image(img)
    printer.text("\n\n")

    printer.set(align="left", bold=False, width=1, height=1)
    printer.text(text + "\n")
    printer.cut()
    return True


def main():
    text = build_text()
    OUT_TXT.write_text(text + "\n")
    ok = print_ticket(text)
    if ok:
        print("printed")
    else:
        print("printer not found")


if __name__ == "__main__":
    main()