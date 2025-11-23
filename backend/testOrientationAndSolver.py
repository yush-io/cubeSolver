import kociemba
from cube_validator import CubeStateValidator

cube_colors = "YYWGWRGWBRYBWRBWOYOGYRGBRWOWWWBYYRRGBOOYORGGGBOOGBBYOR"

mapping = {
    "W": "U",
    "R": "R",
    "O": "L",
    "G": "F",
    "B": "B",
    "Y": "D"
}

cube_faces = "".join(mapping[c] for c in cube_colors)
val = CubeStateValidator(cube_faces)
is_valid, result = val.validate()

if is_valid:
    print(f"Cube is valid! Fixed state: {result}")
    print(kociemba.solve(result))
else:
    print(f"Cube is invalid: {result}")
