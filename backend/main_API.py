from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
from typing import List
import cv2

from StickerDetector import StickerDetector
from ColorMapper import ColorMapper
from cube_validator import CubeStateValidator
import kociemba

app = FastAPI()

MODEL_PATH = "/Users/aayushr./Desktop/CS Projects/cubeSolver/final-project-elin107-ahuss043-clope375-arash031/backend/yolv8Model/content/runs/detect/train3/weights/best.pt"
detector = StickerDetector(MODEL_PATH)
color_mapper = ColorMapper()

# Receives 6 cube faces phots from FAstapi
@app.post("/upload-photos")
async def upload_photos(files: list[UploadFile] = File(...)):
    if len(files) != 6:
        raise HTTPException(status_code=400, detail="You must upload exactly 6 images.")
    face_strings = []
    
    for i, file in enumerate(files):
        # read uploaded files into np array
        # used AI to help, didn't know how to save a file
        with tempfile.NameTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name
            
        image = cv2.imread(temp_path)
        if image is None:
            raise HTTPException(status_code=400, detail="image could not be read")
        
        stickers = detector.detectAndCrop(image)
        
        if len(stickers) != 9:
            raise HTTPException(status_code=500, detail="Color extraction failed on image")
        
        try:
            sideString = color_mapper.extract_color(stickers)
        except:
            raise HTTPException(status_code=500, detail="Color extraction failed on image")
        
        faceStrings.append(sideString)
        
    cubeString = "".join(faceStrings)
    
    validator = CubeStateValidator(cubeString)
    isValid, result = validator.validate()
    
    if not isValid:
        raise HTTPException(status_code=400, detail=result)
    
    try:
        solution = kociemba.solve(result)
    except:
        raise HTTPException(status_code=500, detail="Solver failed")
    
    return JSONReponse({
        "status:" "success",
        "cube:" result,
        "solution": solution
    })