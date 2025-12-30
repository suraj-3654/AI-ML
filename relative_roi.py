import cv2

# Global variables to store our click
click_x, click_y = 100, 100 # Default starting position

# 1. THE CALLBACK: This runs whenever the mouse moves or clicks
def select_point(event, x, y, flags, param):
    global click_x, click_y
    if event == cv2.EVENT_LBUTTONDOWN: # If Left Mouse Button is Clicked
        click_x, click_y = x, y
        print(f"New Anchor Set at: {x}, {y}")

cap = cv2.VideoCapture(0)
cv2.namedWindow("Click to Move Zone")
# Connect the window to our mouse function
cv2.setMouseCallback("Click to Move Zone", select_point)

while True:
    ret, frame = cap.read()
    if not ret: break

    # 2. DEFINE THE BOX DIMENSIONS
    width, height = 150 , 150
    
    # 3. APPLY YOUR LOGIC (The Slice)
    # We use the click_x and click_y from our mouse function
    roi = frame[click_y : click_y + height, click_x : click_x + width]
    
    # 4. DRAW THE BOX
    cv2.rectangle(frame, (click_x, click_y), 
                  (click_x + width, click_y + height), (0, 255, 0), 2)

    cv2.imshow("Click to Move Zone", frame)
    # Show the 'cut-out' separately to see it working!
    cv2.imshow("The ROI Slice", roi) 

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()