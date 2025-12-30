"""
Docstring for detect.webcam_model
"""
import os
import time
import winsound
import cv2
from ultralytics import YOLO
from src.log import UTILITY

# 1. Load your model (Works with best.pt or best.onnx)
# Path relative to webcam_model.py
model_path = os.path.abspath("src/best.pt")
print("Loading model from:", model_path)

model = YOLO(model_path)

# 2. Initialize Webcam (0 is us ually the default built-in camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Scanning for Green Headset... Press 'q' to stop.")

while True:
    # Capture frame-by-frame
    success, frame = cap.read()
    if not success:
        break

    # 3. Run Inference
    # stream=True uses a generator which is much faster for video
    # rect=True prevents the cropping issues we fixed earlier
    results = model.predict(source=frame, stream=True, rect=True, conf=0.10)

    for r in results:
        img_counter = 0
        top_conf = 0
        # 4. Logic Hook: Do something if the object is found
        if len(r.boxes) > 0:
            # Get the highest confidence score found in this frame
            top_conf = r.boxes.conf.max().item()
            print(f"I see something! Max Confidence: {top_conf:.2f}")
            frequency = 2500  # Set Frequency in Hertz (must be in range 37 through 32,767)
            duration = 1000   # Set Duration in milliseconds (1000 ms = 1 second)

            winsound.Beep(frequency, duration)
            img_name = f"opencv_frame_{img_counter}.png"
            # Save the frame to the file
            cv2.imwrite(img_name, frame)
            print(f"{img_name} written!")
            img_counter += 1
        else:
            print("Nothing detected...")

        # 5. Visualize the detections on the live frame
        annotated_frame = r.plot()
        UTILITY.log_data("Geeen Headset", top_conf)

    # Display the resulting frame
    cv2.imshow("Real-Time AI Detection", annotated_frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()