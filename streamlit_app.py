import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

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
SPREADSHEET_NAME = 'ESWA Ella Attendance New'
SHEET_NAME = 'Teams_W_N'

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

df = read_data()

# ---------------- Streamlit App ----------------
with st.sidebar:

    st.image("logo.png", use_container_width=True)
    
    selected = option_menu(
        menu_title=None,
        options = ["Mark Attendance", "Add New", "Current Attendance", "Teams Details"],
        icons=["pencil-square","plus-square-fill","bar-chart-fill","people-fill"],
        menu_icon = "cast",
        default_index=0,
    )


if selected == "Mark Attendance":
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
    attendance_input = st.checkbox("Attendance")

    attendance_input_val = "Present" if attendance_input else "Absent"

    if st.button("Update Attendance"):
        success = update_attendance(phone,group_input, attendance_input_val)
        if success:
            st.success(f"✅ Attendance updated for {name} ({phone})")
        else:
            st.error("❌ Phone number not found in sheet")


if selected == "Add New":
    st.subheader("➕ Add New Member")

    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        group = st.text_input("Team Number")
        attendance = st.checkbox("Attendance")
        submitted = st.form_submit_button("Add Record")

        attendance_input_val = "Present" if attendance else "Absent"

        if submitted:
            if phone and name:
                add_data(["",name, phone, group,"", attendance_input_val])
                st.success(f"✅ Added new record: {name}, {phone}, Team {group}, Attendance {attendance}")
            else:
                st.error("⚠️ Please fill all required fields")

if selected == "Current Attendance":

    st.subheader("📊 Current Attendance")
    values = sheet.get("F2:F150")
    
    # Count how many "Present"
    total_present = sum(1 for v in values if v and v[0].strip() == "Present")
    total_absent = sum(1 for v in values if v and v[0].strip() == "Absent")

    st.write("✅ Present:", total_present)
    st.write("❌ Absent:", total_absent)
    st.write("👥 Total Members:", total_present + total_absent)

if selected == "Teams Details":

    st.subheader("👥 Team Details")

    # --- Step 1: Select Team ---
    team_numbers = df["Team"].dropna().unique().tolist()
    team_numbers.sort()
    selected_team = st.selectbox("Select Team Number", options=team_numbers)

    if selected_team:
        # --- Step 2: Filter team members ---
        team_df = df[df["Team"].astype(str) == str(selected_team)][["Name", "Phone Number", "Attendance"]].copy()

        # Reset index starting from 1 for display
        team_df.index = range(1, len(team_df) + 1)

        # Convert attendance for display
        team_df_display = team_df.copy()
        team_df_display["Attendance"] = team_df_display["Attendance"].apply(
            lambda x: "✅ Present" if str(x) == "Present" else "❌ Absent"
        )

         # --- Step 3: Dynamic present count ---
        present_count = team_df["Attendance"].apply(lambda x: 1 if str(x).strip().lower() == "present" else 0).sum()
        st.info(f"✅ Present: {present_count} / {len(team_df)}")
        

        st.write(f"### Members in Team {selected_team}")
        st.dataframe(team_df_display, use_container_width=True)


        # --- Step 4: Select member to update ---
        member_names = team_df["Name"].tolist()
        selected_member = st.selectbox("Select member to update", options=member_names)

        if selected_member:
            member_record = team_df[team_df["Name"] == selected_member].iloc[0]

            st.write(f"Updating: **{member_record['Name']} ({member_record['Phone Number']})**")

            # Attendance checkbox
            attendance_val = st.checkbox(
                "Attendance",
                value=True if str(member_record["Attendance"]) == "Present" else False
            )

            # --- Step 5: Update button ---
            if st.button("Update Attendance"):
                phone = member_record["Phone Number"]
                new_attendance = "Present" if attendance_val else "Absent"
                update_attendance(phone, selected_team, new_attendance)
                st.success(f"✅ Attendance updated for {selected_member}")

                # Optional: refresh team_df to show updated attendance
                df = read_data()

