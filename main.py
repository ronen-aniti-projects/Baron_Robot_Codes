# Imports
from configuration import Configuration
from interfaces import Interfaces
from robot import Robot 
from travel import Travel 
from moves import Moves 
import RPi.GPIO as gpio
import time
from helpers import meters2feet, feet2meters
from vision import Vision
# Configuration Settings:

def main3():
    # Get a feel for the error in actions:
    try:
        config = Configuration()
        interfaces = Interfaces(config)
        travel_log = Travel(interfaces, config)
        moves = Moves(config, interfaces)
        vision = Vision(config, interfaces)
        robot = Robot(config, interfaces, moves, travel_log, vision)
        robot.open_gripper()
        block_aquired = False 
        #robot.pivot_right(20)
        for _ in range(1):
            #robot.pivot_right(90)
            robot.forward(feet2meters(11))
            robot.reverse(feet2meters(11))
            #robot.pivot_left(90)
            #robot.forward(feet2meters(1))
            robot.travel_log.show_trajectory()

    except KeyboardInterrupt:
        print("Off")
        gpio.output(31, False)
        gpio.output(33, False)
        gpio.output(35, False)
        gpio.output(37, False)
        gpio.cleanup()

# For Tuesday:
def main2():

    try:
        block_colors = ["red", "green", "blue"] * 3
        config = Configuration()
        interfaces = Interfaces(config)
        travel_log = Travel(interfaces, config)
        moves = Moves(config, interfaces)
        vision = Vision(config, interfaces)
        robot = Robot(config, interfaces, moves, travel_log, vision)
        robot.open_gripper()
        block_aquired = False 
        #robot.check_email()
        block_color = block_colors.pop(0) 
        print(f"Heading to this color: {block_color}") # Erase after today
        while True:
            print("Robot Pose {robot.travel_log.current_pose}")
            robot.travel_log.show_trajectory()
            # When the robot has gripped the target block:
            # -> It pivots to the goal
            # -> It moves forward towards the goal
            # IDAEA: After the first drop off, flag the entire goal box as NEAR_GOAL. Then, if NEAR_GOAL, 
            # and facing NEAR GOAL, drop the block off 
            # -> It ungrips the block
            # -> It reverses
            # -> It turns around (180 deg)
            if block_aquired:
                distance_to_goal = robot.pivot_to_goal()
                
                #TODO: Add logic so that the robot actually inches towards the goal. When the robot estimates it's near the goal and facing the goal and on at least its second delivery, then it should drive to wherever it sees another object. If the robot senses its within 4 inches of a wall, it should stop, back up
                #step_size = distance_to_goal / 10

                robot.forward(distance_to_goal)
                robot.open_gripper()
                block_aquired = False
                robot.reverse(feet2meters(0.5))
                for _ in range(3):
                    robot.pivot_right(60)
                robot.close_gripper()
                robot.open_gripper()
                if len(block_colors) == 0:
                    print("Tuesday mission complete")
                    break
                block_color = block_colors.pop(0)

            # When the robot does NOT have a block gripped:
            # -> It takes a picture
            # -> It checks if there are any target blocks in the frame
            # -> If there are, then it pivots towards one
            #    and moves towards it.
            # -> If there aren't, then it pivots by 30 degrees to the right
            # -> IDEA: Check for all colors. If pivot angle of any two are within 10 degrees of each other, don't approach either
            ret, grip_now, angle_degrees, direction, cy = robot.scan(block_color=block_color)
            if ret:

                

                if grip_now: 
                    robot.close_gripper()
                    block_aquired = True
                    robot.email() 
                    continue

                if direction == "right":
                    robot.pivot_right(angle_degrees)

                elif direction == "left":
                    robot.pivot_left(angle_degrees)
                print(cy)
                if cy > 0.8 * robot.config.image_height:
                    robot.forward(feet2meters(0.1)) 
                else:
                    robot.forward(feet2meters(.75))

            else:
                robot.pivot_right(30)


    except KeyboardInterrupt:
        print("Off")
        gpio.output(31, False)
        gpio.output(33, False)
        gpio.output(35, False)
        gpio.output(37, False)
        gpio.cleanup()


def main1():

    try:
        # Constants
        config = Configuration()
        # Hardware controls
        interfaces = Interfaces(config)
        # Test IMU
        for _ in range(10):
            print(interfaces.read_imu())
        
        # Instance of test
        start_pose = [0., 0., 0.]
        construction_pose = [0., 2.25, 0]
        
        # Init travel log for arena
        travel_log = Travel(interfaces, start_pose, construction_pose)
        # Handle driving and motion
        moves = Moves(config, interfaces)
        #vision = Vision(config, interfaces)
        # Build a robot instance
        robot = Robot(config, interfaces, moves, travel_log)
        
        robot.open_gripper()
        #robot.forward(100)

        for _ in range(5):
            robot.pivot_right(30)
            time.sleep(1)
            print(travel_log.current_pose)
            print(travel_log.pose_history)
            print(travel_log.action_history)
            robot.pivot_left(30)
            time.sleep(1)
            print(travel_log.current_pose)
            print(travel_log.pose_history)
            print(travel_log.action_history)
    
    except KeyboardInterrupt:
        print("Off")
        gpio.output(31, False)
        gpio.output(33, False)
        gpio.output(35, False)
        gpio.output(37, False)
        gpio.cleanup()


if __name__ == "__main__":
    main2()
    #main3() 


