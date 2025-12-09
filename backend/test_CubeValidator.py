import pytest

from cube_validator import CubeStateValidator


def test_init_rejects_wrong_length():
    # string must be exactly 54 chars long
    with pytest.raises(ValueError):
        CubeStateValidator("W" * 53)

    with pytest.raises(ValueError):
        CubeStateValidator("W" * 55)


def test_init_rejects_unknown_color():
    # includes 'X' which is not mapped
    bad = "W" * 53 + "X"
    with pytest.raises(ValueError):
        CubeStateValidator(bad)


def test_validate_solved_cube_is_valid():
    # W = U, R = R, G = F, Y = D, O = L, B = B
    raw = (
        "W" * 9 +  # U
        "R" * 9 +  # R
        "G" * 9 +  # F
        "Y" * 9 +  # D
        "O" * 9 +  # L
        "B" * 9    # B
    )

    validator = CubeStateValidator(raw)
    is_valid, state = validator.validate()

    assert is_valid is True

    # mapped kociemba state should be URFDLB in that order
    expected = (
        "U" * 9 +
        "R" * 9 +
        "F" * 9 +
        "D" * 9 +
        "L" * 9 +
        "B" * 9
    )
    assert state == expected


def test_validate_rejects_wrong_color_counts():
    # 10 W's and 8 R's (rest okay) -> fail checkCenters_Counts
    raw = (
        "W" * 10 +  # too many W
        "R" * 8 +
        "G" * 9 +
        "Y" * 9 +
        "O" * 9 +
        "B" * 9
    )
    validator = CubeStateValidator(raw)
    is_valid, msg = validator.validate()

    assert is_valid is False
    assert "Colors do not appear exactly 9 times each" in msg or "Invalid cube" in msg


def test_getPermutation_parity():
    # simple parity check:
    # identity permutation -> even (0)
    # simple swap -> odd (1)
    from cube_validator import CubeStateValidator as CV

    assert CV.getPermutation([0, 1, 2, 3]) == 0
    assert CV.getPermutation([1, 0, 2, 3]) == 1
    assert CV.getPermutation([2, 1, 0, 3]) == 1 