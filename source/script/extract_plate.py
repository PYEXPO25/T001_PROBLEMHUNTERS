import cv2
import os
import argparse
import subprocess
from ultralytics import YOLO
import easyocr
import numpy as np
# ======== Parse Command-Line Arguments ========
parser = argparse.ArgumentParser(description="Extract rider and number plate images from a video.")
parser.add_argument("video_path", type=str, help="Path to the input video file.")
args = parser.parse_args()

# ======== Configuration ========
yolo_model_path = r"E:\Python Projects\attempt1\archive\runs\detect\train14\weights\best.pt"
output_dir = r"E:\Python Projects\attempt1\archive\source\challan\static"
ocr_script_path = r"E:\Python Projects\attempt1\archive\script\ocr_helper.py"  # Path to OCR script

os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# ======== Load YOLO Model ========
model = YOLO(yolo_model_path)

# ======== Video Capture ========
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
        break  # End of video
    frame_count += 1

    # Run YOLO inference on the current frame.
    results = model(frame)

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            bbox = list(map(int, box.xyxy[0].tolist()))  # [x1, y1, x2, y2]

            # Save Rider Image (Class 2)
            if class_id == 2 and not rider_saved:
                rx1, ry1, rx2, ry2 = bbox
                rider_crop = frame[ry1:ry2, rx1:rx2]
                if rider_crop.size > 0:
                    cv2.imwrite(rider_img_path, rider_crop)
                    rider_saved = True
                    print(f"✅ Rider Image Saved: {rider_img_path}")

            # Save Number Plate Image (Class 3)
            elif class_id == 3 and not plate_saved:
                px1, py1, px2, py2 = bbox
                plate_crop = frame[py1:py2, px1:px2]
                if plate_crop.size > 0:
                    cv2.imwrite(plate_img_path, plate_crop)
                    plate_saved = True
                    print(f"✅ Number Plate Image Saved: {plate_img_path}")

        # Stop processing once both images are saved
        if rider_saved and plate_saved:
            break

    if rider_saved and plate_saved:
        break  # Exit loop if both images are captured

cap.release()
cv2.destroyAllWindows()

print("✅ Detection completed. Images saved.")

# ======== Run OCR Script If Number Plate Image Exists ========

# **Image Path**
# **Image Path**
import cv2
import os
import easyocr

# **File Paths**
image_path = r"E:\Python Projects\attempt1\archive\source\challan\static\plate.jpg"
output_txt_path = r"E:\Python Projects\attempt1\archive\script\output\plate_value.txt"

# **Ensure the parent directory exists**
os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)

# **Check if plate image exists**
if not os.path.exists(image_path):
    print("⚠️ Number plate image not found. OCR script not triggered.")
    exit()

print("🚀 Running OCR script...")

# **Load Image**
image = cv2.imread(image_path)

if image is None or image.size == 0:
    print("❌ Error: Could not load image. Check the file path and validity!")
    exit()

# **Run EasyOCR**
reader = easyocr.Reader(['en'], gpu=True)
results = reader.readtext(image, detail=1, allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

# **Process OCR Results**
plate_data = [(bbox, text, confidence) for bbox, text, confidence in results if confidence > 0.5]

# **Sort Text by X-Coordinate (Ensures correct order)**
plate_data.sort(key=lambda item: item[0][0][0])

# **Combine All Text**
plate_text = " ".join([text for (_, text, _) in plate_data])

# **Save to Text File (Create if not exists)**
# if plate_text:
#     try:
#         with open(output_txt_path, "w") as file:
#             file.write(plate_text)
#         print(f"✅ Number plate saved to: {output_txt_path}")
#         print(f"🚘 Final Detected Number Plate: {plate_text}")
#     except PermissionError:
#         print(f"❌ Permission Error: Unable to write to {output_txt_path}. Try running the script as Administrator.")
# else:
#     print("⚠️ OCR could not detect clear text.")
