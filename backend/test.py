from ultralytics import YOLO
import cv2
import time

# loads yolo model from file path
model = YOLO("/Users/aayushr./Desktop/CS Projects/cubeSolver/final-project-elin107-ahuss043-clope375-arash031/backend/yolv8Model/content/runs/detect/train3/weights/best.pt")

cap = cv2.VideoCapture(0) # connection to webcam

if not cap.isOpened():
    print("webcam did not open correctly")
    exit(1)

print("webcam worked correctly")

prev_time = 0 #timestamp of prev frame to compute fps
while True:
    ret, frame = cap.read() # ret -> if frame grab worked, frame -> actual image
    if not ret:
        print("frame grab did not work")
        break

    # runs yolo inference on any image and keeps detections with >=50% confidence
    results = model.predict(source=frame, conf=0.5, verbose=False)
    annotated = results[0].plot() # annotated image

    #fps and box count
    curr_time = time.time()
    if prev_time == 0:
        fps = 0
    else:
        fps = 1 / (curr_time - prev_time)
    prev_time = curr_time # update time for next loop
    num_boxes = len(results[0].boxes) # counts number of detections

    cv2.putText(annotated, f"FPS: {int(fps)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(annotated, f"detections: {num_boxes}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Rubik's Cube Detector (press 'q' to quit)", annotated)

    # waits 1ms for key press and 0xFF for binary mask
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# disconnect webcam, close openCV window, exit message
cap.release()
cv2.destroyAllWindows()
print("exiting...")