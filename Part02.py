# Micro-Python code Part02
'''
Modify the code to:
# a) Read the potentiometer with a 1-second update rate.
# b) The button is “push button”. Pull up resister is required.
# c) Limit the power to the motor to maximum of 50% duty cycle.
# d) Correct the program.
''' 

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
