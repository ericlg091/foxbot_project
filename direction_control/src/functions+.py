#!/usr/bin/env python3
# Import necessary libraries
import pyfirmata
import time
from numpy import pi

# Robot wheels
wheel_length = 25.15
wheel_distance = 30
length = wheel_distance*pi*2
velocity_100 = 24 # cm/s

# Setup communication with Arduino
board = pyfirmata.ArduinoMega('/dev/ttyUSB0')
print("Communication Successfully started")

# Initialize pins
PWM1 = board.get_pin('d:3:p')
PWM2 = board.get_pin('d:5:p')
M1INA = board.get_pin('d:22:o')
M1INB = board.get_pin('d:23:o')
M2INA = board.get_pin('d:24:o')
M2INB = board.get_pin('d:25:o')

# Function to turn off all motors
def power_off_all_motors():
    M1INA.write(0)
    M1INB.write(0)
    M2INA.write(0)
    M2INB.write(0)
    
# linear -- cm note  
# angular -- radians
# velocity -- between 0 and 1
def move_motors(linear, angular):
    power_off_all_motors()
    vel = 1
    print("linear: ", linear, "; angular: ", angular)
    
    if linear != 0:
        if linear > 0:
            M1INA.write(1)
            M1INB.write(0)
            M2INA.write(1)
            M2INB.write(0)
            print("set forwards")
        elif linear < 0:
            M1INA.write(0)
            M1INB.write(1)
            M2INA.write(0)
            M2INB.write(1)
            print("set backwards")
    
        vel_left = vel
        vel_right = vel

        percentage = abs(angular)*100/(2*pi)  # percentage of 2pi [%]
        equivalent_length = percentage*length/100   # equivalent length on the circle [cm]
        vel_dec = (equivalent_length)/(abs(linear)+equivalent_length) # [0-1] decremented velocity
        
        if angular >= 0:
            vel_left -= vel_dec
        else:
            vel_right -= vel_dec
        time_to_wait = abs(linear)/((vel-vel_dec)*velocity_100) # [s]
        
        print("vel_left = ", vel_left)
        print("vel_right = ", vel_right)
        
        if vel_left < 0:
            vel_left = 0
        if vel_right < 0:
            vel_right = 0
            
        PWM1.write(vel_left)
        PWM2.write(vel_right)
        time.sleep(time_to_wait)
        power_off_all_motors()
        print("finished. waited ", time_to_wait, "seconds")
        
    else:
        print("not moving")


# Main code block
if __name__ == '__main__':
    # Turn off all motors initially
    power_off_all_motors()

    try:
        # Main control loop
        #while True:
        move_motors(30, 0)
        
    except KeyboardInterrupt:
        print("\nExiting...")
        power_off_all_motors()
        board.exit()
