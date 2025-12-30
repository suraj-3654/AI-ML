import cv2
import winsound
import time


# --- 1. SETTINGS & GLOBAL VARIABLES ---
cap = cv2.VideoCapture(0)
width, height = 150, 150  # Fixed size of the box
click_x, click_y = 100, 100 # Initial position
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000   # Set Duration To 1000 ms == 1 second

# --- 2. THE MOUSE CALLBACK ---
def select_point(event, x, y, flags, param):
    global click_x, click_y
    if event == cv2.EVENT_LBUTTONDOWN:
        click_x, click_y = x, y
        print(f"Target moved to: {x}, {y}")

# Setup the window and link the mouse function
cv2.namedWindow("Click to Move Zone")
cv2.setMouseCallback("Click to Move Zone", select_point)

# --- 3. CAPTURE INITIAL BACKGROUND ---
ret, back_frame = cap.read()
back_gray = cv2.cvtColor(back_frame, cv2.COLOR_BGR2GRAY)
back_gray = cv2.GaussianBlur(back_gray, (21, 21), 0)

while True:
    ret, frame = cap.read()
    if not ret: break

    # A. PREPARE CURRENT FRAME
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # B. THE MATH: Find the difference
    diff = cv2.absdiff(back_gray, gray)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]

    # C. DYNAMIC ROI (Crucial: These must be inside the loop!)
    roi_x_end = click_x + width
    roi_y_end = click_y + height

    # D. THE SLICE (Wait! Safety check to prevent IndexError)
    # We ensure we don't slice past the camera edge
    roi_area = thresh[click_y : roi_y_end, click_x : roi_x_end]

    # E. LOGIC: Is there motion?
    change_count = cv2.countNonZero(roi_area)
    box_color = (0, 255, 0) # Green by default

    if change_count > 1000: # If enough pixels are white
        box_color = (0, 0, 255) # Change to Red
        winsound.Beep(frequency, duration)
        cv2.putText(frame, "!!! ALERT !!!", (click_x, click_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # F. DRAW EVERYTHING
    cv2.rectangle(frame, (click_x, click_y), (roi_x_end, roi_y_end), box_color, 2)
    
    cv2.imshow("Click to Move Zone", frame)
    cv2.imshow("ROI Mask (What the computer counts)", roi_area)

    # --- 4. KEYBOARD CONTROLS (Only one waitKey) ---
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        back_gray = gray
        print("Background updated to current scene.")

cap.release()
cv2.destroyAllWindows()