import streamlit as st

attendence_page = st.Page(
    page= "pages/attendance.py",
    title= "Mark Attendance",
    default = True
)

add_new_page = st.Page(
    page= "pages/add_new.py",
    title= "Add New",
)

current_status_page = st.Page(
    page= "pages/current_status.py",
    title= "Current Attendance",
)

teams_page = st.Page(
    page= "pages/teams.py",
    title= "Teams Details",
)

pg = st.navigation(pages = [attendence_page,add_new_page,current_status_page,teams_page])

st.logo("logo.png",size="large")

pg.run()
