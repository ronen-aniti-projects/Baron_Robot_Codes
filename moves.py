from helpers import normalize_angle
import RPi.GPIO as gpio
import serial 
import numpy as np
import time

class Moves:
    def __init__(self, config, interfaces):
        self.config = config
        self.interfaces = interfaces 
        self.pivot_tolerance = self.config.pivot_tolerance # 3 #2 # degrees
        self.translational_p_gain = 50.0
    
    def pulse_left(self):
        self.interfaces.stop_motors()
        start_time = time.time()
        while time.time() - start_time < 0.05:
            self.interfaces.motors_lr.ChangeDutyCycle(100)
            self.interfaces.motors_rf.ChangeDutyCycle(100)
        self.interfaces.stop_motors()
        time.sleep(0.25)

    def pulse_right(self):
        self.interfaces.stop_motors()
        start_time = time.time()
        while time.time() - start_time < 0.05:
            self.interfaces.motors_lf.ChangeDutyCycle(100)
            self.interfaces.motors_rr.ChangeDutyCycle(100)
        self.interfaces.stop_motors()
        time.sleep(0.25)    

    def pivot_left(self, angle_degrees):
        self.interfaces.stop_motors()
        heading = self.interfaces.read_imu() 
        goal_heading = normalize_angle(heading - angle_degrees)
        initial_error = normalize_angle(goal_heading - heading)
        error = initial_error 
        print("Pivot left")
        print(f"Goal heading {goal_heading}")
        print(f"Start heading {heading}")
        print(f"Error in heading {error}")
        self.interfaces.motors_lr.ChangeDutyCycle(100)
        self.interfaces.motors_rf.ChangeDutyCycle(100)
        while(abs(error) > self.pivot_tolerance): 
            #(error * initial_error) > 0) and
            error = normalize_angle(goal_heading - self.interfaces.read_imu())
            print(error)
        self.interfaces.stop_motors()
        time.sleep(1)
    
    def pivot_right(self, angle_degrees):
        self.interfaces.stop_motors()
        heading = self.interfaces.read_imu() 
        goal_heading = normalize_angle(heading + angle_degrees)
        initial_error = normalize_angle(goal_heading - heading)
        error = initial_error 
        print("Pivot right")
        print(f"Goal heading {goal_heading}")
        print(f"Start heading {heading}")
        print(f"Error in heading {error}")
        self.interfaces.motors_lf.ChangeDutyCycle(100)
        self.interfaces.motors_rr.ChangeDutyCycle(100)
        while(abs(error) > self.pivot_tolerance): 
            # (error * initial_error) > 0) and
            error = normalize_angle(goal_heading - self.interfaces.read_imu())
            print(error)
        self.interfaces.stop_motors()
        time.sleep(1)
    
    def forward(self, distance_meters):
        print("Entering forward motion")
        goal_ticks = int(
            distance_meters / self.config.wheel_circumference * self.config.ticks_per_revolution
        )
        # Encoder counters
        left_count = np.uint64(0)
        right_count = np.uint64(0)
        # Encoder states
        left_state = int(0)
        right_state = int(0)
        # Timeout function
        start_time = time.time()
        timeout = 90 # seconds
        while True: 
            if (time.time() - start_time) > timeout:
                self.interfaces.motors_lf.ChangeDutyCycle(0)
                self.interfaces.motors_rf.ChangeDutyCycle(0)
            if int(gpio.input(self.config.left_encoder_pin)) != left_state:
                left_count += 1
                left_state = int(gpio.input(self.config.left_encoder_pin))
            if int(gpio.input(self.config.right_encoder_pin)) != right_state:
                right_count += 1
                right_state = int(gpio.input(self.config.right_encoder_pin))
            if left_count >= goal_ticks and right_count >= goal_ticks:
                self.interfaces.motors_lf.ChangeDutyCycle(0)
                self.interfaces.motors_rf.ChangeDutyCycle(0)
                return True
            error = left_count - right_count 
            left_control = max(0, min(100, 50 - self.translational_p_gain * error))
            right_control = max(0, min(100, 50 + self.translational_p_gain * error))
            self.interfaces.motors_lf.ChangeDutyCycle(left_control)
            self.interfaces.motors_rf.ChangeDutyCycle(right_control)
            time.sleep(0.005)
        self.interfaces.stop_motors()
        time.sleep(1)
     
    def reverse(self, distance_meters):
        goal_ticks = int(
            distance_meters / self.config.wheel_circumference * self.config.ticks_per_revolution
        )
        # Encoder counters
        left_count = np.uint64(0)
        right_count = np.uint64(0)
        # Encoder states
        left_state = int(0)
        right_state = int(0)
        # Timeout function
        start_time = time.time()
        timeout = 90 # seconds
        while True: 
            if (time.time() - start_time) > timeout:
                self.interfaces.motors_lf.ChangeDutyCycle(0)
                self.interfaces.motors_rf.ChangeDutyCycle(0)
            if int(gpio.input(self.config.left_encoder_pin)) != left_state:
                left_count += 1
                left_state = int(gpio.input(self.config.left_encoder_pin))
            if int(gpio.input(self.config.right_encoder_pin)) != right_state:
                right_count += 1
                right_state = int(gpio.input(self.config.right_encoder_pin))
            if left_count >= goal_ticks and right_count >= goal_ticks:
                self.interfaces.motors_lr.ChangeDutyCycle(0)
                self.interfaces.motors_rr.ChangeDutyCycle(0)
                return True
            error = left_count - right_count 
            left_control = max(0, min(100, 50 - self.translational_p_gain * error))
            right_control = max(0, min(100, 50 + self.translational_p_gain * error))
            self.interfaces.motors_lr.ChangeDutyCycle(left_control)
            self.interfaces.motors_rr.ChangeDutyCycle(right_control)
            time.sleep(0.005)
        self.interfaces.stop_motors()
        time.sleep(1)