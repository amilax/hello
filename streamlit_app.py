import streamlit as st

current_status_page = st.Page(
    page= "pages/current_status.py",
    title= "Current Attendance",
    default = True
)

attendence_page = st.Page(
    page= "pages/attendance.py",
    title= "Mark Attendance",
)

add_new_page = st.Page(
    page= "pages/add_new.py",
    title= "Add New",
)

teams_page = st.Page(
    page= "pages/teams.py",
    title= "Teams Details",
)

pg = st.navigation(pages = [current_status_page,attendence_page,add_new_page,teams_page])

st.logo("logo.png",size="large")

pg.run()
