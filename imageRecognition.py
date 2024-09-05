
import cv2
import numpy as np
import requests
from io import BytesIO
from PIL import Image

# URL of the ESP32-CAM
url="http://192.168.43.115/capture"

def fetch_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img
    else:
        print("Failed to fetch image from ESP32-CAM")
        return None
def capture_image_from_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open webcam")
        return None

    ret, frame = cap.read()
    cap.release()

    if ret:
        return frame
    else:
        print("Failed to capture image from webcam")
        return None

def detect_faces(img):
    # Load OpenCV's pre-trained Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1, minSize=(30, 30))
    print(faces)
    return faces

def main():
    #img = fetch_image(url)
    img = capture_image_from_webcam()
    if img is not None:
        faces = detect_faces(img)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        cv2.imshow('ESP32-CAM Face Detection', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No image to process.")

if __name__ == "__main__":
    main()
