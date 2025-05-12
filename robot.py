import numpy as np 
from helpers import 

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
            ret, grip_now, angle_degrees, direction = self.vision.scan(block_color = "green")
        elif block_color == "red":
            ret, grip_now, angle_degrees, direction = self.vision.scan(block_color = "red")
        elif block_color == "blue":
            ret, grip_now, angle_degrees, directinon = self.vision.scan(block_color == "blue")
        return ret, grip_now, angle_degrees, direction
    
    def pivot_to_goal(self):
        current_x, current_y, current_heading = self.travel_log.current_pose.copy()
        goal_x, goal_y, goal_heading = self.travel_log.construction_pose.copy()
        dx_abs = abs(goal_x - current_x)
        dy_abs = abs(goal_y - current_y)
        
        if current_heading >= 0:
            pivot_angle = abs(current_heading) + np.rad2deg(np.arctan(dx_abs / dy_abs))
            print(f"Final pivot left to face the goal: Pivot left {pivot_angle: .2f} degrees.")
            self.moves.pivot_left(pivot_angle)
        else:
            pivot_angle = current_heading + np.rad2deg(np.arctan(dx_abs / dy_abs))
            print(f"Final pivot right to face the goal: Pivot right {pivot_angle: .2f} degrees")
            self.moves.pivot_right(pivot_angle)

        current_heading = self.interfaces.read_imu()
        self.travel_log.update_log_pivot_to_goal(current_heading)

        distance_to_goal = (dx_abs*dx_abs + dy_abs*dy_abs)**0.5
        print(f"Distance to goal: {distance_to_goal: .2f} m")
        return distance_to_goal 

    def open_gripper(self):
        self.interfaces.open_gripper()

    def close_gripper(self):
        self.interfaces.close_gripper()

    def check_email(self):
        self.interfaces.check_email()
    
    def email(self):
        self.interfaces.email()
