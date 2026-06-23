# import turtle

# t = turtle.Turtle()
# for _ in range(2):
#     t.forward(150)  
#     t.left(90)     
#     t.forward(80)   
#     t.left(90)      

# turtle.done()



# import cv2 as cv
# import numpy as np
# import requests
# import sys

# # 1. Paste your Google Drive sharing link here:
# share_link = "https://drive.google.com/file/d/1Ssag4n61sv6SlyaP7mUm2CoTYy-X_pt4/view?usp=sharing"
# # 2. Convert the link into a direct download link
# file_id = share_link.split('/d/')[1].split('/')[0]
# download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
# # 3. Download the image bytes using requests
# try:
#     response = requests.get(download_url)
#     img_array = np.frombuffer(response.content, np.uint8)
#     img = cv.imdecode(img_array, cv.IMREAD_COLOR)
# except Exception as e:
#     sys.exit(f"Failed to fetch image from Drive: {e}")

# # Check if image was successfully decoded
# if img is None:
#     sys.exit("Could not decode the image data from Google Drive.")

# # --- DRAWING OPERATIONS ---
# cv.rectangle(img, (10, 10), (100, 100), (0, 0, 255), 2)
# cv.putText(img, 'Hello OpenCV', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# cv.imshow("Display window", img)
# cv.waitKey(0)





# import cv2 as cv
# import numpy as np
# import requests
# import sys
# import os

# # 1. Your new close-up photo Google Drive link
# share_link = "https://drive.google.com/file/d/1Vur3QGdMRYnHAZ_dGrtoIOban8224KGo/view?usp=sharing"

# # 2. Extract ID and download
# file_id = share_link.split('/d/')[1].split('/')[0]
# download_url = f'https://drive.google.com/uc?export=download&id={file_id}'

# try:
#     response = requests.get(download_url)
#     img_array = np.frombuffer(response.content, np.uint8)
#     img = cv.imdecode(img_array, cv.IMREAD_COLOR)
# except Exception as e:
#     sys.exit(f"Failed to fetch image from Drive: {e}")

# if img is None:
#     sys.exit("Could not download the image. Make sure the file was uploaded completely and shared properly!")

# # --- DRAWING OPERATIONS ---
# # These coordinates are scaled specifically to frame the face on this photo size
# cv.rectangle(img, (60, 150), (450, 560), (0, 0, 255), 3)

# # White text sitting neatly just above the box
# cv.putText(img, 'Face Detected', (60, 130), 
#            cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

# # --- FORCE SAVE IT INSIDE FACE_REC_CF ---
# script_dir = os.path.dirname(os.path.abspath(__file__))
# save_path = os.path.join(script_dir, "my_drawn_image.jpg")

# cv.imwrite(save_path, img)
# print("SUCCESS! Saved with your new close-up picture.")




# import cv2 as cv
# import sys

# # 1. Connect to your built-in webcam (0 is usually the main camera)
# cap = cv.VideoCapture(0)

# if not cap.isOpened():
#     sys.exit("Error: Could not open your camera. Make sure no other app is using it!")

# print("Camera started! Look at your bottom taskbar for the 'Live Camera' window.")
# print("Press the 'q' key on your keyboard while looking at the camera window to close it.")

# # 2. Loop forever to read frame-by-frame (like a movie)
# while True:
#     # Capture one single frame from the camera
#     ret, frame = cap.read()
    
#     if not ret:
#         print("Failed to grab frame.")
#         break

#     # --- DRAWING OPERATIONS ON LIVE VIDEO ---
#     # This draws a red box right in the middle of your camera view
#     cv.rectangle(frame, (200, 150), (450, 450), (0, 0, 255), 3)
    
#     # White text sitting above the box
#     cv.putText(frame, 'Scanning Face...', (200, 130), 
#                cv.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

#     # 3. Display the live frame in a window
#     cv.imshow('Live Camera Feed', frame)

#     # 4. BREAK OUT OF THE LOOP: Press 'q' on your keyboard to stop the camera
#     if cv.waitKey(1) & 0xFF == ord('q'):
#         break

# # Clean up and close everything down when done
# cap.release()
# cv.destroyAllWindows()
# print("Camera closed successfully.")




import cv2 as cv
import sys
face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv.VideoCapture(0)
if not cap.isOpened():
    sys.exit("Error: Could not open camera.")
print("Face Tracking Active! Look at the pop-up window.")
print("Press 'q' on your keyboard while looking at the video window to quit.")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    for (x, y, w, h) in faces:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        cv.putText(frame, 'Face Detected', (x, y - 10), 
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv.imshow('Live Face Tracking', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
print("Tracking stopped.")


