import streamlit as st
from database import supabase

st.title("🏫 About Shree Janta Secondary School Setup")

with st.form("school_info_form"):
    school_name = st.text_input("School Name", value="Shree Janta Secondary School")
    address = st.text_input("Address")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    principal_name = st.text_input("Principal Name")
    about_school = st.text_area("About School Description")
    
    save_info = st.form_submit_button("Save School Information")
    if save_info:
        data = {
            "school_name": school_name,
            "address": address,
            "phone": phone,
            "email": email,
            "principal_name": principal_name,
            "about_school": about_school
        }
        supabase.table("school_info").upsert({"id": 1, **data}).execute()
        st.success("School profile updated successfully!")