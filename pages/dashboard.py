import streamlit as st
from database import supabase

st.title("📊 Shree Janta Secondary School - Executive Dashboard")
st.markdown("### Real-Time School Analytics & Metrics")

try:
    students_res = supabase.table("students").select("id", count="exact").execute()
    total_students = students_res.count if students_res.count is not None else len(students_res.data)
except Exception:
    total_students = 0

try:
    teachers_res = supabase.table("teachers").select("id", count="exact").execute()
    total_teachers = teachers_res.count if teachers_res.count is not None else len(teachers_res.data)
except Exception:
    total_teachers = 0

try:
    fees_res = supabase.table("fees").select("paid_amount").execute()
    total_fee_collected = sum([row.get("paid_amount", 0) for row in fees_res.data]) if fees_res.data else 0.0
except Exception:
    total_fee_collected = 0.0

try:
    fin_res = supabase.table("financial").select("amount").execute()
    total_expenses = sum([row.get("amount", 0) for row in fin_res.data]) if fin_res.data else 0.0
except Exception:
    total_expenses = 0.0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Students", value=total_students)
with col2:
    st.metric(label="Total Teachers", value=total_teachers)
with col3:
    st.metric(label="Fee Revenue", value=f"Rs. {total_fee_collected:,.2f}")
with col4:
    st.metric(label="Total Expenses", value=f"Rs. {total_expenses:,.2f}")

st.markdown("---")
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Recent Fee Transactions")
    recent_fees = supabase.table("fees").select("student_name, fee_type, paid_amount, payment_date").order("id", desc=True).limit(5).execute()
    if recent_fees.data:
        st.dataframe(recent_fees.data, use_container_width=True)
    else:
        st.info("No fee data available.")

with col_b:
    st.subheader("Recent Student Registrations")
    recent_students = supabase.table("students").select("full_name, grade, phone, enrollment_date").order("id", desc=True).limit(5).execute()
    if recent_students.data:
        st.dataframe(recent_students.data, use_container_width=True)
    else:
        st.info("No student records found.")
