import streamlit as st
from database import supabase

st.title("🏛️ Faculty Management")
with st.form("faculty_form"):
    faculty_name = st.text_input("Faculty / Department Name (e.g., Science, Management)")
    department = st.text_input("Specific Department / Sub-section")
    head_of_faculty = st.text_input("Head of Faculty Name")
    description = st.text_area("Faculty Description & Notes")
    
    submitted = st.form_submit_button("Save Faculty Info")
    if submitted:
        supabase.table("faculty").insert({
            "faculty_name": faculty_name,
            "department": department,
            "head_of_faculty": head_of_faculty,
            "description": description
        }).execute()
        st.success("Faculty department saved successfully!")

st.markdown("---")
res = supabase.table("faculty").select("*").execute()
if res.data:
    st.dataframe(res.data)
else:
    st.info("No faculty records available.")