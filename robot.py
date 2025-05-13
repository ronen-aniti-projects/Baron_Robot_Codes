import numpy as np 
from helpers import feet2meters, meters2feet, heading_error 
import math 


class Robot:
    def __init__(self, config, interfaces, moves, travel_log, vision):
        self.config = config 
        self.interfaces = interfaces
        self.moves = moves 
        self.travel_log = travel_log
        self.vision = vision

    def pulse_left(self):
        self.moves.pulse_left()
        new_heading = self.interfaces.read_imu()
        self.travel_log.update_log_pulse_left(new_heading)
        print(self.travel_log.current_pose)
    
    def pulse_right(self):
        self.moves.pulse_right()
        new_heading = self.interfaces.read_imu()
        self.travel_log.update_log_pulse_right(new_heading)
        print(self.travel_log.current_pose)
    
    def pivot_left(self, angle_degrees):
        self.moves.pivot_left(angle_degrees)
        new_heading = self.interfaces.read_imu()
        self.travel_log.update_log_pivot_left(new_heading, angle_degrees)
        print(self.travel_log.current_pose)
    
    def pivot_right(self, angle_degrees):
        self.moves.pivot_right(angle_degrees)
        new_heading = self.interfaces.read_imu()
        self.travel_log.update_log_pivot_right(new_heading, angle_degrees)
        print(self.travel_log.current_pose)

    def forward(self, distance_meters):
        #start_heading = self.interfaces.read_imu()
        self.moves.forward(distance_meters)
        goal_heading = self.interfaces.read_imu()
        #average_heading = (start_heading + goal_heading) / 2
        average_heading = goal_heading # The arithmetic mean is not the same as circular mean! Modify this later if there is time. 
        self.travel_log.update_log_forward(average_heading, distance_meters)
        print(self.travel_log.current_pose)

    def reverse(self, distance_meters):
        start_heading = self.interfaces.read_imu()
        self.moves.reverse(distance_meters)
        goal_heading = self.interfaces.read_imu()
        #average_heading = (start_heading + goal_heading) / 2
        average_heading = goal_heading # The arithmetic mean is not the same as circular mean! Modify this later if there is time. 
        self.travel_log.update_log_reverse(average_heading, distance_meters)
        print(self.travel_log.current_pose)

    def scan(self, block_color):
        if block_color == "green":
            ret, grip_now, angle_degrees, direction, cy = self.vision.scan(block_color = "green")
        elif block_color == "red":
            ret, grip_now, angle_degrees, direction, cy = self.vision.scan(block_color = "red")
        elif block_color == "blue":
            ret, grip_now, angle_degrees, direction, cy = self.vision.scan(block_color = "blue")
        return ret, grip_now, angle_degrees, direction, cy
    
    def pivot_to_goal(self):
        current_x, current_y, current_psi = self.travel_log.current_pose 
        goal_x, goal_y, goal_psi = self.travel_log.construction_pose 
        error = heading_error(goal_psi, current_psi)
        if error > 0:
            print(f"Pivot left {error: 0.2f} to goal")
            self.moves.pivot_left(error)
        elif error < 0:
            print(f"Pivot right {error: 0.2f} to goal")
            self.moves.pivot_right(-error)
        else:
            print("Already facing the goal heading")
        
        new_heading  = self.interfaces.read_imu()
        self.travel_log.update_log_pivot_to_goal(new_heading)
        dist = math.hypot(goal_x - current_x, goal_y - current_y)
        return dist 
        

    def open_gripper(self):
        self.interfaces.open_gripper()

    def close_gripper(self):
        self.interfaces.close_gripper()

    def check_email(self):
        self.interfaces.check_email()
    
    def email(self):
        self.interfaces.email()
