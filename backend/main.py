import cv2
from StickerDetector import StickerDetector
from ColorMapper import ColorMapper

def main():
    modelPath = "yolv8Model/content/runs/detect/train3/weights/best.pt"
    imagePath = "images/IMG_0066.jpg"
    
    detector = StickerDetector(modelPath)
    colorMapper = ColorMapper()
    
    frame = cv2.imread(imagePath)
    if frame is None:
        print("Error: Could not read image")
        return
    
    croppedStickers = detector.detectAndCrop(frame)
    print(f"Detected {len(croppedStickers)} stickers")
    
    if len(croppedStickers) != 9:
        print("Error: Expected 9 stickers for once face")
        return
    
    try:
        sideString = colorMapper.extract_color(croppedStickers)
    except Exception as e:
        print(f"Error while extracting colors: {e}")
        return
    
    print(f"Detected side string: {sideString}")
    
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()