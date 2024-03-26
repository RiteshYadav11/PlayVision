import cv2
import numpy as np
import pickle

# Global variables
circles = []  # List to store selected points
selected = False  # Flag to indicate if points are selected

def mousePoints(event, x, y, flags, params):
    global circles, selected
    
    if event == cv2.EVENT_LBUTTONDOWN:
        circles.append([x, y])
        print(circles)
        
        cv2.circle(params['img'], (x, y), 10, (255, 0, 255), -1)
        cv2.imshow("Img", params['img'])

        # Check if 4 points are selected
        if len(circles) == 4:
            selected = True

def main():
    cap = cv2.VideoCapture(0)

    # Set the desired window size
    window_width = 1280
    window_height = 720

    # Set the window name and create the window
    cv2.namedWindow("Img", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Img", window_width, window_height)

    _, img = cap.read()

    if img is None:
        print("Failed to capture video")
        return

    # Print the resolution of the input image
    height, width, _ = img.shape
    print("Input image resolution: {}x{}".format(width, height))

    cv2.imshow("Img", img)
    cv2.setMouseCallback("Img", mousePoints, {'img': img})

    while True:
        _, img = cap.read()

        if selected:
            # Draw a polygon using the selected points
            pts = np.array(circles, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(img, [pts], True, (0, 255, 255), 2)
            
            # Create a mask for the selected region
            mask = np.zeros_like(img)
            cv2.fillPoly(mask, [pts], (255, 255, 255))
            
            # Apply the mask to the video frame to get the result
            result = cv2.bitwise_and(img, mask)

            # Resize the result image to 0.5 of its actual size
            result = cv2.resize(result, None, fx=0.5, fy=0.5)

            cv2.imshow("Result", result)
        else:
            cv2.imshow("Img", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Saving the points
    if selected:
        pickle.dump(circles, open("Calibration", 'wb'))

if __name__ == "__main__":
    main()