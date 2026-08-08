import streamlit as st
from database import supabase
from datetime import datetime
import base64
import os

st.set_page_config(
    page_title="Teacher Salary Receipt", 
    page_icon="💰", 
    layout="wide"
)

st.title("💰 Teacher Salary Receipt & Payroll System")

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

logo_base64 = get_image_base64("school logo.PNG")
school_photo_base64 = get_image_base64("janta.PNG")
teacher_photo_base64 = get_image_base64("ramesh sir.PNG") 

# ---------------- GET TEACHERS ----------------
teachers_res = supabase.table("teachers").select("*").execute()
teacher_list = []
if teachers_res.data:
    teacher_list = [t["name"] for t in teachers_res.data]

# ---------------- PAYROLL FORM ----------------
with st.form("payroll_receipt_form"):
    st.subheader("Generate Salary Receipt")

    if teacher_list:
        teacher_name = st.selectbox("Select Teacher", teacher_list)
    else:
        teacher_name = st.text_input("Teacher Name")

    base_salary = st.number_input("Base Salary", min_value=0.0, format="%.2f")
    allowances = st.number_input("Allowances", min_value=0.0, format="%.2f")
    deductions = st.number_input("Deductions", min_value=0.0, format="%.2f")
    bonus = st.number_input("Bonus", min_value=0.0, format="%.2f")

    net_salary = base_salary + allowances + bonus - deductions
    st.success(f"Calculated Net Salary: Rs. {net_salary:,.2f}")

    payment_method = st.selectbox("Payment Method", ["Cash", "Bank Transfer", "Cheque"])
    transaction_id = st.text_input("Transaction ID / Cheque No")
    salary_month = st.selectbox("Salary Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    payment_date = st.date_input("Payment Date")

    submit_payroll = st.form_submit_button("Generate Salary Receipt")

    if submit_payroll:
        payroll_data = {
            "teacher_name": teacher_name,
            "base_salary": base_salary,
            "allowances": allowances,
            "deductions": deductions,
            "bonus": bonus,
            "net_salary": net_salary,
            "payment_method": payment_method,
            "transaction_id": transaction_id,
            "salary_month": salary_month,
            "payment_date": str(payment_date)
        }

        supabase.table("payroll").insert(payroll_data).execute()

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

        teacher_res = supabase.table("teachers").select("*").eq("name", teacher_name).execute()
        if teacher_res.data:
            teacher_info = teacher_res.data[0]
        else:
            teacher_info = {}

        st.session_state.payroll_bill = {
            "school": school,
            "teacher": teacher_info,
            "payroll": payroll_data,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        st.success("Salary Receipt Generated Successfully!")

# ---------------- RECEIPT PREVIEW ----------------
if "payroll_bill" in st.session_state:
    data = st.session_state.payroll_bill
    school = data["school"]
    teacher = data["teacher"]
    payroll = data["payroll"]

    st.markdown("---")
    st.subheader("🖨️ Final Salary Receipt Preview")

    html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
@media print {{
    body * {{
        visibility: hidden;
    }}
    #printable-receipt, #printable-receipt * {{
        visibility: visible;
    }}
    #printable-receipt {{
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

<div id="printable-receipt" style="
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
OFFICIAL SALARY RECEIPT
</h4>

<hr style="margin: 10px 0;">

<table width="100%" style="font-size: 13px;">
<tr>
<td width="75%" style="vertical-align: top;">
<b>Teacher Details</b><br>
<b>Name:</b> {teacher.get('name', payroll['teacher_name'])}<br>
<b>Subject / Role:</b> {teacher.get('subject', 'N/A')}<br>
<b>Phone:</b> {teacher.get('phone', 'N/A')}<br>
<b>Salary Month:</b> {payroll['salary_month']}
</td>
<td width="25%" align="center" style="vertical-align: top;">
{f"<img src='{teacher_photo_base64}' width='90' height='90' style='border-radius:6px;border:2px solid #1B4F72; object-fit: cover; display:inline-block;'>" if teacher_photo_base64 else "<b>No Photo</b>"}
<br>
<span style="font-size: 10px;">Teacher Photo</span>
</td>
</tr>
</table>

<hr style="margin: 10px 0;">

<b style="font-size: 13px;">Salary Breakdown</b>

<table border="1" width="100%" cellpadding="5" style="border-collapse: collapse; font-size: 12px; margin-top: 5px;">
<tr style="background: #f2f2f2;">
<th>Description</th>
<th>Amount</th>
</tr>
<tr>
<td>Base Salary</td>
<td>Rs. {payroll['base_salary']:,.2f}</td>
</tr>
<tr>
<td>Allowances</td>
<td>Rs. {payroll['allowances']:,.2f}</td>
</tr>
<tr>
<td>Bonus</td>
<td>Rs. {payroll['bonus']:,.2f}</td>
</tr>
<tr>
<td>Deductions</td>
<td>Rs. {payroll['deductions']:,.2f}</td>
</tr>
<tr style="background: #eaf2f8; font-weight: bold;">
<td>Net Payable Salary</td>
<td>Rs. {payroll['net_salary']:,.2f}</td>
</tr>
</table>

<div style="margin-top: 10px; font-size: 12px;">
<b>Payment Method:</b> {payroll['payment_method']}<br>
<b>Transaction ID:</b> {payroll['transaction_id'] if payroll['transaction_id'] else 'N/A'}<br>
<b>Generated Date:</b> {data['date']}
</div>

<br><br>

<table width="100%">
<tr>
<td align="left">
<div class="no-print" style="margin-top: 10px;">
    <button onclick="window.print()" style="background-color: #1B4F72; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 14px; font-weight: bold;">
        🖨️ Print / Save Salary Receipt
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

    st.components.v1.html(html, height=720, scrolling=True)