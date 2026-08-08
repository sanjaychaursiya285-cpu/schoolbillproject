import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Shree Janta Secondary School",
    page_icon="🏫",
    layout="wide"
)

# Initialize login session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def logout():
    st.session_state.logged_in = False
    st.rerun()

# -------------------------------------------------------------------
# 🔒 LOGIN SCREEN
# -------------------------------------------------------------------
if not st.session_state.logged_in:
    st.title("🔐 Shree Janta Secondary School - Login")

    with st.form("login_form"):
        username = st.text_input("Username / Email")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", type="primary")

        if submit:
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid Username or Password!")

    st.stop()  # Stop execution so pages are hidden when not logged in

# -------------------------------------------------------------------
# 🗺️ MULTI-PAGE NAVIGATION (Renders only when logged_in = True)
# -------------------------------------------------------------------

# Logout button in sidebar
st.sidebar.caption(f"Logged in as: **{st.session_state.get('username', 'Admin')}**")
if st.sidebar.button("Logout", type="secondary"):
    logout()

# Define Navigation Pages
dashboard_page = st.Page("pages/dashboard.py", title="dashboard", icon="📊", default=True)
students_page  = st.Page("pages/students.py", title="Students", icon="🎓")
teachers_page  = st.Page("pages/teachers.py", title="Teachers", icon="👨‍🏫")
fee_page   = st.Page("pages/fee.py", title="Finance & Fees", icon="💳")
About_school_page = st.Page("pages/about_school.py", title="About_school", icon="📊")
faculty_page   = st.Page("pages/faculty.py", title="Faculty", icon="💳")
Attendance_page   = st.Page("pages/Attendance.py", title="Attendance", icon="💳")
Marks_page   = st.Page("pages/Marks.py", title="Marks", icon="💳")
Payroll_page   = st.Page("pages/payroll.py", title="Payroll", icon="💳")
financial_page   = st.Page("pages/financial.py", title="Financial", icon="💳")


# Setup Navigation with groups
pg = st.navigation({
    "Main": [dashboard_page],
    "Management": [
        students_page,
        teachers_page,
        financial_page,
        Payroll_page,
        Marks_page,
        Attendance_page,
        faculty_page,
        About_school_page,
        fee_page,dashboard_page
    ]
})

pg.run()
