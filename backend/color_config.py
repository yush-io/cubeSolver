import numpy as np

# Colors in LAB space
REFERENCE_COLORS = {
    'W': np.array([100, 0, 0]),
    'Y': np.array([70, -15, 85]),
    'R': np.array([70, 80, 67]),
    'O': np.array([70, 50, 78]),
    'G': np.array([70, -64, 49]),
    'B': np.array([70, 79, -90])
}

# BGR values for OpenCV !!! not RGB
COLOR_BGR = {
    'W': (255, 255, 255),
    'Y': (0, 255, 255),
    'R': (0, 0, 255),
    'O': (0, 165, 255),
    'G': (0, 255, 0),
    'B': (255, 0, 0)
}