import streamlit as st
from database import supabase

st.title("📈 Financial & Expense Management")
with st.form("financial_form"):
    category = st.selectbox("Category", ["Utilities", "Maintenance", "Supplies", "Events", "Miscellaneous", "Other"])
    amount = st.number_input("Amount (Rs.)", min_value=0.0)
    description = st.text_area("Description / Particulars")
    
    submitted = st.form_submit_button("Save Financial Entry")
    if submitted:
        supabase.table("financial").insert({
            "category": category,
            "amount": amount,
            "description": description
        }).execute()
        st.success("Financial transaction logged successfully!")

st.markdown("---")
fin_res = supabase.table("financial").select("*").order("id", desc=True).execute()
if fin_res.data:
    st.dataframe(fin_res.data)
else:
    st.info("No financial entries found.")