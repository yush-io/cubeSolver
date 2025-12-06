import io
import numpy as np
import pytest
from fastapi.testclient import TestClient

import main_API


def make_fake_image_bytes():
    # tiny 10x10 bgr-ish array encoded as jpg
    import cv2

    img = np.zeros((10, 10, 3), dtype=np.uint8)
    img[:, :] = (0, 0, 255)  # blue-ish
    success, buf = cv2.imencode(".jpg", img)
    assert success
    return io.BytesIO(buf.tobytes())


def test_upload_photos_wrong_file_count():
    client = TestClient(main_API.app)

    # send only 1 file instead of 6
    files = {
        "files": ("face0.jpg", make_fake_image_bytes(), "image/jpeg")
    }

    response = client.post("/upload-photos", files=files)
    assert response.status_code == 400
    assert "You must upload exactly 6 images." in response.text


def test_upload_photos_happy_path(monkeypatch):
    client = TestClient(main_API.app)

    # fake detector
    class FakeDetector:
        def detectAndCrop(self, frame):
            # return 9 fake "roi" images per face
            rois = []
            for _ in range(9):
                rois.append(np.zeros((10, 10, 3), dtype=np.uint8))
            return rois

    # fake color mapper
    class FakeColorMapper:
        def roi_to_lab(self, roi):
            # return dummy lab
            return np.array([50.0, 0.0, 0.0])

        def nearest_color_calculator(self, lab):
            # always say 'W' for simplicity
            return "W"

        def identify_centers(self, centers):
            # pretend faces are scanned as: W, R, G, Y, O, B
            return ['W', 'R', 'G', 'Y', 'O', 'B']

    # fake cube validator
    class FakeValidator:
        def __init__(self, state):
            self.state = state

        def validate(self):
            # always valid, return some kociemba string
            return True, "URFDLB" * 9  # not real, just placeholder

    # fake solver
    class FakeSolver:
        def solve(self, state_string: str) -> str:
            return "R U R' U'"

    # patch globals in main_API module
    monkeypatch.setattr(main_API, "detector", FakeDetector())
    monkeypatch.setattr(main_API, "color_mapper", FakeColorMapper())
    monkeypatch.setattr(main_API, "CubeStateValidator", FakeValidator)
    monkeypatch.setattr(main_API, "solver", FakeSolver())

    # build 6 fake files
    files = []
    for i in range(6):
        files.append(
            ("files", (f"face{i}.jpg", make_fake_image_bytes(), "image/jpeg"))
        )

    response = client.post("/upload-photos", files=files)

    assert response.status_code == 200
    data = response.json()

    # should return formatted solution list
    assert "Solution" in data
    assert data["Solution"] == ["R", "U", "R'", "U'"]
