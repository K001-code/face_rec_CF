import gspread  # <--- THIS WAS MISSING
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- CONNECT TO THE CLOUD ---
# Note: Ensure 'credentials.json' is in the same folder as main.py
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Use your verified Sheet ID
SHEET_ID = "1RVUlJPBKztsl4wZRQHPA0mCs76JnKxbQQQwnTCvAe8I"
sheet = client.open_by_key(SHEET_ID).sheet1

# --- LOGGING FUNCTION ---
def log_attendance(name):
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([name, now])
        print(f"Successfully sent {name} to Google Sheets!")
    except Exception as e:
        print(f"Error sending to sheet: {e}")
# --- TEMPORARY TEST BLOCK ---
# This will run as soon as you execute 'python main.py' or wait for understand the flw of team 1 first
if __name__ == "__main__":
    print("Testing connection from main.py...")
    log_attendance("System_Test_User")