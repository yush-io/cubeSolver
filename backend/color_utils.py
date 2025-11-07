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

# Extract the dominant color from a bounding box region
# frame: original BGR image (from webcame)
# box: YOLO bounding box object
# Returns: str: color label
def extract_color_from_bbox(frame, box):
    # get bounding box coordinates
    coords = yolo_box.xyxy[0]
    x1 = int(coords[0])
    y1 = int(coords[1])
    x2 = int(coords[2])
    y2 = int(coords[3])

    # shrink the box
    # margins avoid edges that can resut from glare/shadows
    margin = 5
    x1 = max(0, x1 + margin)
    y1 = max(0, y1 + margin)
    x2 = min(frame.shape[1], x2 - margin)
    y2 = min(frame.shape[0], y2 - margin)

    # extract region with margin
    regionOfInterest = frame[y1:y2, x1:x2]

    # makes sure we have a valid box that is not pixelless
    if regionOfInterest.size == 0:
        return None
    
    #gets average color of all pixels within the region
    avg_bgr = np.mean(regionOfInterest, axis=(0,1))

    # Converst from BGR to RGB
    # ::-1 revereses and normalize to 0-1
    avg_rgb = avg_bgr[::-1] / 255.0

    # convert RGB to LAB
    avg_lab = skcolor.rgb2lab([[avg_rgb]])[0][0]

    # return the closest reference color
    return nearest_color_lab(avg_lab)
