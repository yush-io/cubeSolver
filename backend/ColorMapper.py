import numpy as np
from skimage import color as skcolor
from abc import ABC, abstractmethod
from typing import List
from sklearn.cluster import KMeans


# reference LAB colors
LAB_COLORS = {
    'W': np.array([90.0,   1.6,  -3.0]),   # white
    'Y': np.array([78.0, -15.0,  35.0]),   # yellow
    'R': np.array([30.0,  42.0,  26.0]),   # red
    'O': np.array([54.0,  40.0,  31.0]),   # orange
    'G': np.array([58.0, -56.0,  25.0]),   # green
    'B': np.array([34.0,  14.0, -48.0])    # blue
}

class IColorMapper(ABC):
    @abstractmethod 
    def nearest_color_calculator(self, lab_color: np.ndarray) -> str:
        pass

    @abstractmethod
    def extract_color(self, sticker_boxes: list) -> str:
        pass
        
    @abstractmethod
    def identify_centers(self, centers: List[np.ndarray]) -> List[str]:
        pass

class ColorMapper(IColorMapper):
    # convert 1 sticker's ROI from BGR to the LAB color
    # uses K-means clustering to ignore glare
    def roi_to_lab(self, roi_bgr: np.ndarray) -> np.ndarray:
        h, w = roi_bgr.shape[:2]

        # removing 25% of the border and assigning that as center
        margin_h, margin_w = int(h * 0.25), int(w * 0.25)
        roi_center = roi_bgr[margin_h:h - margin_h, margin_w:w - margin_w]

        # flatten into pixels
        pixels = roi_center.reshape(-1, 3)
        if len(pixels) == 0: return np.array([0, 0, 0])

        # filters out extreme darkness/brightness
        # widen range to 10-250 to catch dark blues and bright yellows (gets mixed up with white sometimes)
        gray = 0.299 * pixels[:, 2] + 0.587 * pixels[:, 1] + 0.114 * pixels[:, 0]
        mask = (gray > 10) & (gray < 250)
        valid_pixels = pixels[mask]

        if len(valid_pixels) < 10:
            valid_pixels = pixels

        # usse K-Means to find the dominant color
        # point is to ignore glare/reflections/noise
        try:
            kmeans = KMeans(n_clusters=1, n_init=10)
            kmeans.fit(valid_pixels)
            dominant_bgr = kmeans.cluster_centers_[0]
        except:
            dominant_bgr = valid_pixels.mean(axis=0)

        # convert bgr -> rgb -> lab
        avg_rgb = dominant_bgr[::-1] / 255.0
        avg_lab = skcolor.rgb2lab(avg_rgb.reshape(1, 1, 3))[0, 0]

        # clamp L slightly to prevent impossibly bright values
        avg_lab[0] = np.clip(avg_lab[0], 10, 95)

        return avg_lab # [L, A, B]

    # find the neaerest reference color
    def nearest_color_calculator(self, lab_color: np.ndarray) -> str:
        min_distance = float('inf')
        nearest = None

        # WEIGHTS: [L, A, B]
        # We emphasize A/B (2.0) to distinguish colors.
        # We de-emphasize L (0.5) so glare doesn't turn colors like yellow into white.
        weight = np.array([0.5, 2.0, 2.0])

        for color_name, ref_lab_color in LAB_COLORS.items():
            diff = (lab_color - ref_lab_color) * weight # Using Euclidenan Distance to to find the closest match
            difference_distance = np.linalg.norm(diff)

            if difference_distance < min_distance:
                min_distance = difference_distance
                nearest = color_name

        return nearest

    # Matches the 6 detected centers against the known reference colors
    # Uses a global best fit algorithm to handle random scan orders
    def identify_centers(self, centers: List[np.ndarray]) -> List[str]:
        target_names = list(LAB_COLORS.keys()) # ['W', 'Y', 'R', 'O', 'G', 'B']
        
        # 1. Compute Distance Matrix (6 detected x 6 targets)
        distances = np.zeros((6, 6))
        for i, detected in enumerate(centers):
            for j, name in enumerate(target_names):
                ref = LAB_COLORS[name]
                # Same weighting logic as nearest_color_calculator
                diff = detected - ref
                weight = np.array([0.5, 2.0, 2.0]) 
                dist = np.linalg.norm(diff * weight)
                distances[i][j] = dist # each cell = how close the center color is to reference color

        assigned_labels = [None] * 6
        used_targets = set()
        
        print("\nIdentifying Centers (Global Best Fit)")
        
        # Loop 6 times to find the best remaining match in the grid
        for _ in range(6):
            min_dist = float('inf')
            best_file_idx = -1
            best_target_idx = -1
            
            for r in range(6):
                if assigned_labels[r] is not None: continue # File already assigned
                for c in range(6):
                    if c in used_targets: continue # Color already taken
                    
                    if distances[r][c] < min_dist:
                        min_dist = distances[r][c]
                        best_file_idx = r
                        best_target_idx = c
            
            # Lock the color in
            color_char = target_names[best_target_idx]
            assigned_labels[best_file_idx] = color_char
            used_targets.add(best_target_idx)
            print(f"File {best_file_idx} matches {color_char} (Dist: {min_dist:.2f})")
            
        return assigned_labels

    # strings the list of stickers as a string
    def extract_color(self, cropped_stickers: list) -> str:
        if len(cropped_stickers) != 9:
            raise ValueError("Must provide exactly 9 cropped sticker images")
        side_colors = ""
        for roi in cropped_stickers:
            avg_lab = self.roi_to_lab(roi)
            color_label = self.nearest_color_calculator(avg_lab)
            side_colors += color_label
        return side_colors