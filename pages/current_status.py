import streamlit as st
import altair as alt
import pandas as pd

from pages.load_data import read_sheet,read_data

sheet = read_sheet()
df = read_data()
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


# --- Team-wise summary  ---
# Make a safe copy and normalize attendance text
df_clean = df.copy()
df_clean['Attendance'] = df_clean['Attendance'].astype(str).fillna('').str.strip()

# Flag present robustly (handles "Present", "present", "✅ Present", etc.)
df_clean['is_present'] = df_clean['Attendance'].str.lower().str.contains('present', na=False)

# Present count per team (sum of True values), total members per team (size)
present_counts = df_clean.groupby('Team')['is_present'].sum().astype(int)
total_counts = df_clean.groupby('Team').size().astype(int)

# Combine into a dataframe
summary = pd.concat([present_counts, total_counts], axis=1).reset_index()
summary.columns = ['Team', 'Present', 'Total']

# # Optional: sort teams numerically when possible
# try:
#     summary['Team_sort'] = pd.to_numeric(summary['Team'], errors='coerce')
#     summary = summary.sort_values(['Team_sort']).drop(columns=['Team_sort']).reset_index(drop=True)
# except Exception:
#     summary = summary.sort_values('Team').reset_index(drop=True)

# Build Attendance column like "4/10"
summary['Attendance'] = summary['Present'].astype(str) + '/' + summary['Total'].astype(str)

# Final table with index column starting at 1
final_df = summary[['Team', 'Attendance']].copy()

# Reset index starting from 1 for display
final_df.index = range(1, len(final_df) + 1)

# Show
st.write("### Team-wise Attendance Summary")
st.dataframe(final_df, use_container_width=True)
