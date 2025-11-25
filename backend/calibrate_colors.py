# calibrate_cube_colors.py
import cv2
import numpy as np
from skimage import color as skcolor
from StickerDetector import StickerDetector

# Path to your YOLO model
MODEL_PATH = r"C:\Users\evana\Documents\cs100project\final-project-elin107-ahuss043-clope375-arash031\backend\yolv8Model\content\runs\detect\train3\weights\best.pt"  # adjust as needed

# Initialize detector
detector = StickerDetector(MODEL_PATH, conf=0.5)

# Number of faces to calibrate
NUM_FACES = 6

# Initialize dictionary to hold mean LAB for each face
face_colors_lab = {}

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Cannot open webcam")

print("Calibration started. Press 'c' to capture each face in order.")

for face_idx in range(NUM_FACES):
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # Display live feed
        cv2.putText(frame, f"Face {face_idx+1}/{NUM_FACES} - Press 'c' to capture",
                    (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        cv2.imshow("Calibration", frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('c'):
            # Capture this frame
            cropped_stickers = detector.detectAndCrop(frame)
            if len(cropped_stickers) != 9:
                print(f"Detected {len(cropped_stickers)} stickers, need 9. Retake face {face_idx+1}.")
                continue

            # Compute mean LAB per sticker
            lab_list = []
            for roi in cropped_stickers:
                avg_bgr = np.mean(roi, axis=(0,1))
                avg_rgb = avg_bgr[::-1] / 255.0  # BGR to RGB
                avg_lab = skcolor.rgb2lab([[avg_rgb]])[0][0]
                lab_list.append(avg_lab)

            face_colors_lab[f"Face_{face_idx+1}"] = lab_list
            print(f"Captured face {face_idx+1}")
            break

# Release webcam
cap.release()
cv2.destroyAllWindows()

# Compute LAB colors per color (assuming each face has a dominant color)
# Simple approach: take first sticker as representative
LAB_COLORS_CALIBRATED = {}
for i, (face, labs) in enumerate(face_colors_lab.items()):
    color_label = ["W","Y","R","O","G","B"][i]  # assign color order manually
    # average over the 9 stickers
    avg_lab = np.mean(labs, axis=0)
    LAB_COLORS_CALIBRATED[color_label] = avg_lab

print("\nCalibrated LAB_COLORS dictionary:\n")
print("LAB_COLORS = {")
for k,v in LAB_COLORS_CALIBRATED.items():
    print(f"    '{k}': np.array({v.tolist()}),")
print("}")
