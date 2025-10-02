import streamlit as st
from pages.load_data import read_data,update_attendance

df = read_data()

# ---- view -----

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
