# test_stickerdetector.py

import numpy as np
import pytest

import StickerDetector as sd_mod  # module where StickerDetector is defined


class FakeBox:
    def __init__(self, x1, y1, x2, y2):
        # mimic yolo box.xyxy[0] behavior
        self.xyxy = np.array([[x1, y1, x2, y2]])


class FakeResult:
    def __init__(self, boxes):
        self.boxes = boxes


class FakeYOLO:
    def __init__(self, modelPath):
        # ignore modelPath, no real loading
        self.modelPath = modelPath

    def predict(self, source, conf=0.1, verbose=False):
        # create 9 boxes arranged in 3 rows x 3 cols
        boxes = []
        size = 30
        margin = 5
        idx = 0
        for row in range(3):
            for col in range(3):
                x1 = col * size
                y1 = row * size
                x2 = x1 + size
                y2 = y1 + size
                boxes.append(FakeBox(x1, y1, x2, y2))
                idx += 1
        return [FakeResult(boxes)]


def test_detect_and_crop_returns_9_rois(monkeypatch):
    # patch YOLO in the module to our fake
    monkeypatch.setattr(sd_mod, "YOLO", FakeYOLO)

    detector = sd_mod.StickerDetector("dummy/path.pt")

    # make a fake frame (just needs correct shape)
    frame_h, frame_w = 100, 100
    frame = np.zeros((frame_h, frame_w, 3), dtype=np.uint8)

    rois = detector.detectAndCrop(frame)

    # should have 9 cropped sticker images
    assert len(rois) == 9

    # each roi should be non-empty
    for roi in rois:
        assert roi.size > 0
        assert roi.ndim == 3  # h, w, channels
