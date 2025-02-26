import cv2
import os
import argparse
import subprocess
from ultralytics import YOLO
import easyocr
import numpy as np

parser = argparse.ArgumentParser(description="Extract rider and number plate images from a video.")
parser.add_argument("video_path", type=str, help="Path to the input video file.")
args = parser.parse_args()

yolo_model_path = r"E:\Python Projects\attempt1\archive\runs\detect\train14\weights\best.pt"
output_dir = r"E:\Python Projects\attempt1\archive\source\challan\static"
ocr_script_path = r"E:\Python Projects\attempt1\archive\script\ocr_helper.py"  # Path to OCR script

os.makedirs(output_dir, exist_ok=True)  


model = YOLO(yolo_model_path)

cap = cv2.VideoCapture(args.video_path)
if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

frame_count = 0
rider_saved = False
plate_saved = False
rider_img_path = os.path.join(output_dir, "rider.jpg")
plate_img_path = os.path.join(output_dir, "plate.jpg")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break 
    frame_count += 1
    results = model(frame)

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            bbox = list(map(int, box.xyxy[0].tolist()))  
            
            if class_id == 2 and not rider_saved:
                rx1, ry1, rx2, ry2 = bbox
                rider_crop = frame[ry1:ry2, rx1:rx2]
                if rider_crop.size > 0:
                    cv2.imwrite(rider_img_path, rider_crop)
                    rider_saved = True
                    print(f"✅ Rider Image Saved: {rider_img_path}")

            elif class_id == 3 and not plate_saved:
                px1, py1, px2, py2 = bbox
                plate_crop = frame[py1:py2, px1:px2]
                if plate_crop.size > 0:
                    cv2.imwrite(plate_img_path, plate_crop)
                    plate_saved = True
                    print(f"✅ Number Plate Image Saved: {plate_img_path}")

        if rider_saved and plate_saved:
            break

    if rider_saved and plate_saved:
        break  

cap.release()
cv2.destroyAllWindows()

print("✅ Detection completed. Images saved.")


image_path = r"E:\Python Projects\attempt1\archive\source\challan\static\plate.jpg"
output_txt_path = r"E:\Python Projects\attempt1\archive\script\output\plate_value.txt"


os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)


if not os.path.exists(image_path):
    print("⚠️ Number plate image not found. OCR script not triggered.")
    exit()

print("🚀 Running OCR script...")


image = cv2.imread(image_path)

if image is None or image.size == 0:
    print("❌ Error: Could not load image. Check the file path and validity!")
    exit()


reader = easyocr.Reader(['en'], gpu=True)
results = reader.readtext(image, detail=1, allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")


plate_data = [(bbox, text, confidence) for bbox, text, confidence in results if confidence > 0.5]


plate_data.sort(key=lambda item: item[0][0][0])

plate_text = " ".join([text for (_, text, _) in plate_data])

if plate_text:
    try:
        with open(output_txt_path, "w") as file:
            file.write(plate_text)
        print(f"✅ Number plate saved to: {output_txt_path}")
        print(f"🚘 Final Detected Number Plate: {plate_text}")
    except PermissionError:
        print(f"❌ Permission Error: Unable to write to {output_txt_path}. Try running the script as Administrator.")
else:
    print("⚠️ OCR could not detect clear text.")
