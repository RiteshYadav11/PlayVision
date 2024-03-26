import cv2
import numpy as np
import random
import time

# Function to handle mouse clicks
def draw_target(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global target_position
        target_position = (x, y)

# Function to update target position
def update_target_position(window_size):
    global target_position
    target_position = (random.randint(50, window_size[1] - 150), random.randint(50, window_size[0] - 150))

# Function to resize images
def resize_images(window_size):
    global goalpost, target
    goalpost_resized = cv2.resize(goalpost, (window_size[1], window_size[0]))
    target_resized = cv2.resize(target, (100, 100))
    return goalpost_resized, target_resized

# Load images
goalpost = cv2.imread('Files/GoalPost.jpg')
target = cv2.imread('Files/Target.jpg', cv2.IMREAD_UNCHANGED)

# Initialize window
window_name = 'Goalpost Game'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window_name, draw_target)
cv2.moveWindow(window_name, 0, 0)

# Initialize variables
target_position = (100, 100)  # Initial position of target
score = 0
start_time = time.time()

# Main loop
while True:
    # Get window size
    window_size = cv2.getWindowImageRect(window_name)[2::-1]
    
    # Resize images
    goalpost_resized, target_resized = resize_images(window_size)

    # Display images
    window_image = np.zeros((window_size[0], window_size[1], 3), dtype=np.uint8)
    window_image[:goalpost_resized.shape[0], :goalpost_resized.shape[1]] = goalpost_resized
    
    # Ensure target is within window boundaries
    target_x, target_y = target_position
    target_x = min(max(target_x, 0), window_size[1] - 100)
    target_y = min(max(target_y, 0), window_size[0] - 100)
    window_image[target_y:target_y + 100, target_x:target_x + 100] = target_resized

    # Display score and time
    elapsed_time = int(time.time() - start_time)
    cv2.putText(window_image, f'Score: {score}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(window_image, f'Time: {elapsed_time}s', (window_size[1] - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show window
    cv2.imshow(window_name, window_image)

    # Check for click on target
    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('c'):  # Click to update target position and increase score
        x, y = cv2.getWindowImageRect(window_name)[2::-1]
        if (target_x <= x < target_x + 100) and \
           (target_y <= y < target_y + 100):
            update_target_position(window_size)
            score += 1
        else:  # Draw pink circle at click location if target is not hit
            cv2.circle(window_image, (x, y), 10, (255, 0, 255), -1)

# Close window
cv2.destroyAllWindows()
