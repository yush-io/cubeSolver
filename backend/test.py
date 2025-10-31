from ultralytics import YOLO
import cv2
import time

model = YOLO("/home/csmajs/arash031/final-project-elin107-ahuss043-clope375-arash031/backend/yolv8Model/content/runs/detect/train3/weights/best.pt")

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