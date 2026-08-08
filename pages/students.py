import streamlit as st
from database import supabase

st.title("👨‍🎓 Student Records & Registration")
tab1, tab2 = st.tabs(["Add New Student", "Student Records Directory"])

with tab1:
    st.subheader("Register New Student")
    with st.form("student_form"):
        full_name = st.text_input("Full Name")
        grade = st.selectbox("Grade / Class", ["Class 9", "Class 10", "Class 11", "Class 12"])
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        phone = st.text_input("Contact Phone")
        address = st.text_input("Address")
        enrollment_date = st.date_input("Enrollment Date")
        
        submitted = st.form_submit_button("Save Student Record")
        if submitted:
            data = {
                "full_name": full_name,
                "grade": grade,
                "gender": gender,
                "phone": phone,
                "address": address,
                "enrollment_date": str(enrollment_date)
            }
            supabase.table("students").insert(data).execute()
            st.success("Student registered successfully!")

with tab2:
    st.subheader("Enrolled Students Directory")
    response = supabase.table("students").select("*").execute()
    if response.data:
        st.dataframe(response.data)
    else:
        st.info("No student records found.")