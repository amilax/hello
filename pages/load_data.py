import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd


# ---------------- Google Sheets Setup ----------------
def connect_to_gsheet(creds_json, spreadsheet_name, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds",
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open(spreadsheet_name)
    return spreadsheet.worksheet(sheet_name)


# Config
SPREADSHEET_NAME = 'ESWA Ella Attendance New'
SHEET_NAME = 'Teams_W_N'
CREDENTIALS_FILE = './credentials.json'

# Connect
sheet = connect_to_gsheet(CREDENTIALS_FILE, SPREADSHEET_NAME, SHEET_NAME)


# Read Data
def read_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)


# Add Data
def add_data(row):
    sheet.append_row(row)


# Update Attendance
def update_attendance(phone,team, attendance):
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Convert to string and strip spaces
    df["Phone Number"] = df["Phone Number"].astype(str).str.strip()
    phone = str(phone).strip()

    if phone in df["Phone Number"].values:
        row_index = df.index[df["Phone Number"] == phone][0] + 2  # +2 for header + 1-based index
        sheet.update_cell(row_index, 4, team)  # 4th col = team
        sheet.update_cell(row_index, 6, attendance)  # 6th col = Attendance
        return True
    return False

def read_sheet():
    return sheet