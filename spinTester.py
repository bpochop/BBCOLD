import pyfirmata
import time as t

board0 = pyfirmata.Arduino('/dev/ttyUSB0')
mixer_motor = board0.get_pin('d:4:o')
stepper_motor_dir = board0.get_pin('d:2:o')
stepper_motor_step = board0.get_pin('d:3:o')
stepper_motor_enable = board0.get_pin('d:7:o')

print("running enable pin now")
#stepper_motor_enable.write(1)
t.sleep(1)
print("done")


mixer_motor.write(1)
step_count = 900
delay = .001

def spinMotor():
     
    mixer_motor.write(0)# turns on motor
    t.sleep(2)
    mixer_motor.write(1)
    print("done")
 
    
def up():
     
    stepper_motor_dir.write(1)
    for x in range(step_count):
        stepper_motor_step.write(1)
        t.sleep(delay)
        stepper_motor_step.write(0)
        t.sleep(delay)
 
def down():
    stepper_motor_dir.write(0)
    for x in range(step_count):
        stepper_motor_step.write(1)
        t.sleep(delay)
        stepper_motor_step.write(0)
        t.sleep(delay)
        
        
print("turning on now")
stepper_motor_enable.write(0)
t.sleep(1)
print("GOING DOWN")
down()
print("spinning")
spinMotor()
print("going up")
up()
t.sleep(1)
stepper_motor_enable.write(1)
print("done, time to sleep")




