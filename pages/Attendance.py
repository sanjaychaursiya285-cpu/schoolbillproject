import streamlit as st
from database import supabase

st.title("📊 Attendance Management System")
with st.form("attendance_form"):
    person_type = st.selectbox("Attendance Type", ["Student", "Teacher"])
    person_name = st.text_input(f"Enter {person_type} Name")
    attendance_date = st.date_input("Attendance Date")
    status = st.selectbox("Status", ["Present", "Absent", "Late", "Leave"])
    remarks = st.text_input("Remarks (Optional)")
    
    submitted = st.form_submit_button("Save Attendance")
    if submitted:
        supabase.table("attendance").insert({
            "person_type": person_type,
            "person_name": person_name,
            "attendance_date": str(attendance_date),
            "status": status,
            "remarks": remarks
        }).execute()
        st.success(f"Attendance recorded for {person_name} ({status})!")

st.markdown("---")
st.subheader("Attendance Log Viewer")
log_data = supabase.table("attendance").select("*").order("id", desc=True).limit(20).execute()
if log_data.data:
    st.dataframe(log_data.data)
else:
    st.info("No recent attendance records.")