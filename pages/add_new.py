import streamlit as st
from pages.load_data import add_data

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
            add_data(["", name, phone, group, "", attendance_input_val])
            st.success(f"✅ Added new record: {name}, {phone}, Team {group}, Attendance {attendance}")
        else:
            st.error("⚠️ Please fill all required fields")