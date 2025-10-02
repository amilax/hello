import streamlit as st
from pages.load_data import read_sheet

sheet = read_sheet()

# ----- view -----------

st.subheader("📊 Current Attendance")
values = sheet.get("F2:F150")

# Count how many "Present"
total_present = sum(1 for v in values if v and v[0].strip() == "Present")
total_absent = sum(1 for v in values if v and v[0].strip() == "Absent")

st.write("✅ Present:", total_present)
st.write("❌ Absent:", total_absent)
st.write("👥 Total Members:", total_present + total_absent)