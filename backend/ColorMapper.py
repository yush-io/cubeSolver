import numpy as np
from skimage import color as skcolor
from scipy.spatial.distance import euclidean # using SciPy for clarity
from abc import ABC, abstractmethod


# Colors in LAB space
LAB_COLORS = {
    'W': np.array([93, -1, 10]),
    'Y': np.array([92, -14, 90]),
    'R': np.array([53, 80, 67]),
    'O': np.array([70, 24, 79]),
    'G': np.array([89, -74, 85]),
    'B': np.array([46, 6, -46])
}



# BGR values for OpenCV not RGB different
BGR_COLORS = {
    'W': (208, 234, 236),
    'Y': (40, 236, 236),
    'R': (0, 0, 255),
    'O': (0, 165, 255),
    'G': (0, 255, 102),
    'B': (187, 110, 41)
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
        
        # small weight for A/B channels
        weight = np.array([1.0, 1.2, 1.2])

        # Starts a loop a iterate 
        for color_name, ref_lab_color in LAB_COLORS.items():
            # calculate the euclidean distance (uses SciPy library gives the distance between 2 points in 3d space because 
            # LAB has 3 axies)
            difference_distance = np.linalg.norm((lab_color - ref_lab_color) * weight)

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
            h, w = roi.shape[:2]

            # Crop central region to avoid edges/reflections
            margin_h, margin_w = int(h * 0.2), int(w * 0.2)
            roi_center = roi[margin_h:h-margin_h, margin_w:w-margin_w]

            # Mask out extremely bright/dark pixels
            mask = np.all((roi_center > 20) & (roi_center < 235), axis=2)
            if np.sum(mask) == 0:
                roi_masked = roi_center
            else:
                roi_masked = roi_center[mask]

            # Average BGR -> RGB
            avg_bgr = np.mean(roi_masked, axis=0) if roi_masked.ndim == 2 else np.mean(roi_masked, axis=0)
            avg_rgb = avg_bgr[::-1] / 255.0

            # Convert to LAB and clamp L
            avg_lab = skcolor.rgb2lab([[avg_rgb]])[0][0]
            avg_lab[0] = np.clip(avg_lab[0], 20, 90)  # clamp L to reduce white misclassification

            color_label = self.nearest_color_calculator(avg_lab)
            side_colors += color_label

        return side_colors

