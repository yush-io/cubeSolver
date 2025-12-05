from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import cv2
import os
import numpy as np

#custom files
from StickerDetector import StickerDetector
from ColorMapper import ColorMapper
from cube_validator import CubeStateValidator
from KociembaSolver import KociembaSolver
from fastapi.middleware.cors import CORSMiddleware

# create the api app
app = FastAPI()

# allowing unity to talk with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# folder to save uploaded images for debugging
UPLOAD_DEBUG_DIR = "debug_uploads"
os.makedirs(UPLOAD_DEBUG_DIR, exist_ok=True)

# path to yolo model
MODEL_PATH = "yolv8Model/content/runs/detect/train3/weights/best.pt"

# create objects used for detection, color mapping, and solving
detector = StickerDetector(MODEL_PATH)
color_mapper = ColorMapper()
solver = KociembaSolver()

# helper to try different image filters to help detection if it fails at first
def apply_filters(img, attempt):
    if attempt == 0: return img  # orginal image
    if attempt == 1: # high contrast
        return cv2.convertScaleAbs(img, alpha=1.5, beta=0) 
    if attempt == 2: # high brightness
        return cv2.convertScaleAbs(img, alpha=1.0, beta=50)
    if attempt == 3: # grayscale (simulated as BGR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    return img


# main api endpoint
# receives 6 images of the cube faces and returns solve moves string as JSON 
@app.post("/upload-photos")
async def upload_photos(files: list[UploadFile] = File(...)):
    """
    Main endpoint: receives 6 images, detects stickers via YOLO,
    identifies faces using Global Best Fit (random order supported),
    reorders to URFDLB, validates, and solves.
    """
    print(f"Received {len(files)} files")
    # must have exactly 6 faces
    if len(files) != 6:
        raise HTTPException(status_code=400, detail="You must upload exactly 6 images.")

    # will store lab colors for each face
    faces_lab: list[list[np.ndarray]] = []
    centers_lab: list[np.ndarray] = []

    # loop through all uploaded images
    for i, file in enumerate(files):
        # save image for debugging 
        contents = await file.read()
        debug_path = os.path.join(UPLOAD_DEBUG_DIR, f"face_{i}_photo.png")
        with open(debug_path, "wb") as f_out:
            f_out.write(contents)

        # decode image from bytes
        np_arr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        if image is None:
            raise HTTPException(status_code=400, detail=f"Image {i} could not be read")

        # try detection with multiple filters
        stickers = []
        for attempt in range(4):
            processed_img = apply_filters(image, attempt)
            current_stickers = detector.detectAndCrop(processed_img)
            
            print(f"Image {i} (Attempt {attempt}): Found {len(current_stickers)} stickers")
            
            # If we find > 9, take top 9 (assuming detector returns unsorted confidence, or just take first 9)
            if len(current_stickers) > 9:
                 current_stickers = current_stickers[:9]

            # success case
            if len(current_stickers) == 9:
                stickers = current_stickers
                # save filtered image that worked
                cv2.imwrite(f"{UPLOAD_DEBUG_DIR}/success_face_{i}.jpg", processed_img)
                break 
            
            # keep result of last attempt even if failed
            if attempt == 3:
                stickers = current_stickers

        # check if detection worked
        if len(stickers) != 9:
            print(f"Error: Expected 9 stickers, found {len(stickers)} on image {i}")
            return JSONResponse({
                "status": "error",
                "reason": "detected fewer than 9 stickers",
                "detected": len(stickers),
                "face_index": i,
            }, status_code=500)

        # convert each sticker roi to lab color
        sticker_labs = [color_mapper.roi_to_lab(roi) for roi in stickers]
        faces_lab.append(sticker_labs)
        
         # center sticker used for face mapping
        centers_lab.append(sticker_labs[4]) # Index 4 is center

    # determine which face is which using the 6 center tiles
    try:
        # This returns a list like ['R', 'W', 'B', 'G', 'Y', 'O'] based on best fit
        scan_order = color_mapper.identify_centers(centers_lab)
        print(f"Identified Scan Order: {scan_order}")
    except Exception as e:
        print(f"Center ID failed: {e}")
        raise HTTPException(status_code=500, detail="Could not identify cube face colors.")

    # label every sticker using nearest color match
    face_strings: list[str] = []
    
    for face_idx, sticker_labs in enumerate(faces_lab):
        side_str = ""
        expected_center = scan_order[face_idx]
        
        for i, lab in enumerate(sticker_labs):
            # force center sticker to match the global ID (face color)
            if i == 4:
                label = expected_center
            else:
                label = color_mapper.nearest_color_calculator(lab)
            side_str += label
        face_strings.append(side_str)

    # combine all faces into one string
    raw_cube_string = "".join(face_strings)
    print("Raw String:", raw_cube_string)

    # reorder faces to match kociemba solver format
    # order must be: up, right, front, down, left, back
    KOCIEMBA_ORDER = ['W', 'R', 'G', 'Y', 'O', 'B'] # U, R, F, D, L, B
    
    scanned_faces_dict = {}
    
    # map detected faces to their color
    for i, color_char in enumerate(scan_order):
        chunk = raw_cube_string[i*9 : (i+1)*9]
        scanned_faces_dict[color_char] = chunk
    
     # rebuild cube in the right order  
    final_ordered_faces = []
    for target in KOCIEMBA_ORDER:
        if target not in scanned_faces_dict:
            raise HTTPException(status_code=500, detail=f"Missing face color: {target}")
        final_ordered_faces.append(scanned_faces_dict[target])
        
    final_cube_string = "".join(final_ordered_faces)
    print("Final Kociemba String:", final_cube_string)

    # print the cube in a readable 3x3 format (debug only)
    def print_cube_3x3(cube_str):
        if len(cube_str) != 54: return
        names = ["U(W)", "R(R)", "F(G)", "D(Y)", "L(O)", "B(B)"]
        faces = [cube_str[i:i+9] for i in range(0, 54, 9)]
        for idx, face in enumerate(faces):
            print(f"Face {names[idx]}:")
            for r in range(0, 9, 3): print(" ".join(face[r:r+3]))
            print()
    print_cube_3x3(final_cube_string)

    # validate cube before solving
    validator = CubeStateValidator(final_cube_string)
    isValid, result = validator.validate()

    if not isValid:
        print(f"Validation Failed: {result}")
        raise HTTPException(status_code=400, detail=result)

    # get solution from kociemba
    try:
        solution = solver.solve(result)
        print(f"Solution: {solution}")
    except Exception as e:
        print("Solver error:", e)
        raise HTTPException(status_code=500, detail=str(e))

    # return solution as list for unity
    return JSONResponse({
        "Solution": solution.split()
    })