from abc import ABC, abstractmethod
from ultralytics import YOLO
import numpy as np
from typing import List

class IStickerDetector(ABC):
    
    @abstractmethod
    def detectAndCrop(self, frame: np.ndarray) -> List[np.ndarray]:
        pass


class StickerDetector(IStickerDetector):
    
    def __init__(self, modelPath: str, conf: float = 0.10):
        # constructor for StickerDetector
        # parameters: 
        #   modelPath (str): path to yolov8 model
        #   conf (float): confidence threshold for showing detection
    
        self.model = YOLO(modelPath)
        self.conf = conf
       
    def detectAndCrop(self, frame) -> list:
        results = self.model.predict(source=frame, conf=self.conf, verbose=False)
        boxes = results[0].boxes

        # gets the coordinates for the center piece boxes
        box_centers = []
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            box_centers.append((box, cx, cy))

        # sort by y coordinate to roughly assign rows
        box_centers.sort(key=lambda b: b[2])  # sort by center y

        # cluster into rows with 3 stickers per row
        rows = [box_centers[i*3:(i+1)*3] for i in range(3)]

        # sort each row by x coordinate (left -> right)
        sorted_boxes = []
        for row in rows:
            row.sort(key=lambda b: b[1])  # sort by center x
            sorted_boxes.extend([b[0] for b in row])

        croppedStickers = []
        # apply the border reduction so we have the coordinate of the sticker roi
        for box in sorted_boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            margin = 5
            x1 = max(0, x1 + margin)
            y1 = max(0, y1 + margin)
            x2 = min(frame.shape[1], x2 - margin)
            y2 = min(frame.shape[0], y2 - margin)
            roi = frame[y1:y2, x1:x2]
            if roi.size > 0:
                croppedStickers.append(roi) # if exists, append

        return croppedStickers
