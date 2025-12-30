import cv2
import numpy as np
import requests # New dependency
import time

# --- SETTINGS ---
# Use 'shot.jpg' instead of 'video' for better stability
url = url = "http://10.144.9.124:8080/shot.jpg"
width, height = 150, 150
click_x, click_y = 100, 100

def get_frame_from_phone(url):
    try:
        # Pull the raw image from the phone
        img_resp = requests.get(url, timeout=5)
        # Convert raw bytes to a NumPy array (the format OpenCV likes)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        frame = cv2.imdecode(img_arr, -1)
        # Resize to keep the math fast
        return cv2.resize(frame, (640, 480))
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

# --- INITIALIZATION ---
print("Connecting to phone...")
back_frame = None
while back_frame is None:
    back_frame = get_frame_from_phone(url)
    if back_frame is None:
        print("Retrying connection...")
        time.sleep(1)

back_gray = cv2.cvtColor(back_frame, cv2.COLOR_BGR2GRAY)
back_gray = cv2.GaussianBlur(back_gray, (21, 21), 0)

# --- MAIN LOOP ---
while True:
    frame = get_frame_from_phone(url)
    if frame is None: continue # Skip this loop if the network flickered

    # ... Your existing motion detection logic starts here ...
    # (Gray conversion, diff, thresh, ROI slice, etc.)