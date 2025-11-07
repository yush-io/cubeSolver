from ultralytics import YOLO
import cv2
import time
from color_utils import extract_color_from_box
from color_config import COLOR_BGR

model = YOLO(r"C:\Users\evana\Documents\cs100project\final-project-elin107-ahuss043-clope375-arash031\backend\yolv8Model\content\runs\detect\train3\weights\best.pt")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("webcam did not open correctly")
    exit(1)

print("webcam worked correctly")

prev_time = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("frame grab did not work")
        break

    # YOLO inference (single frame)
    results = model.predict(source=frame, conf=0.5, verbose=False)
    annotated = results[0].plot()

    # exxtract colors from each detected sticker
    detected_boxes = results[0].boxes
    colors_detected = []

    for box in detected_boxes:
        sticker_color = extract_color_from_box(frame, box)

        if sticker_color is not None:
            colors_detected.append(sticker_color)

            # draw the color label on top
            coords = box.xyxy[0]
            x = int(coords[0])
            y = int(coords[1])

            # put colored rectangle as background
            label_color = COLOR_BGR[sticker_color]
            cv2.rectangle(annotated, (x, y -25), (x + 40, y), label_color, -1)

            # put letter on top
            cv2.putText(annotated, sticker_color, (x + 5, y- 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0),2)

    #fps and box count
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time) if prev_time else 0
    prev_time = curr_time
    num_boxes = len(results[0].boxes)

    cv2.putText(annotated, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(annotated, f"detections: {num_boxes}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Rubik's Cube Detector (press 'q' to quit)", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print("exiting...")