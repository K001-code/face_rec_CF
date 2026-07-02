## Automatic Student Attendance Tracking System with Facial Recognition  
The Automatic Student Attendance Tracking System with Facial Recognition is a project designed to replace manual roll calls with automated, biometric identification. The system detects, identifies, and logs students in real-time.  

## Features & Prerequisites
- __Real-time Detection__: Captures and identifies students instantly via camera input.  
- __Automated Tracking__: After student identified, automatically updates their attendance in Google Sheets  
- __Language__: Python
- __Libraries__: opencv-python, dlib, cmake, face_recognition, numpy, oauth2client


## Instruction
Run the following code snippets in terminal:  
### 1. Clone the repo to your local machine  
   `git clone https://github.com/K001-code/face_rec_CF.git`  
### 2. Install necessary libraries
   `pip install -r requirements.txt`
### 2. Generate training images from pre-provided videos
   `cd src`  
   `python vid2pic.py`  
### 3. Once converted to images, run the following code  
   `python encoding.py`  
### 4. After encoding, run the following program for live facial recognition and attendance update  
   `python main.py`