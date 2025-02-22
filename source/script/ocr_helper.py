import cv2
import easyocr


image_path = r"E:\Python Projects\attempt1\archive\processed_plate.jpg"

image = cv2.imread(image_path)

if image is None:
    print("Error: Could not load image. Check the path!")
    exit()

reader = easyocr.Reader(['en'])

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

results = reader.readtext(gray)

for bbox, text, confidence in results:
    print(f"Detected Text: {text} (Confidence: {confidence:.2f})")
