import cv2

image_path = r"E:\Python Projects\attempt1\archive\output\plates\plate_frame_50.jpg"
image = cv2.imread(image_path)
if image is None:
    print("Error: Could not load image!")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blurred = cv2.GaussianBlur(gray, (5, 5), 0)

thresh = cv2.adaptiveThreshold(
    blurred, 255, 
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
    cv2.THRESH_BINARY, 11, 2
)

# Optionally, you could use fixed thresholding:
# _, thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)

cv2.imshow("Original", image)
cv2.imshow("Grayscale", gray)
cv2.imshow("Blurred", blurred)
cv2.imshow("Thresholded", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("processed_image.jpg", thresh)
