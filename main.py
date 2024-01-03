import cv2
import os
from ultralytics import YOLO
from datetime import datetime
import time  # Added for time-based operations

def detect_atm_usage(model_path, video_path, target_fps, output_dir):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)
    frame_no = 0
    frame_interval = int(cap.get(cv2.CAP_PROP_FPS) / target_fps)

    # Set time limits
    start_time = None
    atm_detection_timeout = 100  # 100 seconds timeout for ATM card detection
    cash_detection_timeout = 100  # 100 seconds timeout for cash detection after ATM card detection

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            print(f"Working with frame {frame_no}, no frame detected")
            break

        # **ATM card and note detection logic**
        atm_detected = False
        results = model.track(source=frame, show=True, project='./result', tracker="bytetrack.yaml", conf=0.4)
    
        for result in results:
            labels = result.boxes.data.cpu().numpy()
            
            if len(labels) != 0:
                a = labels[0]
                if a[-1] == 0 and a[-2] > 0.35:
                    print("ATM Card is Detected") 
                    
                    # Start the timer for ATM card detection
                    if start_time is None:
                        start_time = time.time()

                    # Check if ATM card detection timeout has elapsed
                    if (time.time() - start_time) >= atm_detection_timeout:
                        print("ATM detection timeout reached. Exiting...")
                        cap.release()
                        return "ATM is not Working"

                # Additional logic for cash detection
                if a[-1] == 1 and a[-2] > 0.8:
                    print("Cash is Detected")
                    
                    # Check if cash detection timeout has not elapsed
                    if (time.time() - start_time) < cash_detection_timeout:
                        print("ATM is Working")
                        cap.release()
                        return "ATM is Working"
                    else:
                        print("Cash detection timeout reached. Exiting...")
                        cap.release()
                        return "ATM is not Working"

        # Increment frame counter
        frame_no += 1

    # Release video capture
    cap.release()

    print("ATM is not Working")
    return "ATM is not Working"

# Example usage (unchanged):
model_path = 'best.pt'
video_path = "test2.mp4"
target_fps = 8
output_dir = 'detections/frames/'
working = detect_atm_usage(model_path, video_path, target_fps, output_dir)
print(working)



#  Attributes:
#         xyxy (torch.Tensor | numpy.ndarray): The boxes in xyxy format.
#         conf (torch.Tensor | numpy.ndarray): The confidence values of the boxes.
#         cls (torch.Tensor | numpy.ndarray): The class values of the boxes.
#         id (torch.Tensor | numpy.ndarray): The track IDs of the boxes (if available).
#         xywh (torch.Tensor | numpy.ndarray): The boxes in xywh format.
#         xyxyn (torch.Tensor | numpy.ndarray): The boxes in xyxy format normalized by original image size.
#         xywhn (torch.Tensor | numpy.ndarray): The boxes in xywh format normalized by original image size.
#         data (torch.Tensor): The raw bboxes tensor (alias for `boxes`).