import numpy as np
from skimage import color as skcolor
from scipy.spatial.distance import euclidean # using SciPy for clarity
from abc import ABC, abstractmethod


# Colors in LAB space
LAB_COLORS = {
    'W': np.array([100, 0, 0]),
    'Y': np.array([70, -15, 85]),
    'R': np.array([30, 80, 67]),
    'O': np.array([50, 50, 78]),
    'G': np.array([70, -64, 49]),
    'B': np.array([30, 79, -90])
}

# BGR values for OpenCV not RGB different
BGR_COLORS = {
    'W': (255, 255, 255),
    'Y': (0, 255, 255),
    'R': (0, 0, 255),
    'O': (0, 165, 255),
    'G': (0, 255, 0),
    'B': (255, 0, 0)
}

# Interface for a color mapper
class IColorMapper(ABC):
    @abstractmethod 
    # return the nearest color label for a single LAB color
    def nearest_color_calculator(self, lab_color: np.ndarray) -> str:
        pass

    @abstractmethod
    # return a string of 9 color labels for one side of the cube
    def extract_color(self, sticker_boxes: list) -> str:
        pass



class ColorMapper(IColorMapper):
    # find nearest reference color using Euclidean distance in LAB space
    # lab_color: numpy array [L, A, B]
    # returns str: color label
    def nearest_color_calculator(self, lab_color: np.ndarray) -> str:
        min_distance = float('inf')
        nearest = None
        
        # Starts a loop a iterate 
        for color_name, ref_lab_color in LAB_COLORS.items():
            # calculate the euclidean distance (uses SciPy library gives the distance between 2 points in 3d space because 
            # LAB has 3 axies)
            difference_distance = euclidean(lab_color, ref_lab_color)

            if difference_distance < min_distance:
                min_distance = difference_distance
                nearest = color_name
        
        return nearest

    # Extract the dominant color from a bounding box region
    # frame: original BGR image (from webcame)
    # box: YOLO bounding box object
    # Returns: str: color label
    def extract_color(self, cropped_stickers: list) -> str:
        # makes sure we have a valid box that is not pixelless
        if len(cropped_stickers) != 9:
            raise ValueError("Must provide exactly 9 cropped sticker images")

        side_colors = ""

        for roi in cropped_stickers:
            avg_bgr = np.mean(roi, axis=(0,1))
            avg_rgb = avg_bgr[::-1] / 255.0 # BGR to RGB
            avg_lab = skcolor.rgb2lab([[avg_rgb]])[0][0] # convert to LAB using skcolor library
            color_label = self.nearest_color_calculator(avg_lab) # returns 1 string
            side_colors += color_label # append to the string

        return side_colors
    
