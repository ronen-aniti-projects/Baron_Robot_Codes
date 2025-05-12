# Autonomous Block Collection Robot

## Logic 
- Mission Considerations:
    - Block sequence : R -> B -> G x3
    - Set boolean GRIPPER_FULL = FALSE at START
    - Set boolean TARGET_LOCK = TRUE 
    - Set boolean AVOIDANCE = FALSE
    - Set boolean HEADING_TO_GOAL = TRUE 
- While True:
    - Ask: Is HEADING_TO_GOAL = TRUE? 
        - If yes:
            - Move forward 1 ft.
            - Record IMU reading 
            - Update (x, y) and heading estimates 
            - Pivot again to goal 
            - Ask: Is (x, y) within goal bounding box? 
            - If yes: 
                - Open gripper 
                - Set HEADING_TO_GOAL = FALSE 
    - Ask: Is TARGET_LOCK = TRUE and GRIPPER_FULL = FALSE?
    - If yes:
        - Ask: Is there any other block in center tri-portion of image and has estimated distance smaller than 1 foot?
        - If yes:
            - Pivot 20 degrees right
            - Update heading estimate 
            - MOVE FORWARD 0.5 ft.
            - Pivot 20 degrees left
            - Update heading estimate
            - SET TARGET_LOCK = FALSE 
            - Continue
        - Record IMU reading 
        - Move forward 1 ft.
        - Record IMU reading 
        - Take the average of the before and after IMU readings
        - Update (x, y) and heading estimate
        - Take another picture
        - Ask: Is the target block within grasping distance?
        - If yes:
            - Close gripper 
            - SET GRIPPER_FULL = TRUE 
            - Take picture 
            - Email picture 
            - Pivot to the GOAL (x, y) map position
            - SET HEADING_TO_GOAL = TRUE
    - Take a picture
    - Ask: Is the target block in the picture (and is more than goal bounding box width away)?
    - If yes:
        - Estimate the pivot angle and direction
        - Execute PIVOT 
        - Record IMU reading 
        - UPDATE robot estimated heading 
        - Take another picture 
        - Ask: is the target block in the picture? 
        - If yes:
            - Estimate the pivot angle
            - Ask:
            - Is the pivot angle < 5 degrees?
            - If yes:
                - SET TARGET_LOCK = TRUE 
                - Continue
        - If no: 
            - Continue
    - If no:
        - Pivot 20 degrees right
        - Record IMU reading 
        - Update heading estimate





- While True:
    - Take picture
    - Ask: is target block within a 2 degree pivot left or right of center?
    - - If yes:
    - - - Move forward 1 ft. (using P control with encoder feedback)
    - - - Record IMU reading
    - - - Update x, y
    - - - Update heading 
    
    - Ask: is target block in picture? 
    - - If yes:
    - - - Estimate the pivot angle and direction
    - - - Pivot that amount and direction
    - - - Read the IMU
    - - - Update the heading of the robot state estimate 
    - - If no:
    - - - Pivot left by 20 degrees

