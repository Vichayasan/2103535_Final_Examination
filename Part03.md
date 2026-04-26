# 3. Briefly explain the program. What does it do?
**Program Description**

This program implements a camera belt system controller on a Raspberry Pi Pico using the picozero library. Upon initialization, the green LED activates and the motor remains stationary. A momentary push button controls the DC motor via the Cytron MDD3A driver — a short press toggles the belt direction between forward and reverse at maximum speed, while holding the button for one second transmits a "Take a picture" command to the REPL. The EE-SX470 photoelectric sensor functions as a limit switch; upon beam interruption, the green LED is deactivated and the red LED is illuminated as a fault indicator. The program terminates gracefully on KeyboardInterrupt, stopping the motor immediately.
