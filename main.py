# --- IMPORTS ---
import cv2
import sys
import pickle
import face_recognition
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. SETUP GOOGLE SHEETS CONNECTION ( team 2)
# 1. SETUP GOOGLE SHEETS CONNECTION
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json",
    ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
)
client = gspread.authorize(creds)

#thisis the id that that will put the name to the sheet
SHEET_ID = "1RVUlJPBKztsl4wZRQHPA0mCs76JnKxbQQQwnTCvAe8I"
sheet = client.open_by_key(SHEET_ID).sheet1
# 2. ATTENDANCE LOGIC & MEMORY ( make sure name doch in the file )
TEAM_MEMBERS = ["bofang", "bota", "khin", "mana", "meng", "phanthorng", "phivath", "rany", "tharith", "sreynai"]
logged_names = set() 
# if unkknow send to google cloud
def log_attendance(name):
    if name in logged_names:
        return 

    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([name, now])
        print(f"SUCCESS: Recorded {name} to Google Sheet!")
        logged_names.add(name)
    except Exception as e:
        print(f"ERROR: Could not log to sheet: {e}")

#3. FACE RECOGNITION MAIN LOOP ( team 1)
def main():
    STRICT_TOLERANCE = 0.40

    try:
        with open("face_encodings.pickle", "rb") as f:
            known_data = pickle.load(f)
        known_encodings = known_data["encodings"]
        known_names = known_data["names"]
        print(f"Successfully loaded {len(known_names)} known face(s).")
    except FileNotFoundError:
        sys.exit("ERROR: 'face_encodings.pickle' file not found.")
    except Exception as e:
        sys.exit(f"ERROR: Could not load pickle file. {e}")

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        sys.exit("ERROR: Could not open webcam.")

    while True:
        ret, frame = cap.read()
        if not ret:
            sys.exit("ERROR: Camera disconnected.")
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            color = (0, 0, 255)  
            
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                shortest_distance = face_distances[best_match_index]
                
                if shortest_distance <= STRICT_TOLERANCE:
                    name = known_names[best_match_index]
                    color = (0, 255, 0) 
                    
                    if name in TEAM_MEMBERS:
                        log_attendance(name)
            
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)
            
        cv2.imshow("Camera", frame)
        
        if cv2.waitKey(1) == ord("q"):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
def log_attendance(name):
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([name, now])
        print(f"Successfully sent {name} to Google Sheets!")
    except Exception as e:
        print(f"Error sending to sheet: {e}")
# TEMPORARY TEST BLOCK
# This will run as soon as you execute 'python main.py' or wait for understand the flw of team 1 first
if __name__ == "__main__":
    print("Testing connection from main.py...")
    log_attendance("System_Test_User")