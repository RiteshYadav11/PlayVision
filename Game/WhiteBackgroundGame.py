import cv2
import numpy as np

# Function to handle mouse clicks
def draw_circle(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(transparent_background, (x, y), 10, (255, 0, 255), -1)  # Pink color

# Create a transparent background image
transparent_background = np.zeros((720, 1280, 4), dtype=np.uint8)
# transparent_background[:, :] = [255, 255, 255, 0]  # Set background to transparent
transparent_background[:, :, :3] = 255  # Set RGB channels to white
transparent_background[:, :, 3] = 0  # Set alpha channel to 0 for full transparency


# Create resizable window
cv2.namedWindow('Whiteboard Game', cv2.WINDOW_NORMAL)
cv2.imshow('Whiteboard Game', transparent_background)
cv2.setMouseCallback('Whiteboard Game', draw_circle)

# Main loop
while True:
    cv2.imshow('Whiteboard Game', transparent_background)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('r'):  # Reset the display if 'r' is pressed
        transparent_background = np.zeros((720, 1280, 4), dtype=np.uint8)
        transparent_background[:, :] = [255, 255, 255, 0]  # Set background to transparent

cv2.destroyAllWindows()
