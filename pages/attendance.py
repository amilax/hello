import streamlit as st
from pages.load_data import read_data,update_attendance


df = read_data()

# -----View------

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
# attendance_input = st.checkbox("Attendance")

# Attendance checkbox
attendance_input = st.checkbox(
    "Attendance",
    value=True if str(attendance) == "Present" else False)


attendance_input_val = "Present" if attendance_input else "Absent"

if st.button("Update Attendance"):
    success = update_attendance(phone, group_input, attendance_input_val)
    if success:
        st.success(f"✅ Attendance updated for {name} ({phone})")
        df = read_data()
    else:
        st.error("❌ Phone number not found in sheet")