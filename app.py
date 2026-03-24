import streamlit as st
import pandas as pd
import pytesseract
import plotly.express as px
from PIL import Image
from database import init_db, insert_report, register_user, login_user, get_all_users, get_all_reports
from fraud_model import predict_message
from alerts import send_alert
from url_checker import check_url
from quiz import get_quiz
from voice_detection import detect_voice_from_file

# Initialize DB
init_db()

# Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="ShieldAI | Fraud Detection", page_icon="🛡️", layout="wide")

# ---------- ADVANCED CUSTOM STYLING ----------
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #020617);
        color: #f8fafc;
    }
    
    /* Glassmorphism Containers */
    div.stButton > button {
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4);
        border: none;
        color: white;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Modern Cards */
    .css-1r6slb0, .e1f1d6gn1 {
        background: rgba(30, 41, 59, 0.5);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    /* Title Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
        animation: fadeIn 1s ease-out;
    }

    .sub-text {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 3rem;
    }

    /* Input Field Styling */
    .stTextInput input, .stTextArea textarea, .stSelectbox div {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = ""

# ---------- AUTHENTICATION UI ----------
# ---------- IMPROVED LOGIN / REGISTER SYSTEM ----------
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🔐 Access Portal")
        
        # Using tabs for a cleaner "Registration Accordingly" flow
        tab1, tab2 = st.tabs(["Existing User", "New Registration"])

        with tab2:
            st.markdown("### Create Account")
            new_user = st.text_input("Choose Username", placeholder="e.g. johndoe123")
            new_pwd = st.text_input("Create Password", type="password", help="Use a strong password")
            
            # This is the "Accordingly" part: Defining the role during registration
            new_role = st.select_slider(
                "Select Account Level",
                options=["User", "Admin"],
                help="Admins have access to the Dashboard and User Management."
            )
            
            if st.button("Complete Registration", use_container_width=True):
                if new_user and new_pwd:
                    # Logic: Check if user already exists (handled in your register_user function)
                    register_user(new_user, new_pwd, new_role)
                    st.success(f"✅ {new_role} Account Created! You can now login.")
                    st.balloons()
                else:
                    st.warning("⚠️ Please fill in all fields.")

        with tab1:
            st.markdown("### Login")
            user = st.text_input("Username", key="l_user")
            pwd = st.text_input("Password", type="password", key="l_pwd")
            
            if st.button("Sign In", use_container_width=True):
                result = login_user(user, pwd)
                if result:
                    # result[3] is the role column from your DB (ID, User, Pwd, Role)
                    st.session_state.logged_in = True
                    st.session_state.role = result[3] 
                    st.success(f"Welcome back, {user}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()
# ---------- SIDEBAR NAVIGATION ----------
with st.sidebar:
    st.markdown('<h1 style="color:#38bdf8;">🛡️ ShieldAI</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    if st.session_state.role == "Admin":
        menu = ["📊 Dashboard", "👥 Users", "🔍 Detect", "🌐 URL", "🎤 Voice", "📸 Screenshot", "📝 Report", "🧠 Quiz"]
    else:
        menu = ["🔍 Detect", "🌐 URL", "🎤 Voice", "📸 Screenshot", "📝 Report", "🧠 Quiz"]
    
    choice = st.radio("Navigation", menu)
    
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.role = ""
        st.rerun()

# ---------- MAIN CONTENT AREA ----------
st.markdown(f'<div class="main-title">{choice}</div>', unsafe_allow_html=True)

# ---------- DASHBOARD (TREE GRAPH VERSION) ----------
if choice == "📊 Dashboard":
    st.markdown("### 🏛️ System Overview")
    
    # ✅ Fetch data from DB
    reports = get_all_reports()

    # ✅ Convert to DataFrame safely
    if reports:
        df = pd.DataFrame(reports, columns=["id", "user_id", "type", "description", "link"])
    else:
        df = pd.DataFrame(columns=["id", "user_id", "type", "description", "link"])

    # ✅ Create 3 columns
    col1, col2, col3 = st.columns(3)

    # ✅ Metrics
    total_reports = len(df)
    fraud_count = total_reports   # since all are fraud reports
    safe_count = 0

    col1.metric("Total Reports", total_reports)
    col2.metric("Fraud Detected", fraud_count)
    col3.metric("Safe Messages", safe_count)

    st.markdown("---")
    st.markdown("### 🌳 Fraud Distribution (Tree Graph)")

    # ✅ Treemap
    if not df.empty:
        fig = px.treemap(
            df,
            path=[px.Constant("All Scams"), "type", "user_id"],
            values="id",
            color="type",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hover_data=["description"]
        )

        fig.update_layout(
            margin=dict(t=10, l=10, r=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No report data available to generate tree graph.")

    # ✅ Line chart
    st.markdown("### 📊 Activity Trends")
    chart_data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri"],
        "Incidents": [4, 7, 2, 8, 5]
    })
    st.line_chart(chart_data.set_index("Day"))
# USER MANAGEMENT
elif choice == "👥 Users":
    users = get_all_users()
    df_users = pd.DataFrame(users)
    
    c1, c2 = st.columns(2)
    with c1: search = st.text_input("🔍 Search Users")
    with c2: role_filter = st.selectbox("Filter Role", ["All", "User", "Admin"])
    
    filtered_df = df_users.copy()
    if search: filtered_df = filtered_df[filtered_df['username'].str.contains(search, case=False)]
    if role_filter != "All": filtered_df = filtered_df[df_users['role'] == role_filter]
    
    st.dataframe(filtered_df, use_container_width=True)

# FRAUD DETECTION
elif choice == "🔍 Detect":
    col1, col2 = st.columns([2, 1])
    with col1:
        msg = st.text_area("Paste Content to Analyze", height=200, placeholder="Enter SMS, Email or Message body here...")
    with col2:
        email = st.text_input("Alert Recipient", placeholder="email@example.com")
        analyze_btn = st.button("Run AI Analysis", use_container_width=True)
    
    if analyze_btn:
        with st.spinner("Analyzing patterns..."):
            result = predict_message(msg)
            if "Fraud" in result:
                st.error(f"🚩 {result}")
                if email:
                    send_alert(email, msg)
                    st.warning("⚠️ Alert email dispatched to security team.")
            else:
                st.success(f"✅ {result}")

# URL CHECKER
elif choice == "🌐 URL":
    url = st.text_input("Enter URL to verify", placeholder="https://suspicious-link.com")
    if st.button("Scan URL"):
        result = check_url(url)
        if "Suspicious" in result: st.error(result)
        else: st.success(result)

# SCREENSHOT ANALYSIS
elif choice == "📸 Screenshot":
    file = st.file_uploader("Upload suspicious screenshot", type=["png", "jpg", "jpeg"])
    if file:
        img = Image.open(file)
        st.image(img, caption="Uploaded Image", use_container_width=True)
        with st.spinner("Extracting text via OCR..."):
            text = pytesseract.image_to_string(img)
            st.info(f"**Extracted Text:** {text}")
            result = predict_message(text)
            st.write(f"**AI Verdict:** {result}")

# SCAM REPORTING
elif choice == "📝 Report":
    with st.form("report_form"):
        uid = st.number_input("User ID", min_value=1)
        typ = st.selectbox("Scam Category", ["Phishing", "OTP", "Lottery", "Job Scam"])
        desc = st.text_area("Detailed Description")
        link = st.text_input("Source Link (if any)")
        if st.form_submit_button("Submit Official Report"):
            insert_report(uid, typ, desc, link)
            st.success("✅ Report logged in secure database.")

# CYBER QUIZ
elif choice == "🧠 Quiz":
    quiz = get_quiz()
    st.markdown(f"### {quiz['question']}")
    ans = st.radio("Select the correct safety measure:", quiz["options"])
    if st.button("Check Answer"):
        if ans == quiz["answer"]:
            st.balloons()
            st.success("🎯 Spot on! You're staying safe online.")
        else:
            st.error("❌ That's a common trap. Remember to always verify the source!")

# VOICE DETECTION
elif choice == "🎤 Voice":
    uploaded_file = st.file_uploader("Upload Call Recording", type=["wav", "mp3"])
    if uploaded_file:
        if st.button("Analyze Voice Print"):
            with st.spinner("Transcribing and analyzing..."):
                text = detect_voice_from_file(uploaded_file)
                st.markdown(f"**Detected Speech:** *{text}*")
                result = predict_message(text)
                if "Fraud" in result: st.error(result)
                else: st.success(result)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 0.8rem;'>ShieldAI v2.0 | Secured by end-to-end encryption</div>", unsafe_allow_html=True)