print('Morse greeting: HOLA AMIGOS (RP2040 interno)')

import serial
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUDRATE = 115200

# Faster than the OK script
DOT = 0.12
DASH = DOT * 3
INTRA = DOT
LETTER_GAP = DOT * 3
WORD_GAP = DOT * 7

MORSE = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',
    'E': '.',     'F': '..-.',  'G': '--.',   'H': '....',
    'I': '..',    'J': '.---',  'K': '-.-',   'L': '.-..',
    'M': '--',    'N': '-.',    'O': '---',   'P': '.--.',
    'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',
    'Y': '-.--',  'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.'
}

ser = serial.Serial(SERIAL_PORT, BAUDRATE)
time.sleep(2)  # allow RP2040 to reset

def send(cmd, delay=0.2):
    ser.write(cmd.encode('utf-8') + b'\r\n')
    time.sleep(delay)

def led_on(duration):
    send('led.value(1)', delay=duration)


def led_off(duration):
    send('led.value(0)', delay=duration)


def dot():
    led_on(DOT)
    led_off(INTRA)


def dash():
    led_on(DASH)
    led_off(INTRA)


def letter_gap():
    led_off(LETTER_GAP)


def word_gap():
    led_off(WORD_GAP)


def blink_morse(text):
    for i, ch in enumerate(text):
        if ch == ' ':
            word_gap()
            continue
        code = MORSE.get(ch)
        if not code:
            continue
        for symbol in code:
            if symbol == '.':
                dot()
            elif symbol == '-':
                dash()
        # letter gap after each letter
        letter_gap()


# Wake REPL
ser.write(b'\r\n')
time.sleep(0.2)

# Configure pin
send('from machine import Pin')
send('led = Pin(1, Pin.OUT)')

message = 'HOLA AMIGOS'
print('Mensaje:', message)
blink_morse(message)

# End with a clear OFF
led_off(WORD_GAP)

print('Listo: saludo en Morse completado')

# ---- Clean release ----
send('led.value(0)')                 # ensure OFF
send('led = None')                   # remove reference
send('import machine')
send('machine.reset()')              # full reset for clean state

ser.close()
