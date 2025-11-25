# live_color_test_fixed.py
from ultralytics import YOLO
import cv2
import time
from ColorMapper import ColorMapper, BGR_COLORS
import numpy as np
from skimage import color as skcolor

# Load YOLO model (use raw string for Windows paths)
model = YOLO(r"C:\Users\evana\Documents\cs100project\final-project-elin107-ahuss043-clope375-arash031\backend\yolv8Model\content\runs\detect\train3\weights\best.pt")

# Initialize color mapper
color_mapper = ColorMapper()

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Webcam did not open correctly")
    exit(1)

print("Webcam opened correctly")

prev_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Frame grab failed")
        break

    results = model.predict(source=frame, conf=0.5, verbose=False)
    annotated = results[0].plot()  # frame with bounding boxes

    colors_detected = []

    for box in results[0].boxes:
        # Crop sticker region
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        margin = 5
        x1, y1 = max(0, x1 + margin), max(0, y1 + margin)
        x2, y2 = min(frame.shape[1], x2 - margin), min(frame.shape[0], y2 - margin)
        roi = frame[y1:y2, x1:x2]

        if roi.size == 0:
            continue

        # Average BGR -> RGB -> LAB
        avg_bgr = np.mean(roi, axis=(0, 1))
        avg_rgb = avg_bgr[::-1] / 255.0  # BGR -> RGB normalized
        avg_lab = skcolor.rgb2lab([[avg_rgb]])[0][0]  # flatten to 1D (3,)

        # Get nearest color
        color_label = color_mapper.nearest_color_calculator(avg_lab)
        colors_detected.append(color_label)

        # Draw rectangle and label
        label_color = BGR_COLORS[color_label]
        cv2.rectangle(annotated, (x1, y1 - 25), (x1 + 40, y1), label_color, -1)
        cv2.putText(annotated, color_label, (x1 + 5, y1 - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # FPS and number of detections
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    prev_time = curr_time

    cv2.putText(annotated, f"FPS: {int(fps)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(annotated, f"Detections: {len(colors_detected)}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # Show live feed
    cv2.imshow("Rubik's Cube Color Detector", annotated)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("Exiting...")
