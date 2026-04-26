# Wiring Diagram Of Part01
<img width="1971" height="1283" alt="Screenshot 2026-04-25 085720" src="https://github.com/user-attachments/assets/35b76a13-add2-4e5d-bc88-dade0e97787a" />

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

This program implements a unidirectional DC motor speed and direction control system using a Raspberry Pi Pico microcontroller. The system comprises an analog potentiometer, a momentary push button, and a PWM-driven motor driver interface.

---

**Operation**

Upon initialization, the system configures the following peripherals:
- `ADC` on GP26 for analog potentiometer reading
- `PWM` on GP15 at 1 kHz carrier frequency for motor speed control
- `GPIO` GP16 and GP17 as digital outputs for motor direction control
- `GPIO` GP14 as a digital input with internal pull-up resistor for button sensing

The main control loop executes the following tasks continuously:

**1) Speed Control (1-second update rate)**
The potentiometer is sampled via a 16-bit ADC (`read_u16()`) at a non-blocking 1-second interval using `time.ticks_ms()`. The raw ADC value (0–65535) is scaled to 50% of its maximum range by integer right-shift division (`// 2`), yielding a duty cycle range of 0–32767. This value is applied to the PWM output, limiting motor power to a maximum of 50% duty cycle.

**2) Direction Control**
The push button is polled on every loop iteration. Since the internal pull-up resistor is enabled, a logic LOW (`0`) indicates a button press. Upon detection, the boolean flag `direction` is toggled and a 300 ms software debounce delay is applied to prevent false triggering.

**3) Motor Direction Output**
Based on the `direction` flag, GP16 and GP17 are driven in complementary states — one HIGH and one LOW — to set the H-bridge motor driver's rotation direction.
