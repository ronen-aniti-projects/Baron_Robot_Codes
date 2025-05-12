

def normalize_angle(angle_degrees):
    """
    Map [0, 360) to [-180, 180)
    """
    return ((angle_degrees + 180) % 360) - 180


def meters2feet(meters):
    return 3.28084 * meters 

def feet2meters(feet):
    return 0.3048 * feet 

