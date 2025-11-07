import numpy as np
from skimage import color as skcolor
from color_config import REFERENCE_COLORS


# find nearest reference color using Euclidean distance in LAB space
# lab_color: numpy array [L, A, B]
# returns str: color label
def nearest_color_lab(lab_color):
    min_distance = float('inf')
    nearest = None
    
    for color_name, ref_lab in REFERENCE_COLORS.items():
        distance = np.linalg.norm(lab_color - ref_lab)
        if distance < min_distance:
            min_distance = distance
            nearest = color_name
    
    return nearest



    