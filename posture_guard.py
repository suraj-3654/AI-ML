import cv2
from ultralytics import YOLO
import winsound
import time

# 1. Load the Pose Model
model = YOLO('yolov8n-pose.pt') 

cap = cv2.VideoCapture(0)

# 2. State Variables
ideal_y = None  # This will hold your "Perfect Posture" height
tolerance = 60  # How many pixels you can drop before it alerts (adjust this)

print("--- POSTURE GUARD ---")
print("Step 1: Sit up straight.")
print("Step 2: Press 'S' to calibrate your ideal posture.")
print("Step 3: Press 'Q' to quit.")

while True:
    success, frame = cap.read()
    if not success: break

    results = model(frame, stream=True, verbose=False)

    for r in results:
        if r.keypoints and len(r.keypoints.xy[0]) > 0:
            # Extract Nose Y-coordinate
            nose_y = int(r.keypoints.xy[0][0][1])

            l_sh = r.keypoints[0][5]
            r_sh = r.keypoints[0][6]

            current_width = abs(l_sh[0] - r_sh[0]).item()



            
            # --- CALIBRATION LOGIC ---
            if ideal_y is not None:

                if current_width > (ideal)
                # If current nose is significantly LOWER than ideal
                if nose_y > (ideal_y + tolerance):
                    status = "SLOUCHING!"
                    frequency = 2500  # Set Frequency in Hertz (must be in range 37 through 32,767)
                    duration = 1000   # Set Duration in milliseconds (1000 ms = 1 second)

                    winsound.Beep(frequency, duration)
                    color = (0, 0, 255) # Red
                    # Trigger your UTILITY.log_data and Beep here
                else:
                    status = "Good Posture"
                    color = (0, 255, 0) # Green
                
                # Draw the benchmark line and status
                cv2.line(frame, (0, ideal_y + tolerance), (640, ideal_y + tolerance), (255, 255, 255), 1)
                cv2.putText(frame, status, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            else:
                cv2.putText(frame, "Press 'S' to Calibrate", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Plot the AI skeleton
        frame = r.plot()

    cv2.imshow("Posture Guard Pro", frame)

    # Keyboard Controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        ideal_y = nose_y
        print(f"✅ Calibrated! Your ideal nose level is: {ideal_y}")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()