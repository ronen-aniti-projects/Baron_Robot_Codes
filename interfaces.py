import RPi.GPIO as gpio
from picamera2 import Picamera2, Preview
from libcamera import Transform
import time 
import serial 
from helpers import normalize_angle
import cv2
import matplotlib.pyplot as plt

import imaplib
import email
import os
from datetime import datetime
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

class Interfaces:
    def __init__(self, config):
        self.config = config
        self.init_gpio()
        self.gripper = self.init_gripper()
        self.camera = self.init_camera()
        self.motors_lf, self.motors_lr, self.motors_rf, self.motors_rr = self.init_motors()
        self.imu = self.init_imu()
    
    def check_email(self):
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login('raniti.enpm701@gmail.com','nliu mchf ukzu hesx') 
        mail.list()
        count = 0

        while count < 60:
            try:
                print("try")
                mail.select("inbox")
                result, data = mail.search(None, '(UNSEEN FROM "mitchels@umd.edu")') # "mitchels@umd.edu / raniti@umd.edu"
                print(result)
                print(len(data))
                ids = data[0]
                id_list = ids.split()
                latest_email_id = id_list[-1]
                result, data = mail.fetch(latest_email_id, "(RFC822)")
                if data is None:
                    print("Waiting...")
                if data is not None:
                    print("Process initiated!")
                    return
            except IndexError:
                time.sleep(2)
                if count < 59:
                    count = count + 1
                    continue 
                else: 
                    print("Gameover")
                    count = 60
    
    def email(self):
        pic_time = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{pic_time}.jpg"
        self.camera.switch_mode_and_capture_file(
            self.camera.create_still_configuration(main={"size": (1280, 720)}),
            filename
        )

        # Email information
        smtpUser = 'raniti.enpm701@gmail.com'
        smtpPass = 'nliu mchf ukzu hesx'

        # Destination email information
        toAdd = ['ENPM809TS19@gmail.com', 'raniti@umd.edu']
        fromAdd = smtpUser
        subject = 'Image recorded at ' + pic_time 
        msg = MIMEMultipart()
        msg['Subject'] = subject 
        msg['From'] = fromAdd 
        msg['To'] = ",".join(toAdd)
        msg.preamble = "Image recorded at " + pic_time 

        # Email text
        body = MIMEText("Image recorded at " + pic_time)
        msg.attach(body)

        # Attach image
        fp = open(pic_time + '.jpg', 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        # Send email
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo() 
        s.login(smtpUser, smtpPass)
        s.sendmail(fromAdd, toAdd, msg.as_string())
        print("Email delivered")

    
    def read_imu(self):
        #self.imu.reset_input_buffer()
        while True:
            try:
                self.imu.write(b'R')
                raw = self.imu.readline()
                if not raw.endswith(b'\n'):
                    raise ValueError("Incomplete frame")
                heading_string = raw.decode('ascii').strip()
                heading = float(heading_string)
                return normalize_angle(heading)
            except ValueError:
                time.sleep(0.005)
                continue

    def init_gpio(self):
        """
        Initializes the GPIO pins.
        """
        print("Setting the GPIO pins")
        # Set the pin nmbering mode
        gpio.setmode(gpio.BOARD)
        
        # Set the drive motor pins 
        gpio.setup(self.config.motors_right_forward, gpio.OUT)
        gpio.output(self.config.motors_right_forward, False)

        gpio.setup(self.config.motors_right_reverse, gpio.OUT)
        gpio.output(self.config.motors_right_reverse, False)   

        gpio.setup(self.config.motors_left_forward, gpio.OUT)
        gpio.output(self.config.motors_left_forward, False)

        gpio.setup(self.config.motors_left_reverse, gpio.OUT)
        gpio.output(self.config.motors_left_reverse, False)

        # Set the encoder pins
        gpio.setup(self.config.right_encoder_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.setup(self.config.left_encoder_pin, gpio.IN, pull_up_down=gpio.PUD_UP)
        
        # Set the gripper pin
        gpio.setup(self.config.gripper_pin, gpio.OUT)

    def init_gripper(self):
        """
        Initializes and returns the gripper PWM interface.
        """
        print(f"Initializing the gripper PWM interface.")
        gripper_pwm = gpio.PWM(self.config.gripper_pin, self.config.gripper_frequency)
        gripper_pwm.start(0)
        return gripper_pwm

    def init_camera(self):
        """
        Initializes and returns the interface for the camera.
        """
        print(f"Initializing the camera interface.")
        cam = Picamera2()
        video_config = cam.create_video_configuration(
        main={"size": self.config.camera_res, "format": "RGB888"},
        transform=Transform(vflip=1, hflip=1)
        )
        cam.configure(video_config)
        cam.start()
        time.sleep(2)

        return cam

    def capture_array(self):
        """
        Returns a pre-processed HSV array for image masking
        """
        print("Capturing smooth hsv image")
        bgr = self.camera.capture_array("main")
        bgr = cv2.resize(
            bgr, 
            dsize=(self.config.image_width, self.config.image_height), interpolation=cv2.INTER_AREA
        )
        H, W, D = bgr.shape 
        #N = 75
        bgr[:int(0.35*H),:,:] = 0 # top portion black out
        #bgr[-N,:,:] = 0 # bottom portion black out
        blurred = cv2.GaussianBlur(bgr, (3,3), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        return hsv 

    def init_motors(self):
        """
        Initializes and returns drive motor PWM interfaces
        """
        print("Initializing the drive motor PWM interfaces")
        left_motors_forward_pwm = gpio.PWM(self.config.motors_left_forward, self.config.drive_motor_frequency)
        left_motors_forward_pwm.start(0)

        left_motors_reverse_pwm = gpio.PWM(self.config.motors_left_reverse, self.config.drive_motor_frequency)
        left_motors_reverse_pwm.start(0)

        right_motors_forward_pwm = gpio.PWM(self.config.motors_right_forward, self.config.drive_motor_frequency)
        right_motors_forward_pwm.start(0)
        
        right_motors_reverse_pwm = gpio.PWM(self.config.motors_right_reverse, self.config.drive_motor_frequency)
        right_motors_reverse_pwm.start(0)
        
        return left_motors_forward_pwm, left_motors_reverse_pwm, right_motors_forward_pwm, right_motors_reverse_pwm

    def stop_motors(self):
        for pwm in [self.motors_lf, self.motors_lr, self.motors_rf, self.motors_rr]:
            pwm.ChangeDutyCycle(0)
        gpio.output(self.config.motors_left_forward, gpio.LOW)
        gpio.output(self.config.motors_left_reverse, gpio.LOW)
        gpio.output(self.config.motors_right_forward, gpio.LOW)
        gpio.output(self.config.motors_right_reverse, gpio.LOW)

    def init_imu(self):
        """
        Initializes and returns an IMU interface
        """
        print(f"Establishing serial communication with IMU")
        imu = serial.Serial(self.config.usb, self.config.baud_rate, timeout=1)
        time.sleep(2)
        imu.reset_input_buffer()
        return imu

    def open_gripper(self):
        self.gripper.ChangeDutyCycle(self.config.gripper_max_duty)
        time.sleep(2)
        self.gripper.ChangeDutyCycle(0)
    
    def close_gripper(self):
        self.gripper.ChangeDutyCycle(self.config.gripper_min_duty)
        time.sleep(2)
    
    def turn_off_gpio(self):
        gpio.output(self.config.motors_left_forward, False)
        gpio.output(self.config.motors_left_reverse, False)
        gpio.output(self.config.motors_right_forward, False)
        gpio.output(self.config.motors_right_reverse, False)
        gpio.cleanup()
        
