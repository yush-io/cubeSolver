import itertools # used for generating combinations of rotations, makes my life easier
from collections import Counter # helps counter lists faster
from typing import List, Tuple, Optional # for tuple type hinting

#Constants: Kociemba Facelet Index Tables
# Corner indices: (U, R, F), (U, F, L), (U, L, B), (U, B, R), (D, F, R), (D, L, F), (D, B, L), (D, R, B)
CORNER_FACELETS = [
    (8, 9, 20), (6, 18, 38), (0, 36, 47), (2, 45, 11),
    (29, 26, 15), (27, 44, 24), (33, 53, 42), (35, 17, 51)
]
CORNER_COLOR_NAMES = [
    ("U", "R", "F"), ("U", "F", "L"), ("U", "L", "B"), ("U", "B", "R"),
    ("D", "F", "R"), ("D", "L", "F"), ("D", "B", "L"), ("D", "R", "B"),
]

# Edge indices: UR, UF, UL, UB, DR, DF, DL, DB, FR, FL, BL, BR
EDGE_FACELETS = [
    (5, 10), (7, 19), (3, 37), (1, 46),     # UR, UF, UL, UB
    (32, 16), (28, 25), (30, 43), (34, 52), # DR, DF, DL, DB
    (23, 12), (21, 41), (50, 39), (48, 14)  # FR, FL, BL, BR
]
EDGE_COLOR_NAMES = [
    ("U", "R"), ("U", "F"), ("U", "L"), ("U", "B"),
    ("D", "R"), ("D", "F"), ("D", "L"), ("D", "B"),
    ("F", "R"), ("F", "L"), ("B", "L"), ("B", "R"),
]

class CubeStateValidator:
    # make basic check for 54 char long string
    # convert to kociemba format
    def __init__(self, cube_string_54: str):
        mapping = {
            "W": "U",
            "R": "R",
            "O": "L",
            "G": "F",
            "B": "B",
            "Y": "D"
        }   
        if len(cube_string_54) != 54:
            raise ValueError("Cube string must be exactly 54 characters long.")
        
        self.raw = cube_string_54.upper()

    
        try:
            self.state = "".join([mapping[ch] for ch in self.raw])
        except KeyError as e:
            raise ValueError(f"Color char {e} found in string but not in color_map.")
        
    # returns either
    # (true, fixed_state) -> cube is valid or can be fixed
    # (false, error_message) -> is invalid and can not be fixed
    def validate(self) -> Tuple[bool, str]:
        # check color counts and centers
        try:
            self.checkCenters_Counts()
        except ValueError as e:
            return False, f"Invalid cube: {e}"

        # check corners/edges, attempt to catch only rotational issues
        try:
            cornerPermutation, cornerOrient = self.extractCorners()
            edgePermutation, edgeOrient = self.extractEdges()

            # check parity and orientation sums
            self.validateCornerOrient(cornerOrient)
            self.validateEdgeOrient(edgeOrient)
            self.validateParity(cornerPermutation, edgePermutation)
            return True, self.state
       

    # Internal Validation Logic
    # Checks valid cube colors
    # each color appears 9 times
    # centers are unique
    def checkCenters_Counts(self):
        validColors = {"U", "R", "F", "D", "L", "B"}
        count = Counter(self.state)

        # check for unexpected color
        for i in count.keys():
            if i not in validColors:
                raise ValueError("Unexpected color found in cube state.")

        # check for missing colors or incorrect count
        for i in validColors:
            count = count.get(i,0) # Counter library function to count iterations
            if count != 9:
                raise ValueError("Colors do not appear exactly 9 times each")
        
        # check for unique center colors
        centerI = [4, 13, 22, 31, 40, 49]
        center = []
        for i in centerI:
            centerColor = self.state[i]
            center.append(centerColor)
        if len(set(center)) != 6:
            raise ValueError("Center colors are not unique.")


    def extractCorners(self):
        cornerIndices = []
        cronerOrient = []
        canonicalTriplets = [tuple(c) for c in CORNER_COLOR_NAMES]

        for facelets in CORNER_FACELETS:
            currentColors = tuple(self.state[i] for i in facelets)
            found = False

            # compare agianst all canonical corner pieces
            for i, refColors in enumerate(canonicalTriplets):
                # all possible orientations for corner
                possibleOrient = [
                    refColors, 
                    (refColors[1], refColors[2], refColors[0]),
                    (refColors[2], refColors[0], refColors[1])
                ]

                # check if current matches any of the possible orientations
                for orientation, rotatedColors in enumerate(possibleOrient):
                    if currentColors == rotatedColors:
                        cornerIndices.append(i)
                        cronerOrient.append(orientation)
                        found = True
                        break

                if found:
                    break
            if not found:
                raise ValueError(f"Invalid corner piece found: {currentColors}")
        return cornerIndices, cronerOrient

    def validateCornerOrient(self, orients):
        if sum(orients) % 3 != 0:
            raise ValueError("Corner orientation invalid.")

    def extractEdges(self):
        edgeIndices = []
        edgeOrient = []
        canonicalPairs = [tuple(c) for c in EDGE_COLOR_NAMES]

        for facelets in EDGE_FACELETS:
            currentColors = tuple(self.state[i] for i in facelets)
            found = False
            for i, refColors in enumerate(canonicalPairs):
                if currentColors == refColors:
                    edgeIndices.append(i)
                    edgeOrient.append(0)
                    found = True
                elif currentColors == (refColors[1], refColors[0]):
                    edgeIndices.append(i)
                    edgeOrient.append(1)
                    found = True

                if found: 
                    break
            if not found:
                raise ValueError(f"Invalid edge piece found: {currentColors}")
        return edgeIndices, edgeOrient

    def validateEdgeOrient(self, orients):
        if sum(orients) % 2 != 0:
            raise ValueError("Edge orientation invalid.")

    # calculates the parity of a permutation by counting inversions
    @staticmethod
    def getPermutation(perm):
        inversions = 0
        n = len(perm)
        for i in range(n):
            for j in range(i + 1, n):
                if perm[i] > perm[j]:
                    inversions += 1
        return inversions % 2

    # check that corner and edge permutations have matching parity
    def validateParity(self, cornerPerm, edgePerm):
        cornerParity = self.getPermutation(cornerPerm)
        edgeParity = self.getPermutation(edgePerm)
        if cornerParity != edgeParity:
            raise ValueError("Parity Error.")