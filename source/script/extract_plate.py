import cv2
import os
import json
from ultralytics import YOLO


yolo_model_path = r"E:\Python Projects\attempt1\archive\runs\detect\train14\weights\best.pt"  
video_source = r"E:\Python Projects\attempt1\archive\test\videos\sample2.mp4"               
output_dir = r"E:\Python Projects\attempt1\archive\output"                                   
rider_dir = os.path.join(output_dir, "riders")        
plate_dir = os.path.join(output_dir, "plates")          
json_output_path = os.path.join(output_dir, "detections.json")  

# Create output directories if they don't exist.
os.makedirs(rider_dir, exist_ok=True)
os.makedirs(plate_dir, exist_ok=True)

# ======== Load YOLO Model ========
model = YOLO(yolo_model_path)

# ======== Video Capture ========
cap = cv2.VideoCapture(video_source)
if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

frame_count = 0
results_data = [] 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  
    frame_count += 1

    results = model(frame)
    
    for result in results:
        for box in result.boxes:
            if int(box.cls[0]) == 0:
                helmet_found = True
                break
        if helmet_found:
            break

    if helmet_found:
        continue

    rider_box = None
    plate_box = None
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            bbox = list(map(int, box.xyxy[0].tolist()))  
            if class_id == 2 and rider_box is None:  
                rider_box = bbox
            elif class_id == 3 and plate_box is None: 
                plate_box = bbox

   
    if rider_box is None or plate_box is None:
        continue

    rx1, ry1, rx2, ry2 = rider_box
    rider_crop = frame[ry1:ry2, rx1:rx2]
    px1, py1, px2, py2 = plate_box
    plate_crop = frame[py1:py2, px1:px2]

    # Save the cropped images with unique filenames.
    rider_img_path = os.path.join(rider_dir, f"rider_frame_{frame_count}.jpg")
    plate_img_path = os.path.join(plate_dir, f"plate_frame_{frame_count}.jpg")
    cv2.imwrite(rider_img_path, rider_crop)
    cv2.imwrite(plate_img_path, plate_crop)

    results_data.append({
        "frame": frame_count,
        "rider_image_path": os.path.abspath(rider_img_path),
        "plate_image_path": os.path.abspath(plate_img_path)
    })

    cv2.imshow("Video Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

with open(json_output_path, "w") as f:
    json.dump(results_data, f, indent=4)

print(f"✅ Detections saved to {json_output_path}")
