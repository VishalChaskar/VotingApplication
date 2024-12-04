import cv2
from deepface import DeepFace

img1_path = "Vishal1.jpg"

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Press 'Enter' to capture an image.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture webcam frame.")
        break

    cv2.imshow("Webcam - Press 'Enter' to capture", frame)

    key = cv2.waitKey(1)
    if key == 13:  # Enter key
        img2_path = "webcam_image.png"
        cv2.imwrite(img2_path, frame)
        print("Image captured.")
        break
cap.release()
cv2.destroyAllWindows()

result = DeepFace.verify(img1_path, img2_path, enforce_detection=False)
print("Result:", result)
