import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Define the "Tripwire" area (A rectangle in the middle of the screen)
# [y_start:y_end, x_start:x_end]

tripwire_y = (100, 300)
tripwire_x = (200, 400)

while True:
    success, frame = cap.read()
    if not success: break

# 1. Convert to HSV (Easier for computers to detect color)

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# 2. Define a color range (This example is for a bright RED object)
# You might need to adjust these numbers for your specific object!

lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

# 3. Create a mask (Black and White image where Red is White)
mask = cv2.inRange(hsv, lower_red, upper_red)
# 4. Check the Tripwire Area
# We look at the pixels ONLY inside our defined box

roi = mask[tripwire_y[0]:tripwire_y[1], tripwire_x[0]:tripwire_x[1]]
pixel_count = cv2.countNonZero(roi)

# 5. Visual Feedback
# Draw the tripwire box




