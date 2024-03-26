import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image, ImageTk
import pyautogui
import random
import torch

class BallDetectionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ball Detection App")

        # Check for CUDA availability
        if torch.cuda.is_available():
            self.device = 'cuda'
        else:
            self.device = 'cpu'

        # Load the YOLOv8 model
        self.model = YOLO("Weights/best.pt")
        self.model.to(self.device)

        # Opening the file in read mode
        my_file = open("coco.txt", "r")
        # Reading the file
        data = my_file.read()
        # Replacing end splitting the text | when newline ('\n') is seen.
        self.class_list = data.split("\n")
        my_file.close()

        # Generate random colors for class list
        self.detection_colors = []
        for i in range(len(self.class_list)):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.detection_colors.append((b, g, r))

        self.screen_width, self.screen_height = pyautogui.size()

        # Set the frame width and height to match the screen resolution
        self.frame_wid = self.screen_width
        self.frame_hyt = self.screen_height

        # Initialize array to store width values
        self.width_values = []

        # Create GUI elements
        self.start_button = ttk.Button(master, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = ttk.Button(master, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.video_label = tk.Label(master)
        self.video_label.pack()

        # Flag to control recording loop
        self.recording = False
        self.cap = None

    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            print("Cannot open video file")
            return

        while self.recording:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            # If frame is read correctly, ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            # Resize frame to fit the screen resolution
            frame = cv2.resize(frame, (self.frame_wid, self.frame_hyt))

            # Predict on image
            detect_params = self.model.predict(source=[frame], conf=0.45, save=False)

            # Convert tensor array to numpy
            DP = detect_params[0].numpy()

            if len(DP) != 0:
                for i in range(len(detect_params[0])):
                    boxes = detect_params[0].boxes
                    box = boxes[i]
                    clsID = box.cls.cpu().numpy()[0]
                    conf = box.conf.cpu().numpy()[0]
                    bb = box.xyxy.cpu().numpy()[0]

                    center_x = int((bb[0] + bb[2]) / 2)
                    center_y = int((bb[1] + bb[3]) / 2)

                    # Calculate width and height of the detected object
                    width = bb[2] - bb[0]
                    height = bb[3] - bb[1]

                    # Store width value in the array
                    self.width_values.append(width)

                    cv2.rectangle(
                        frame,
                        (int(bb[0]), int(bb[1])),
                        (int(bb[2]), int(bb[3])),
                        self.detection_colors[int(clsID)],
                        3,
                    )

                    # Display class name and confidence
                    font = cv2.FONT_HERSHEY_COMPLEX
                    cv2.putText(
                        frame,
                        self.class_list[int(clsID)] + " " + str(round(conf, 3)) + "%",
                        (int(bb[0]), int(bb[1]) - 10),
                        font,
                        1,
                        (255, 255, 255),
                        2,
                    )

                    # Display x and y coordinates
                    cv2.putText(
                        frame,
                        "X: " + str(center_x) + ", Y: " + str(center_y),
                        (int(bb[0]), int(bb[1]) - 30),
                        font,
                        1,
                        (255, 255, 255),
                        2,
                    )
                    cv2.putText(
                        frame,
                        "Width: {:.2f}".format(width),
                        (int(bb[0]), int(bb[3]) + 30),
                        font,
                        1,
                        (255, 255, 255),
                        2,
                    )

            # Convert frame to RGB for tkinter display
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img = ImageTk.PhotoImage(image=img)
            self.video_label.configure(image=img)
            self.video_label.image = img

            # Update GUI
            self.master.update()

        # Stop recording
        self.stop_recording()

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # When recording stops, calculate minimum width value and save it to a file
        if self.width_values:
            min_width_value = min(self.width_values)
            with open("min_width_value.txt", "w") as f:
                f.write(str(min_width_value))

        # Release the capture
        if self.cap is not None:
            self.cap.release()
            cv2.destroyAllWindows()

def main():
    root = tk.Tk()
    app = BallDetectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
