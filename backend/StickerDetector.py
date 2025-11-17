from abc import ABC, abstractmethod
from ultralytics import YOLO
import numpy as np
from typing import List

class IStickerDetector(ABC):
    
    @abstractmethod
    def detectAndCrop(self, frame: np.ndarray) -> List[np.ndarray]:
        pass


class StickerDetector(IStickerDetector):
    
    def __init__(self, modelPath: str, conf: float = 0.5):
        # constructor for StickerDetector
        # parameters: 
        #   modelPath (str): path to yolov8 model
        #   conf (float): confidence threshold for showing detection
    
        self.model = YOLO(modelPath)
        self.conf = conf
       
    def detectAndCrop(self, frame) -> List[np.ndarray]:
        # detects the stickers and crops the region from the frame
        # parameters: 
        #   frame: np.ndarray (BGR image from cam)
        # return:
        #   list of np.ndarray: cropped sticker images 
    
        results = self.model.predict(source = frame, conf = self.conf, verbose = False) # detection info
        boxes = results[0].boxes # extract every bounding box
        
        tempList = [] # list to hold ((y1, x1), box) tupes
        for box in boxes:
            #extract top-left coord of every box
            x1 = int(box.xyxy[0][0])
            y1 = int(box.xyxy[0][1])
            tempList.append(((y1, x1), box))
        
        tempList.sort() # left to right, top to bottom
        
        sortedBoxes = [item[1] for item in tempList] # gets rid of the coordinates in list
        
        # reverse each row after sorting because mirror image
        row1 = sortedBoxes[0:3][::-1]
        row2 = sortedBoxes[3:6][::-1]
        row3 = sortedBoxes[6:9][::-1]
        sortedBoxes = row1 + row2 + row3
        
        croppedStickers = [] # list to hold cropped sticker images
        
        for box in sortedBoxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0]) # get all coords of box
            
            margin = 5 # margin to crop potential black edges
            x1 = max(0, x1 + margin)
            y1 = max(0, y1 + margin)
            x2 = min(frame.shape[1], x2 - margin)
            y2 = min(frame.shape[0], y2 - margin)
            
            regionOfInterest = frame[y1:y2, x1:x2] # crops the sticker region and assigns to roi
            
            if regionOfInterest.size > 0:
                croppedStickers.append(regionOfInterest) # if non-empty add to list
        
        return croppedStickers