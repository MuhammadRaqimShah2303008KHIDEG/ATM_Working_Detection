import cv2
import ultralytics
from ultralytics import YOLO

model = YOLO('best.pt')
results = model.track(source='test2.mp4', \
save=True, show=True, project='./result', tracker="bytetrack.yaml", conf=0.35)