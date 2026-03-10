<img width="1232" height="864" alt="OpenClawForMakers" src="https://github.com/user-attachments/assets/b1719cb1-f801-4f0e-a97e-0ce29ade12bd" />

# OpenClaw
OpenClaw as a maker autoconfigured device starting from raw components

# Requirements 

Lattepanda IOTA
https://www.dfrobot.com/product-2991.html?tracking=hOuIhw4fDaJRTdy4abz04npbQC78dqxBkqVt7XMFYxEXj2s0ukWgm71wbut0ewUP 

Active Cooler
https://www.dfrobot.com/product-2987.html?tracking=hOuIhw4fDaJRTdy4abz04npbQC78dqxBkqVt7XMFYxEXj2s0ukWgm71wbut0ewUP 

Methane gas sensor
https://www.dfrobot.com/product-2708.html?tracking=hOuIhw4fDaJRTdy4abz04npbQC78dqxBkqVt7XMFYxEXj2s0ukWgm71wbut0ewUP 

Also: 5v3A Power Supply, LED, 7 Segment display

# Setup
1. Install Ubuntu
2. Install OpenClaw curl -fsSL https://openclaw.ai/install.sh | bash
3. Run these commands:
sudo apt install python3-pip
pip3 install pyserial
sudo usermod -a -G dialout roni

# USB Web cam

If you want to use a web cam so OpenClaw will be able to make verifications, run also

sudo apt-get update -y
sudo apt-get install -y fswebcam v4l-utils
sudo usermod -aG video roni

# Requests

Example: "Tell me where do I connect a Sainsmart 8x8 led matrix and make it work to display a space invaders ship"

# Python code

In this repository you will find a python folder with some of the developments made by OpenClaw. Please consider that they are using the onboard RP2040, so OpenClaw is running those scripts using, for example

mpremote connect /dev/ttyACM0 exec "import max7219_scroll" 

# Contact

Roni Bandini
https://www.instagram.com/ronibandini/
https://x.com/RoniBandini
