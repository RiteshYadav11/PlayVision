import cv2
import numpy as np
from ultralytics import YOLO
import pyautogui
import pickle
import torch

# Check if CUDA (GPU support) is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Opening the file in read mode
my_file = open("coco.txt", "r")
# Reading the file
data = my_file.read()
# Replacing end splitting the text when newline ('\n') is seen.
class_list = data.split("\n")
my_file.close()

# Function to load calibration data from a pickle file
def load_calibration_data(filename):
    try:
        circles = pickle.load(open(filename, "rb"))
        print("Calibration points loaded successfully:", circles)
        return circles
    except FileNotFoundError:
        print("Calibration file not found. Please run the calibration script first.")
        exit()

# Function to read the threshold value from a configuration file
def read_threshold_value(filename):
    try:
        with open(filename, 'r') as f:
            threshold_value = int(f.read().strip())
        print("Threshold value loaded successfully:", threshold_value)
        return threshold_value
    except FileNotFoundError:
        print("Configuration file not found. Using default threshold value.")
        return 140  # Default threshold value

def is_inside_roi(point, circles):
    # Convert the list of points to numpy array
    pts = np.array(circles, np.int32)
    pts = pts.reshape((-1, 1, 2))
    
    # Create a mask for the defined ROI
    mask = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
    cv2.fillPoly(mask, [pts], (255))
    
    # Check if the point is inside the ROI
    return cv2.pointPolygonTest(pts, point, False) >= 0

# Function to transform normalized video coordinates to screen coordinates using calibration data
def transform_video_to_screen(norm_x, norm_y, circles):
    # Get screen resolution
    screen_width, screen_height = pyautogui.size()
    
    # Here 'circles' represents the calibration data
    video_points = circles
    screen_points = [[0, 0], [screen_width, 0], [screen_width, screen_height], [0, screen_height]]

    video_w = video_points[2][0] - video_points[0][0]
    video_h = video_points[3][1] - video_points[0][1]
    screen_w = screen_points[2][0] - screen_points[0][0]
    screen_h = screen_points[3][1] - screen_points[0][1]

    screen_x = int(norm_x * screen_w + screen_points[0][0])
    screen_y = int(norm_y * screen_h + screen_points[0][1])

    return screen_x, screen_y

# Load YOLO model
model = YOLO("Weights/best.pt", "v8")

# Move model to GPU if available
if torch.cuda.is_available():
    model = model.cuda()

# Capture video from webcam
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Load calibration data
circles = load_calibration_data("Calibration")

# Read threshold value from configuration file
threshold_value = read_threshold_value("min_width_value.txt")

# Set initial mouse position to the center of the screen
pyautogui.moveTo(pyautogui.size()[0] // 2, pyautogui.size()[1] // 2)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Predict on the frame
    detect_params = model.predict(source=[frame], conf=0.45, save=False)

    if len(detect_params) > 0:
        for i in range(len(detect_params[0])):
            boxes = detect_params[0].boxes
            box = boxes[i]
            clsID = box.cls.cpu().numpy()[0]
            bb = box.xyxy.cpu().numpy()[0]

            # Calculate center coordinates of the detected object
            center_x = int((bb[0] + bb[2]) / 2)
            center_y = int((bb[1] + bb[3]) / 2)

            # Calculate width of the detected object
            width = bb[2] - bb[0]

            # Check if the object is a sports ball and its width is below the threshold
            if class_list[int(clsID)] == "sports ball" and width < threshold_value:
                cv2.rectangle(frame, (int(bb[0]), int(bb[1])), (int(bb[2]), int(bb[3])), (255, 0, 255), 3)
                cv2.putText(frame, f"Ball: ({center_x}, {center_y})", (center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                # Check if the center coordinates are inside the defined ROI
                if is_inside_roi((center_x, center_y), circles):
                    # Normalize the coordinates
                    norm_x = center_x / frame.shape[1]
                    norm_y = center_y / frame.shape[0]

                    # Map the coordinates to screen resolution using calibration data
                    screen_x, screen_y = transform_video_to_screen(norm_x, norm_y, circles)
                    offset_x = int(0.08 * pyautogui.size()[0])  # 1.2 cm left
                    offset_y = int(0.1 * pyautogui.size()[1])   # 1 cm above
                    screen_x += offset_x
                    screen_y += offset_y

                    # Move the mouse to the mapped coordinates
                    pyautogui.moveTo(screen_x, screen_y)
                    pyautogui.click()

    # Display the frame
    cv2.imshow("ObjectDetection", frame)

    # Terminate run when "Q" pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
