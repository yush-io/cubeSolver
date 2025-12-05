import numpy as np
import pytest

from ColorMapper import ColorMapper, LAB_COLORS


# helper: tiny fake roi with solid bgr color
def make_solid_bgr_roi(bgr, h=20, w=20):
    roi = np.zeros((h, w, 3), dtype=np.uint8)
    roi[:, :] = bgr  # broadcast color into entire image
    return roi


def test_nearest_color_calculator_exact_lab_match():
    # make sure if we feed in the exact lab color, it gives back the right letter
    mapper = ColorMapper()
    for label, lab in LAB_COLORS.items():
        result = mapper.nearest_color_calculator(lab)
        assert result == label, f"expected {label}, got {result}"


def test_roi_to_lab_basic_shape_and_range():
    # test that roi_to_lab returns a lab vector with sane values
    mapper = ColorMapper()

    # bright-ish blue-ish roi in BGR (blue channel high)
    roi = make_solid_bgr_roi(bgr=(255, 0, 0))

    lab = mapper.roi_to_lab(roi)

    # should be length 3
    assert lab.shape == (3,)
    # L should be clamped between 10 and 95
    assert 10 <= lab[0] <= 95
    # A/B don't have strict bounds, but should be finite numbers
    assert np.isfinite(lab[1])
    assert np.isfinite(lab[2])


def test_roi_to_lab_empty_roi_returns_zero():
    # if for some reason roi is empty, we expect [0,0,0]
    mapper = ColorMapper()
    empty_roi = np.zeros((0, 0, 3), dtype=np.uint8)
    lab = mapper.roi_to_lab(empty_roi)
    assert np.array_equal(lab, np.array([0, 0, 0]))


def test_identify_centers_perfect_match_order_preserved():
    # if we pass in the 6 reference lab colors in some random order,
    # identify_centers should label them correctly by position
    mapper = ColorMapper()

    # make a specific order (not same as dict order)
    order = ['R', 'W', 'B', 'G', 'Y', 'O']
    centers = [LAB_COLORS[c] for c in order]

    labels = mapper.identify_centers(centers)

    # we expect each index i to be labeled by the original color char
    assert labels == order  


def test_extract_color_calls_roi_to_lab_and_nearest_correctly(monkeypatch):
    # here we don't care about real image math, just that extract_color
    # loops through 9 stickers and builds the string in order

    mapper = ColorMapper()

    fake_rois = [np.zeros((10, 10, 3), dtype=np.uint8) for _ in range(9)]

    # fake lab sequence to map 9 stickers to known labels
    fake_labs = [
        LAB_COLORS['W'],
        LAB_COLORS['R'],
        LAB_COLORS['G'],
        LAB_COLORS['Y'],
        LAB_COLORS['O'],
        LAB_COLORS['B'],
        LAB_COLORS['W'],
        LAB_COLORS['R'],
        LAB_COLORS['G'],
    ]

    calls = {"idx": 0}

    def fake_roi_to_lab(roi):
        # return next fake lab value in sequence
        idx = calls["idx"]
        calls["idx"] += 1
        return fake_labs[idx]

    # patch roi_to_lab so we don't depend on real color math
    monkeypatch.setattr(mapper, "roi_to_lab", fake_roi_to_lab)

    side = mapper.extract_color(fake_rois)

    # expected string based on fake_labs
    assert side == "WRGYOBWRG"
