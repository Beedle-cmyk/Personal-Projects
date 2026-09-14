import cv2
from ultralytics import YOLO
from src.config import MODEL_FOR_PREDICTIONS, MIN_CONF, MAX_CONF, LIVE_FEED

model = YOLO(MODEL_FOR_PREDICTIONS)

capture = cv2.VideoCapture(LIVE_FEED)

if not capture.isOpened():
    print("Error: Could not open video stream.")
    exit()

print("Press 'q' to quit")

while True:
    ret, frame = capture.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    results = model(frame, stream=True)

    for result in results:
        if result.boxes is None or len(result.boxes) == 0:
            continue

        confidences = result.boxes.conf.cpu().numpy()
        valid_detection = any(MIN_CONF <= conf <= MAX_CONF for conf in confidences)

        if valid_detection:
            annotated_frame = result.plot()
            cv2.imshow("YOLO Live Segmentation", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()