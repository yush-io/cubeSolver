# A simple webcam based sticker detection script using YOLOv8 just to test inital color
# mapper functions and adjustments for LAB Colors
from ultralytics import YOLO
import cv2
import time
from ColorMapper import ColorMapper
from ColorMapper import BGR_COLORS

# loads yolo model from file path
model = YOLO("Users\evana\Documents\cs100project\final-project-elin107-ahuss043-clope375-arash031\backend\yolv8Model\content\runs\detect\train3\weights\best.pt")

cap = cv2.VideoCapture(0) # connection to webcam

if not cap.isOpened():
    print("webcam did not open correctly")
    exit(1)

print("webcam worked correctly")

prev_time = 0 #timestamp of prev frame to compute fps

# loop for real-time detection
while True:
    ret, frame = cap.read() # reads 1 frame
    if not ret:
        print("frame grab did not work")
        break

    # run YOLO inference on current frame
    # conf = 0.5, makes so only considers predictions with c>= 50%
    # returns a copy of the frame with bounding boxes 
    results = model.predict(source=frame, conf=0.5, verbose=False)
    annotated = results[0].plot()

    # exxtract colors from each detected sticker
    detected_boxes = results[0].boxes
    colors_detected = []

    # loop through each detected sticker
    for box in detected_boxes:
        sticker_color = extract_color(box)

        if sticker_color is not None:
            colors_detected.append(sticker_color)

            # draw the color label on top
            coords = box.xyxy[0]
            x = int(coords[0])
            y = int(coords[1])

            # put colored rectangle as background
            label_color = BGR_COLORS[sticker_color]
            cv2.rectangle(annotated, (x, y -25), (x + 40, y), label_color, -1)

            # put letter on top
            cv2.putText(annotated, sticker_color, (x + 5, y- 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0),2)

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