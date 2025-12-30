import cv2

cap = cv2.VideoCapture(0)

# 1. Take a 'Snapshot' of the empty room
ret, background_frame = cap.read()
# Convert to Gray and Blur it (to ignore tiny pixel jitters)
background_gray = cv2.cvtColor(background_frame, cv2.COLOR_BGR2GRAY)
background_gray = cv2.GaussianBlur(background_gray, (21, 21), 0)

while True:
    ret, current_frame = cap.read()
    if not ret: break

    # 2. Prepare the current frame
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.GaussianBlur(current_gray, (21, 21), 0)

    # 3. THE MATH: Subtract Background from Current
    # Only the parts that CHANGED will be bright
    frame_delta = cv2.absdiff(background_gray, current_gray)
    
    # 4. Convert the difference into a clear White/Black mask
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    
    # 5. Count the 'Movement' pixels
    movement_pixels = cv2.countNonZero(thresh)

    if movement_pixels > 5000: # If enough pixels changed...
        cv2.putText(current_frame, "MOTION DETECTED!", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Security Feed", current_frame)
    cv2.imshow("Movement Only (The Math)", thresh)

    # Press 'r' to reset the background
    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        background_gray = current_gray
        print("Background Reset!")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()