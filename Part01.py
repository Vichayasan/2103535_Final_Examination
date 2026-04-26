# Micro-Python code Part01
"""
a)    PUSH and RELEASE the button to drive the belt system at maximum speed in one direction. PUSH and RELEASE again will toggle its direction.
b)    LED is in GREEN at the beginning. LED turns RED when the Limit Switch is hit.
c)    PUSH and HOLD the button for 1 second, send the message “Take a picture” to REPL (Read-Eval-Print Loop).
d)    Can exit the program from the keyboard (KeyboardInterrupt). The motor will stop.
"""

from picozero import Button, LED, PWMOutputDevice, Potentiometer
import time

# CONFIG PINS
BUTTON       = Button(14, bounce_time=0.02)
M2A          = PWMOutputDevice(17)
M2B          = PWMOutputDevice(16)
LIMIT_SWITCH = Button(21, pull_up=False)
LED_GREEN    = LED(7, pwm=False)
LED_RED      = LED(6, pwm=False)
Poten        = Potentiometer(27)

press_time = 0

def control_Motor():
    if (M2A.value == 0 and M2B.value == 0) or (M2A.value == 1 and M2B.value == 1):
        M2A.on()
        M2B.off()
    elif M2A.value == 1:
        M2A.off()
        M2B.on()
    else:
        M2A.on()
        M2B.off()

def control_Camera():
    print("Take a picture")

def control_LED():
    LED_GREEN.toggle()
    LED_RED.toggle()


# Start timer
def on_press(): 
    global press_time
    press_time = time.ticks_ms()

# Calculate timer for debouce after release button
def on_release():
    held = time.ticks_diff(time.ticks_ms(), press_time)
    if held >= 1000: # If held the button less than 1 second
        control_Camera()
    else: # If held the button more than 1 second
        control_Motor()

# Init
LED_GREEN.on()
LED_RED.off()
M2A.off()
M2B.off()

# Interrupt Callback to use funtion reference
BUTTON.when_activated       = on_press
BUTTON.when_deactivated     = on_release
LIMIT_SWITCH.when_activated = control_LED
LIMIT_SWITCH.when_deactivated = control_LED

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    M2A.off()
    M2B.off()
    print("Motor stopped.")
