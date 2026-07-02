# --- IMPORTS ---
import cv2
import sys
import pickle
import face_recognition
import numpy as np
import gspread
import time
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
    # Check if we already sent this name. If yes, stop here!
    if name in logged_names:
        return 

    # If not, send to Google Sheets
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([name, now])
        print(f"Successfully sent {name} to Google Sheets!")
        
        # Add to the logged_names list so we don't send it again
        logged_names.add(name)
        
    except Exception as e:
        print(f"Error sending to sheet: {e}")

# track time, dak timing
# This dictionary store the time when a person was first detected
detection_timers = {}
already_signed_in = [] # it prevents from  dak name 2 dong
REQUIRED_SECONDS = 2
# I imported the librabry time
def process_attendance(name_detected):
    current_time = time.time()
    # 1. Skip instantly if already signed in (No lag)
    if name_detected in already_signed_in:
        return 
    # 2. Start timer if new
    if name_detected not in detection_timers:
        detection_timers[name_detected] = current_time
        print(f" Started countdown for {name_detected}...")
        return
    # 3. Calculate exact elapsed seconds
    elapsed = current_time - detection_timers[name_detected]
    print(f" Scanning {name_detected}: {int(elapsed)} / {REQUIRED_SECONDS} seconds passed...")
    
    if elapsed >= REQUIRED_SECONDS:
        print(f" 3 Seconds reached! Sending {name_detected} to Google Sheet...")
        already_signed_in.append(name_detected)
        del detection_timers[name_detected]

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
                        #  Start the timer 
                        process_attendance(name)
            
                        # Only log IF the timer is finished 
                        if name in already_signed_in:
                            log_attendance(name)

                   # if name in TEAM_MEMBERS: 
                   #   log_attendance(name)( i changed these 2 lines to the 6lines on the top )
                   
            
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)
            
        cv2.imshow("Camera", frame)
        
        if cv2.waitKey(1) == ord("q"):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
