import cv2
import os
from StickerDetector import StickerDetector

# Path to your YOLOv8 model
MODEL_PATH = r"C:\Users\evana\Documents\cs100project\final-project-elin107-ahuss043-clope375-arash031\backend\yolv8Model\content\runs\detect\train3\weights\best.pt"

# Path to your test images (update this folder path)
IMAGES_FOLDER = r"C:\Users\evana\Documents\cs100project\final-project-elin107-ahuss043-clope375-arash031\backend\test_images"

# Initialize the detector
detector = StickerDetector(MODEL_PATH)

# Collect all PNG images in the folder
image_files = sorted([f for f in os.listdir(IMAGES_FOLDER) if f.lower().endswith(".png")])

if len(image_files) != 6:
    print(f"Warning: Expected 6 images, found {len(image_files)}")

for idx, image_file in enumerate(image_files):
    image_path = os.path.join(IMAGES_FOLDER, image_file)
    image = cv2.imread(image_path)

    if image is None:
        print(f"Failed to read image: {image_file}")
        continue

    cropped_stickers = detector.detectAndCrop(image)

    print(f"Image {idx+1} ({image_file}): Detected {len(cropped_stickers)} stickers")

