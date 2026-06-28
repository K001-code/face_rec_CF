import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authorize
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Connect
SHEET_ID = "1RVUlJPBKztsl4wZRQHPA0mCs76JnKxbQQQwnTCvAe8I"
sheet = client.open_by_key(SHEET_ID).sheet1

# Test
sheet.append_row(["Rebuild_Check", "2026-06-28"])
print("Success! The new credentials are working.")