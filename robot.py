import numpy as np 
from helpers import feet2meters, meters2feet, normalize_angle
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
        goal_x = self.travel_log.construction_pose[0]
        goal_y = self.travel_log.construction_pose[1]
        current_x = self.travel_log.current_pose[0]
        current_y = self.travel_log.current_pose[1]
        current_psi = self.travel_log.current_pose[2]
        dx = abs(goal_x - current_x)
        dy = abs(goal_y - current_y)

        theta = np.arctan(dx / dy) * 180/np.pi
        if abs(current_psi) > theta:
            if current_psi < 0:
                self.pivot_right(abs(current_psi) - theta)
            elif current_psi > 0:
                self.pivot_left(current_psi + theta)
        elif abs(current_psi) < theta:
            if current_psi < 0:
                self.pivot_left(theta - abs(current_psi))
            elif current_psi > 0:
                self.pivot_left(curretn_psi + theta)

        distance = (dx*dx + dy*dy)**0.5
        #ADD update travel log~!

        return distance


            

    def open_gripper(self):
        self.interfaces.open_gripper()

    def close_gripper(self):
        self.interfaces.close_gripper()

    def check_email(self):
        self.interfaces.check_email()
    
    def email(self):
        self.interfaces.email()
