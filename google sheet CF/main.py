import cv2
import face_recognition
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- 1. SETUP GOOGLE SHEETS CONNECTION ---
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", 
        ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)
sheet = client.open("AttendanceSheet").sheet1

# --- 2. FACE RECOGNITION SETUP ---

# --- 3. THE LOGIC --- to add more member.

if name == "Bo Fang":
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([name, now])
    print(f"Recorded {name} to Google Sheet!")
else:
    print(f"Detected {name}, not logging to Sheet.")