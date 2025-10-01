import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd


# ---------------- Google Sheets Setup ----------------
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
import json

def connect_to_gsheet(spreadsheet_name, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds",
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]

    # Load credentials from Streamlit secrets
    creds_dict = st.secrets["gcp_service_account"]
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open(spreadsheet_name)
    return spreadsheet.worksheet(sheet_name)

# Config
SPREADSHEET_NAME = 'eswa_ella_attendence'
SHEET_NAME = 'attendence'

# Connect
sheet = connect_to_gsheet(SPREADSHEET_NAME, SHEET_NAME)


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


# ---------------- Streamlit App ----------------
st.title("ESWA - ELLA")

# Mode Selection
mode = st.selectbox("Choose an action:", ["Mark Attendance", "Add New"])

df = read_data()

if mode == "Mark Attendance":
    st.subheader("🔍 Search & Update Attendance")

    # Phone number autocomplete
    phone = st.selectbox("Phone Number", options=[""] + df["Phone Number"].astype(str).tolist())

    name, group, attendance = "", "", 0

    if phone:
        record = df[df["Phone Number"].astype(str) == str(phone)]
        if not record.empty:
            name = record["Name"].values[0]
            group = record["Team"].values[0]
            attendance = record["Attendance"].values[0]

    # Show details
    name_input = st.text_input("Name", value=name, disabled=True)
    group_input = st.text_input("Team", value=group, disabled=False)
    attendance_input = st.checkbox("Attendance", value=bool(attendance))

    if st.button("Update Attendance"):
        success = update_attendance(phone,group_input, int(attendance_input))
        if success:
            st.success(f"✅ Attendance updated for {name} ({phone})")
        else:
            st.error("❌ Phone number not found in sheet")


elif mode == "Add New":
    st.subheader("➕ Add New Member")

    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        group = st.text_input("Team Number")
        attendance = st.checkbox("Attendance")
        submitted = st.form_submit_button("Add Record")

        if submitted:
            if phone and name:
                add_data(["",name, phone, group,"", int(attendance)])
                st.success(f"✅ Added new record: {name}, {phone}, Team {group}, Attendance {attendance}")
            else:
                st.error("⚠️ Please fill all required fields")

