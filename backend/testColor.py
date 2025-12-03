import cv2
from StickerDetector import StickerDetector
from ColorMapper import ColorMapper

MODEL_PATH = r"C:\Users\evana\Documents\cs100project\final-project-elin107-ahuss043-clope375-arash031\backend\yolv8Model\content\runs\detect\train3\weights\best.pt"
detector = StickerDetector(MODEL_PATH)
color_mapper = ColorMapper()

image_files = [
    "WIN_20251125_00_11_43_Pro.jpg",
    "WIN_20251125_00_11_39_Pro.jpg",
    "WIN_20251125_00_11_37_Pro.jpg",
    "WIN_20251125_00_11_35_Pro.jpg",
    "WIN_20251125_00_11_32_Pro.jpg",
    "WIN_20251125_00_11_48_Pro.jpg"
]

for img_file in image_files:
    image = cv2.imread(img_file)
    stickers = detector.detectAndCrop(image)
    if len(stickers) != 9:
        print(f"{img_file}: Sticker extraction failed ({len(stickers)} stickers found)")
        continue
    color_string = color_mapper.extract_color(stickers)
    print(f"{img_file}: {color_string}")
