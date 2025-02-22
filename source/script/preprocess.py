import cv2
import numpy as np

def preprocess_image(image_path):
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)

    kernel = np.ones((3,3), np.uint8)
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

    processed_path = "processed_plate.jpg"
    cv2.imwrite(processed_path, morph)
    
    return processed_path

processed_img = preprocess_image(r"E:\Python Projects\attempt1\archive\output\plates\plate_frame_98.jpg")
cv2.imshow("Processed Image", cv2.imread(processed_img))
cv2.waitKey(0)
cv2.destroyAllWindows()
