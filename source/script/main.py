import cv2
import torch
import json
import easyocr
from ultralytics import YOLO
import os

model_path = os.path.join(os.path.dirname(__file__), "..", "runs", "detect", "train14", "weights", "best.pt")
model = YOLO(model_path)

reader = easyocr.Reader(['en'])

source = os.path.join(os.path.dirname(__file__), "..", "test", "videos", "sample1.mp4")
cap = cv2.VideoCapture(source)

checked_riders = set()
detection_data = []
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame_count += 1
    
    detections = model(frame)
    riders = []
    plates = []
    
    for result in detections:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            class_id = int(box.cls[0])
            
            if class_id == 2:  
                riders.append((x1, y1, x2, y2))
            elif class_id == 3:  
                plates.append({
                    "bbox": [x1, y1, x2, y2],
                    "image_path": os.path.join("..", "output", "plates", f"plate_{frame_count}_{len(plates)}.jpg")
                })
    
    for rider_box in riders:
        x1, y1, x2, y2 = rider_box
        rider_id = f"rider_{x1}_{y1}_{x2}_{y2}"
        
        if rider_id not in checked_riders:
         
            best_plate = None
            best_distance = float("inf")
            for plate in plates:
                px1, py1, px2, py2 = plate["bbox"]
                distance = abs(y2 - py1)
                if distance < best_distance:
                    best_distance = distance
                    best_plate = plate
            
            detection_data.append({
                "rider_id": rider_id,
                "helmet_status": "without helmet",
                "image_path": os.path.join("..", "output", "riders", f"rider_{frame_count}.jpg"),
                "number_plate": {
                    "bbox": best_plate["bbox"] if best_plate else None,
                    "image_path": best_plate["image_path"] if best_plate else None
                }
            })
            checked_riders.add(rider_id)

cap.release()

output_path = os.path.join("/", "detections.json")
with open(output_path, "w") as f:
    json.dump(detection_data, f, indent=4)

print(f"Detections saved to {output_path}")
