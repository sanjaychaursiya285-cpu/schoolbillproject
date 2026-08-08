import streamlit as st
from database import supabase

st.title("📝 Student Examination Marks")
with st.form("marks_form"):
    student_name = st.text_input("Student Name")
    exam_name = st.selectbox("Exam Name", ["First Terminal", "Second Terminal", "Pre-Board", "Final Board Exam"])
    subject = st.text_input("Subject Name")
    full_marks = st.number_input("Full Marks", min_value=0.0, value=100.0)
    pass_marks = st.number_input("Pass Marks", min_value=0.0, value=40.0)
    obtained_marks = st.number_input("Obtained Marks", min_value=0.0)
    remarks = st.text_input("Performance Remarks / Grade")
    
    submitted = st.form_submit_button("Save Student Marks")
    if submitted:
        supabase.table("student_marks").insert({
            "student_name": student_name,
            "exam_name": exam_name,
            "subject": subject,
            "full_marks": full_marks,
            "pass_marks": pass_marks,
            "obtained_marks": obtained_marks,
            "remarks": remarks
        }).execute()
        st.success("Marks recorded successfully!")

st.markdown("---")
marks_res = supabase.table("student_marks").select("*").execute()
if marks_res.data:
    st.dataframe(marks_res.data)
else:
    st.info("No exam mark records found.")