import numpy as np
import typing 
import time 
import matplotlib.pyplot as plt 
from helpers import feet2meters, meters2feet 

class Travel:
    def __init__(self, 
        interfaces,
        config
        ):
        self.current_pose = config.start_pose.copy()
        self.construction_pose = config.construction_pose.copy()
        self.start_time = time.time()
        self.pose_history = [[time.time() - self.start_time, config.start_pose.copy()]]
        self.action_history = []
        self.interfaces = interfaces
        print(f"Pose at initialization: {self.current_pose}")

    @property
    def x(self):
        return self.current_pose[0]

    @property 
    def y(self):
        return self.current_pose[1] 
        
    @property
    def psi(self):
        return self.current_pose[2] 

    @property
    def is_near_goal(self):
        return (0 <=self.current_pose[0] <= feet2meters(4)) and (feet2meters(6) <= self.current_pose[1] <= feet2meters(10)) 

    def update_log_forward(self, average_heading, distance_meters):
        new_x = self.current_pose[0] + distance_meters * np.sin(np.deg2rad(average_heading))
        new_y = self.current_pose[1] + distance_meters * np.cos(np.deg2rad(average_heading))
        new_heading = self.interfaces.read_imu()
        self.current_pose = [
            new_x, new_y, new_heading
        ]
        self.pose_history.append([time.time() - self.start_time, self.current_pose.copy()])
        self.action_history.append(f"forward {distance_meters: .2f}")

    def update_log_reverse(self, average_heading, distance_meters): 
        new_x = self.current_pose[0] - distance_meters * np.sin(np.deg2rad(average_heading))
        new_y = self.current_pose[1] - distance_meters * np.cos(np.deg2rad(average_heading))
        new_heading = self.interfaces.read_imu()
        self.current_pose = [
            new_x, new_y, new_heading
        ]
        self.pose_history.append([time.time() - self.start_time, self.current_pose.copy()])
        self.action_history.append(f"reverse {distance_meters: .2f}")

    def update_log_pulse_left(self, new_heading):
        self.current_pose[2] = new_heading 
        self.action_history.append(f"pulse left")
        self.pose_history.append([time.time-self.start_time, self.current_pose.copy()])
    
    def update_log_pulse_right(self, new_heading):
        self.current_pose[2] = new_heading 
        self.action_history.append(f"pulse right")
        self.pose_history.append([time.time-self.start_time, self.current_pose.copy()])


    def update_log_pivot_left(self, new_heading, angle_command):
        self.current_pose[2] = new_heading
        self.action_history.append(f"pivot left {angle_command: .2f}")
        self.pose_history.append([time.time() - self.start_time, self.current_pose.copy()])

    def update_log_pivot_right(self, new_heading, angle_command):
        self.current_pose[2] = new_heading        
        self.action_history.append(f"pivot right {angle_command: .2f}")
        self.pose_history.append([time.time() - self.start_time, self.current_pose.copy()])

    def update_log_pivot_to_goal(self, new_heading):
        self.current_pose[2] = new_heading 
        self.action_history.append(f"Pivot to goal. Facing: {new_heading}")
        self.pose_history.append([time.time() - self.start_time, self.current_pose.copy()])

    def show_trajectory(self):
        times, poses = zip(*self.pose_history)
        xs, ys, _ = zip(*poses)
        plt.plot(xs, ys, marker='o')
        plt.xlabel("X (m)")
        plt.ylabel("Y (m)")
        plt.title("Robot Trajectory")
        plt.show()
