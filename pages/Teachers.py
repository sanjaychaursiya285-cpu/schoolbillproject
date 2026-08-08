import streamlit as st
from database import supabase

st.title("👩‍🏫 Teacher Directory")
with st.form("teacher_form"):
    name = st.text_input("Teacher Full Name")
    subject = st.text_input("Subject Specialization")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    submitted = st.form_submit_button("Save Teacher Record")
    if submitted:
        supabase.table("teachers").insert({"name": name, "subject": subject, "phone": phone, "email": email}).execute()
        st.success("Teacher saved successfully!")

st.markdown("---")
res = supabase.table("teachers").select("*").execute()
if res.data:
    st.dataframe(res.data)
else:
    st.info("No teacher records found.")