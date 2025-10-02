import streamlit as st
import altair as alt
import pandas as pd

from pages.load_data import read_sheet

sheet = read_sheet()

# ----- view -----------

st.subheader("📊 Current Attendance")
values = sheet.get("F2:F150")

# Count how many "Present"
total_present = sum(1 for v in values if v and v[0].strip() == "Present")
total_absent = sum(1 for v in values if v and v[0].strip() == "Absent")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="✅ Present", value=total_present)
with col2:
    st.metric(label="❌ Absent", value=total_absent)

st.metric(label="👥 Total Members", value=total_present + total_absent)

# --- pie chart ---
df_chart = pd.DataFrame({
    "Status": ["Present", "Absent"],
    "Count": [total_present, total_absent]
})

# Simple Pie Chart
chart = alt.Chart(df_chart).mark_arc().encode(
    theta='Count:Q',
    color=alt.Color('Status:N', legend=None)
)

st.altair_chart(chart, use_container_width=True)
