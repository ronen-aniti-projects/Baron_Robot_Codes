

def normalize_angle(angle_degrees):
    """
    Map [0, 360) to [-180, 180)
    """
    return ((angle_degrees + 180) % 360) - 180

def heading_error(theta_goal, theta_start):
    """
    This returns a signed shortest-angle difference from start
    heading to goal heading, normalized to [-180, 180)
    """
    raw = theta_goal - theta_start 
    return ((raw + 180) % 360) - 180  

def meters2feet(meters):
    return 3.28084 * meters 

def feet2meters(feet):
    return 0.3048 * feet 

