import numpy as np
import typing 
import time 
from helpers import normalize_angle
import cv2 

class Vision:
    def __init__(self, config, interfaces):
        self.interfaces = interfaces
        self.config = config

    def estimate_distance(self, bb_w, bb_h): 
        estimated_Z_inches = 3.7243 + 1113.5561 / bb_h
        estimated_Z_meters = 0.0254 * estimated_Z_inches
        return estimated_Z_meters

    def estimate_pivot(self, cx_bb, cy_bb):
        cx_image = self.config.image_width // 2 
        cy_image = self.config.image_width // 2
        horizontal_error = cx_bb - cx_image
        pivot_angle = abs(horizontal_error) * self.config.angle_to_pixel_ratio
        direction = "right" if horizontal_error > 0 else "left"
        print(f"estimated pivot angle {pivot_angle: .2f} {direction}")
        return pivot_angle, direction, horizontal_error

    def scan(self, block_color="green"):
        hsv = self.interfaces.capture_array()
        if block_color == "green":
            mask = cv2.inRange(
                hsv, 
                self.config.green_mask_low,
                self.config.green_mask_high
            )
        elif block_color == "red":
            mask1 = cv2.inRange(
                hsv, 
                self.config.red_mask_1_low,
                self.config.red_mask_1_high
            )
            mask2 = cv2.inRange(
                hsv,
                self.config.red_mask_2_low,
                self.config.red_mask_2_high
            )
            mask = cv2.bitwise_or(mask1, mask2)
        elif block_color == "blue":
            mask = cv2.inRange(
                hsv,
                self.config.blue_mask_low,
                self.config.blue_mask_high
            )
            
        contours, _ = cv2.findContours(
            mask, 
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        if not contours:
            return False, False, None, None, None
        
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) < self.config.contour_area_thresh:
            return False, False, None, None, None
        x, y, w, h = cv2.boundingRect(largest)
        cx_bb = x + w // 2 
        cy_bb = y + h // 2 


        
        # debug visuals:
        ############
        W = 640
        H = 480
        cx_image = W // 2
        cy_image = H // 2
        rgb_annotated = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
       
        cv2.drawMarker(
            rgb_annotated, 
            (cx_image, cy_image), 
            (255, 0, 0),
            markerType=cv2.MARKER_CROSS,
            markerSize=20,
            thickness=1 
        )
        cv2.drawMarker(
            rgb_annotated, 
            (cx_bb, cy_bb),
            (0, 0, 255),
            markerType=cv2.MARKER_CROSS,
            markerSize=20,
            thickness=1
        )
        cv2.arrowedLine(
            rgb_annotated, 
            (cx_image, cy_image),
            (cx_bb, cy_image),
            (255, 255, 0),
            thickness=1,
            tipLength=0.1
        )
        ################
        # Display
        cv2.imshow("Blurred with BB", rgb_annotated)
        cv2.waitKey(0)
        # Display
        cv2.imshow("Mask", mask)
        cv2.waitKey(0)
        


        # Change this later
        # This is the condition for the block being close enough
        if cy_bb > 0.85 * self.config.image_height:
            print("Grip now")
            return True, True, None, None, cy_bb

        pivot_angle, direction, pixel_error = self.estimate_pivot(cx_bb, cy_bb)
        return True, False, pivot_angle, direction, cy_bb

