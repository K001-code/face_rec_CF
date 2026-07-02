import cv2, sys, pickle, face_recognition, time, gspread
import numpy as np
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials


def main():
    #check if camera is available, if not exit
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        sys.exit("ERROR: Could not open webcam.")

    # 1. SETUP GOOGLE SHEETS CONNECTION
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json",
        ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    )
    client = gspread.authorize(creds)
    SHEET_ID = "1RVUlJPBKztsl4wZRQHPA0mCs76JnKxbQQQwnTCvAe8I"
    sheet = client.open_by_key(SHEET_ID).sheet1

    global TEAM_MEMBERS, REQUIRED_SECONDS, STRICT_TOLERANCE # declare as global var
    # 2. ATTENDANCE LOGIC & MEMORY (make sure the names are the same as in the video files)
    TEAM_MEMBERS = ["bofang", "bota", "khin", "mana", "meng", "phanthorng", "phivath", "rany", "tharith", "sreynai"]
    REQUIRED_SECONDS = 4 
    STRICT_TOLERANCE = 0.35 # The lower the value, the stricter the recognition is
    logged_names = set()

    # This dictionary store the time when a person was first detected
    detection_timers = {}
    already_signed_in = [] # tracks students who have already scanned
    encoding_path = "face_encodings.pickle"
    known_encodings, known_names = load_encoding(encoding_path)
    

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
            # compare the face encoding of the camera frame to the known encodings
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            
            #if a face is detected, find the closest resemblance/distance
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                shortest_distance = face_distances[best_match_index]
                
                if shortest_distance <= STRICT_TOLERANCE:
                    name = known_names[best_match_index]
                    color = (0, 255, 0) 
                    if name in TEAM_MEMBERS:
                        #  Start the timer 
                        process_attendance(name, already_signed_in, detection_timers)
            
                        # Only log IF the timer is finished 
                        if name in already_signed_in:
                            log_attendance(name, logged_names, sheet)
            
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)
        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) == ord("q"):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    return


def load_encoding(path):
    try:
        with open(path, "rb") as f:
            known_data = pickle.load(f)
        print(f"Successfully loaded {len(known_data["names"])} known face(s).")
        return (known_data["encodings"], known_data["names"])
    except FileNotFoundError:
        sys.exit("ERROR: 'face_encodings.pickle' file not found.")
    except Exception as e:
        sys.exit(f"ERROR: Could not load pickle file. {e}")


def log_attendance(name, logged_names, sheet):
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


def process_attendance(name_detected, already_signed_in, detection_timers):
    current_time = time.time()
    # Skip instantly if already signed in
    if name_detected in already_signed_in:
        return
    # Start timer if new
    if name_detected not in detection_timers:
        detection_timers[name_detected] = current_time
        print(f" Started countdown for {name_detected}...")
        return
    # Calculate exact elapsed seconds
    elapsed = current_time - detection_timers[name_detected]
    print(f" Scanning {name_detected}: {int(elapsed)} / {REQUIRED_SECONDS} seconds passed...")
    
    if elapsed >= REQUIRED_SECONDS:
        print(f" 4 Seconds reached! Sending {name_detected} to Google Sheet...")
        already_signed_in.append(name_detected)
        del detection_timers[name_detected]

if __name__ == "__main__":
    main()