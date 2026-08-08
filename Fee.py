import streamlit as st
from database import supabase
from datetime import datetime
import base64
import os

st.set_page_config(
    page_title="Shree Janta Secondary School - Bill", 
    page_icon="🧾", 
    layout="wide"
)

st.title("🧾 Master Consolidated School Bill & Statement")

# ---------------- IMAGE FUNCTION ----------------
def get_image_base64(filename):
    paths = [filename, f"C:/Users/IDEAL_COMPUTER/Desktop/{filename}"]
    for path in paths:
        if os.path.exists(path):
            with open(path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
            ext = path.split(".")[-1].lower()
            mime = "image/png" if ext == "png" else "image/jpeg"
            return f"data:{mime};base64,{encoded}"
    return ""

# Load all images (logo, school photo, and student photo separately)
logo_base64 = get_image_base64("school logo.PNG")
school_photo_base64 = get_image_base64("janta.PNG")
student_photo_base64 = get_image_base64("girl photo.PNG")

# ---------------- GET STUDENTS ----------------
students_res = supabase.table("students").select("*").execute()
student_list = []
if students_res.data:
    student_list = [s["full_name"] for s in students_res.data]

# ---------------- BILL FORM ----------------
with st.form("master_bill_form"):
    st.subheader("Student All Inclusive Bill")

    if student_list:
        selected_student = st.selectbox("Select Student", student_list)
    else:
        selected_student = st.text_input("Student Name")

    fee_type = st.selectbox(
        "Fee Type",
        ["Tuition Fee", "Library Fee", "Exam Fee", "Transport Fee", "Computer Fee"]
    )

    total_fee = st.number_input("Total Fee", min_value=0.0, format="%.2f")
    paid_amount = st.number_input("Paid Amount", min_value=0.0, format="%.2f")
    due_amount = total_fee - paid_amount

    st.success(f"Due Amount : Rs. {due_amount:,.2f}")

    payment_method = st.selectbox(
        "Payment Method",
        ["Cash", "Bank Transfer", "ESEWA", "Khalti", "Cheque"]
    )

    remarks = st.text_area("Remarks")
    submit = st.form_submit_button("Generate Master Bill")

    if submit:
        fee_data = {
            "student_name": selected_student,
            "fee_type": fee_type,
            "total_fee": total_fee,
            "paid_amount": paid_amount,
            "due_amount": due_amount,
            "payment_method": payment_method,
            "remarks": remarks
        }

        supabase.table("fees").insert(fee_data).execute()

        school_res = supabase.table("school_info").select("*").execute()
        if school_res.data:
            school = school_res.data[0]
        else:
            school = {
                "school_name": "SHREE JANTA SECONDARY SCHOOL",
                "address": "Nepal",
                "phone": "N/A",
                "email": "N/A"
            }

        student_res = supabase.table("students").select("*").eq("full_name", selected_student).execute()
        if student_res.data:
            student = student_res.data[0]
        else:
            student = {}

        st.session_state.bill = {
            "school": school,
            "student": student,
            "fee": fee_data,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        st.success("Bill Generated Successfully")

# ---------------- BILL PREVIEW ----------------
if "bill" in st.session_state:
    data = st.session_state.bill
    school = data["school"]
    student = data["student"]
    fee = data["fee"]

    st.markdown("---")
    st.subheader("🖨️ Final Bill Preview")

    html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
@media print {{
    body * {{
        visibility: hidden;
    }}
    #printable-bill, #printable-bill * {{
        visibility: visible;
    }}
    #printable-bill {{
        position: absolute;
        left: 0;
        top: 0;
        width: 100%;
        border: none !important;
        box-shadow: none !important;
    }}
    .no-print {{
        display: none !important;
    }}
}}
</style>
</head>
<body style="background-color: #f9f9f9; padding: 10px;">

<div id="printable-bill" style="
border:2px solid #1B4F72;
padding:15px;
font-family:Arial;
font-size: 13px;
max-width: 700px;
margin: auto;
background: white;
">

<!-- TOP HEADER: SCHOOL LOGO, NAME & SCHOOL PHOTO -->
<table width="100%" style="margin-bottom: 5px;">
<tr>
<td width="20%" align="center">
{f"<img src='{logo_base64}' width='75' style='display:inline-block;'>" if logo_base64 else "<b>Logo</b>"}
</td>
<td width="60%" align="center">
<h3 style="margin: 2px 0; color: #1B4F72;">{school.get('school_name','School')}</h3>
<p style="margin: 0; font-size: 11px; color: #555;">
{school.get('address','Nepal')} | Phone: {school.get('phone','N/A')}
</p>
</td>
<td width="20%" align="center">
{f"<img src='{school_photo_base64}' width='90' height='80' style='border-radius:4px; object-fit: cover; display:inline-block; border: 1px solid #1B4F72;'>" if school_photo_base64 else "<b>School Photo</b>"}
</td>
</tr>
</table>

<h4 style="margin: 8px 0 10px 0; background: #1B4F72; color: white; padding: 4px; text-align: center;">
MASTER CONSOLIDATED BILL
</h4>

<hr style="margin: 10px 0;">

<table width="100%" style="font-size: 13px;">
<tr>
<td width="75%" style="vertical-align: top;">
<b>Student Details</b><br>
<b>Name:</b> {student.get('full_name',fee['student_name'])}<br>
<b>Grade:</b> {student.get('grade','N/A')}<br>
<b>Phone:</b> {student.get('phone','N/A')}<br>
<b>Address:</b> {student.get('address','N/A')}
</td>
<td width="25%" align="center" style="vertical-align: top;">
{f"<img src='{student_photo_base64}' width='90' height='90' style='border-radius:6px;border:2px solid #1B4F72; object-fit: cover; display:inline-block;'>" if student_photo_base64 else "<b>No Photo</b>"}
<br>
<span style="font-size: 10px;">Student Photo</span>
</td>
</tr>
</table>

<hr style="margin: 10px 0;">

<b style="font-size: 13px;">Fee Details</b>

<table border="1" width="100%" cellpadding="5" style="border-collapse: collapse; font-size: 12px; margin-top: 5px;">
<tr style="background: #f2f2f2;">
<th>Fee Type</th>
<th>Total</th>
<th>Paid</th>
<th>Due</th>
</tr>
<tr>
<td>{fee['fee_type']}</td>
<td>Rs. {fee['total_fee']:,.2f}</td>
<td>Rs. {fee['paid_amount']:,.2f}</td>
<td>Rs. {fee['due_amount']:,.2f}</td>
</tr>
</table>

<div style="margin-top: 10px; font-size: 12px;">
<b>Payment Method:</b> {fee['payment_method']}<br>
<b>Remarks:</b> {fee['remarks'] if fee['remarks'] else 'None'}<br>
<b>Date:</b> {data['date']}
</div>

<br><br>

<table width="100%">
<tr>
<td align="left">
<div class="no-print" style="margin-top: 10px;">
    <button onclick="window.print()" style="background-color: #1B4F72; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: bold;">
        🖨️ Print / Save PDF
    </button>
</div>
</td>
<td align="right" style="font-size: 12px;">
_____________________<br>
<b>Principal Signature</b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</td>
</tr>
</table>

</div>

</body>
</html>
"""

    # st.components.v1.html का उपयोग करने से JavaScript सीधे और सही तरीके से काम करेगा
    st.components.v1.html(html, height=680, scrolling=True)