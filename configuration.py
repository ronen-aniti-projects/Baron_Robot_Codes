import numpy as np 
from helpers import feet2meters 

class Configuration:

    def __init__(self):
        
        # Navigation
        self.start_pose = [0.,0.,0.]
        self.construction_pose = [0., feet2meters(8), 0.]
        self.construction_xmin = feet2meters(0)
        self.construction_xmax = feet2meters(4)
        self.construction_ymin = feet2meters(6)
        self.construction_ymax = feet2meters(10)
        self.pivot_tolerance = 1 # degrees
        
        # Pins
        self.left_encoder_pin = 12
        self.right_encoder_pin = 7
        self.trig_pin = 16
        self.echo_pin = 18
        self.gripper_pin = 36
        self.motors_left_forward = 31 
        self.motors_left_reverse = 33
        self.motors_right_reverse = 35
        self.motors_right_forward = 37 
        
        # Geometry
        self.wheel_diameter = 0.063 # meters
        self.wheel_circumference = self.wheel_diameter * np.pi
        self.ticks_per_revolution = 20

        # PWM settings
        self.gripper_frequency = 50 # Hz
        self.gripper_min_duty = 5 
        self.gripper_max_duty = 10 
        self.drive_motor_frequency = 50 # Hz
        
        # Image processing
        self.angle_to_pixel_ratio = 0.061 
        self.camera_res = (1640, 1232)
        self.red_mask_1_low = np.array([0, 100, 100])
        self.red_mask_1_high = np.array([10, 255, 255])
        self.red_mask_2_low = np.array([170, 100, 100])
        self.red_mask_2_high = np.array([179, 255, 255])
        self.green_mask_low = np.array([35, 60, 40])
        self.green_mask_high = np.array([85, 255, 255])
        self.blue_mask_low = np.array([100, 150,  50])
        self.blue_mask_high = np.array([140, 255, 255])
        self.bb_thresh = 140
        self.image_width = 640
        self.image_height = 480 
        self.contour_area_thresh = 20
        self.pixel_cutoff = 90
        self.pixel_error_cutoff = 20

        # IMU
        self.baud_rate = 115200
        self.usb = '/dev/ttyUSB0'



