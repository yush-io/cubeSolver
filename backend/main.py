import cv2
# uncomment when StickerDetector class is made
# from StickerDetector import StickerDetector 
from ColorMapper import ColorMapper

# detector = StickerDetector(r"C:\Users\evana\Documents\cs100project\final-project-elin107-ahuss043-clope375-arash031\backend\yolv8Model\content\runs\detect\train3\weights\best.pt")
colorMap = ColorMapper()

# replace with FastAPI image input later
image_path = "images/IMG_0066.jpg"

# load the image
frame = cv2.imread(image_path)
if frame is None:
    print(f"Error: Could not read image")
    exit(1)

# cropped_stickers = detector.detect_and_crop(frame)

#if len(cropped_stickers) != 9:
 #   print(f"Error: Expected 9 stickers")
 #   exit(1)

# side_string = colorMap.extract_color(cropped_stickers)

# print(f"Detected side string: {side_string}")

