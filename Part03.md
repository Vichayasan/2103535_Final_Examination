*3. Briefly explain the program. What does it do?*
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
