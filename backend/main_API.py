from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
from typing import List
import cv2

from StickerDetector import StickerDetector
from ColorMapper import ColorMapper
from cube_validator import CubeStateValidator
import kociemba
from fastapi.middleware.cors import CORSMiddleware # enables Cross-Origin resource sharing in FASTAPI which is essentail to UNITY 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = r"C:\Users\evana\Documents\cs100project\final-project-elin107-ahuss043-clope375-arash031\backend\yolv8Model\content\runs\detect\train3\weights\best.pt"
detector = StickerDetector(MODEL_PATH)
color_mapper = ColorMapper()

# Receives 6 cube faces phots from FAstapi
@app.post("/upload-photos")
async def upload_photos(files: list[UploadFile] = File(...)):
    # see what is being printed
    print(f"Received {len(files)} files:")
    for f in files:
        print(f.filename, f.content_type)

    if len(files) != 6:
        raise HTTPException(status_code=400, detail="You must upload exactly 6 images.")
    
    face_strings = []
    
    for i, file in enumerate(files):
        # read uploaded files into np array
        # used AI to help, didn't know how to save a file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name
            
        # load image with OpenCV
        image = cv2.imread(temp_path)
        if image is None:
            raise HTTPException(status_code=400, detail="image could not be read")
        
        # run stickerDetector class 
        stickers = detector.detectAndCrop(image)
        if len(stickers) != 9:
            return JSONResponse({
                "status": "error",
                "reason": "detected fewer than 9 stickers",
                "detected": len(stickers)
            }, status_code=500)
    
        
        # run colorMapper classs
        try:
            side_string = color_mapper.extract_color(stickers)
        except:
            raise HTTPException(status_code=500, detail="Color extraction failed on image")
        
        face_strings.append(side_string)
    
    #combine all 6 sides into one facelt string
    cubeString = "".join(face_strings)
    
    print("Cube String before validation: ", cubeString)

    #function to visualize and debug code
    def print_cube_3x3(cube_string_54: str):
        if len(cube_string_54) != 54:
            raise ValueError("Cube string must be exactly 54 characters long.")

        # Break into 6 faces
        faces = [cube_string_54[i:i+9] for i in range(0, 54, 9)]
        face_names = ["U", "R", "F", "D", "L", "B"]

        for idx, face in enumerate(faces):
            print(f"{face_names[idx]} face:")
            # Print as 3x3
            for i in range(0, 9, 3):
                print(" ".join(face[i:i+3]))
            print()  # empty line between faces

    print_cube_3x3(cubeString)

    def reorder_faces_by_center(cube_string: str) -> str:
        # Split into 6 faces of 9 stickers
        faces = [cube_string[i:i+9] for i in range(0, 54, 9)]
        
        # Determine center color of each face
        centers = [face[4] for face in faces]
        
        # Target center colors for URFDLB order
        target_order = ["W", "R", "G", "Y", "O", "B"]
        
        # Map each target face to the index in faces
        face_map = []
        for color in target_order:
            if color not in centers:
                raise ValueError(f"Center color {color} not found in cube_string centers: {centers}")
            face_index = centers.index(color)
            face_map.append(face_index)
        
        # Reorder faces
        reordered_faces = [faces[i] for i in face_map]
        
        # Combine into a single string
        return "".join(reordered_faces)

    cubeString = reorder_faces_by_center(cubeString)
    print("Cube String after reordering to URFDLB:", cubeString)

    # test for valid state
    validator = CubeStateValidator(cubeString)
    isValid, result = validator.validate()
    
    if not isValid:
        raise HTTPException(status_code=400, detail=result)
    
    try:
        solution = kociemba.solve(result)
    except:
        raise HTTPException(status_code=500, detail="Solver failed")
    
    return JSONResponse({
        "status": "success",
        "cube": result,
        "solution": solution
    })