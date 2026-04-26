# Wiring Diagram Of Part01
<img width="1908" height="1209" alt="6872087421_Vichayasan_wiring" src="https://github.com/user-attachments/assets/6ee285f5-5d5d-4fd9-96de-c4b6cffd5faa" />

# Micro-Python code Part01
a)    PUSH and RELEASE the button to drive the belt system at maximum speed in one direction. PUSH and RELEASE again will toggle its direction.?<br/>
b)    LED is in GREEN at the beginning. LED turns RED when the Limit Switch is hit.<br/>
c)    PUSH and HOLD the button for 1 second, send the message “Take a picture” to REPL (Read-Eval-Print Loop).<br/>
d)    Can exit the program from the keyboard (KeyboardInterrupt). The motor will stop.<br/>
```python
from picozero import Button, LED, PWMOutputDevice, Potentiometer
import time

# CONFIG PINS
BUTTON       = Button(14, bounce_time=0.02)
M2A          = PWMOutputDevice(17)
M2B          = PWMOutputDevice(16)
LIMIT_SWITCH = Button(21, pull_up=False)
LED_GREEN    = LED(7, pwm=False)
LED_RED      = LED(6, pwm=False)
Poten        = Potentiometer(10)

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
```

# Micro-Python code Part02
Modify the code to: <br/>
a) Read the potentiometer with a 1-second update rate. <br/>
b) The button is “push button”. Pull up resister is required. <br/>
c) Limit the power to the motor to maximum of 50% duty cycle. <br/>
d) Correct the program. <br/>

```python
from machine import Pin, ADC, PWM
import time

pot       = ADC(Pin(26))
button    = Pin(14, Pin.IN, Pin.PULL_UP)   # ✅ PULL_UP
motor_pwm = PWM(Pin(15))
motor_pwm.freq(1000)
motor_in1 = Pin(16, Pin.OUT)
motor_in2 = Pin(17, Pin.OUT)

direction    = True
last_pot_read = 0

while True:
    now = time.ticks_ms()

    # a) Read pot every 1 second
    if time.ticks_diff(now, last_pot_read) >= 1000:
        pot_value  = pot.read_u16()
        duty_cycle = pot_value // 2        # c) max 50% duty cycle
        motor_pwm.duty_u16(duty_cycle)
        last_pot_read = now

    # b) PULL_UP → active LOW → use not
    if not button.value():
        direction = not direction
        time.sleep(0.3)

    if direction:
        motor_in1.high()
        motor_in2.low()
    else:
        motor_in1.low()
        motor_in2.high()

    time.sleep(0.05)
```

# Briefly explain the program. What does it do?
**Program Description**

This program implements a camera belt system controller on a Raspberry Pi Pico using the picozero library. Upon initialization, the green LED activates and the motor remains stationary. A momentary push button controls the DC motor via the Cytron MDD3A driver — a short press toggles the belt direction between forward and reverse at maximum speed, while holding the button for one second transmits a "Take a picture" command to the REPL. The EE-SX470 photoelectric sensor functions as a limit switch; upon beam interruption, the green LED is deactivated and the red LED is illuminated as a fault indicator. The program terminates gracefully on `KeyboardInterrupt`, stopping the motor immediately.
