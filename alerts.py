import streamlit as st
import pandas as pd
import pytesseract
from PIL import Image

# Dummy imports for logic (Keep your existing imports)
# from database import init_db, insert_report, register_user, login_user, get_all_users, get_all_reports
# from fraud_model import predict_message
# ... (your other imports)

# Page config
st.set_page_config(page_title="Guardian AI", page_icon="🛡️", layout="wide")

# ---------- ENHANCED STYLING ----------
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #020617);
        color: #f8fafc;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
    }

    /* Gradient Title */
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* Buttons Customization */
    div.stButton > button {
        background: linear-gradient(45deg, #0284c7, #4f46e5);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
        background: linear-gradient(45deg, #0ea5e9, #6366f1);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] {
        color: #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<h1 class="main-title">🛡️ Guardian AI</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; font-size:1.1rem;'>Advanced Fraud Intelligence & Cyber Security Suite</p>", unsafe_allow_html=True)

# ---------- LOGIN SYSTEM (Refined) ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            user = st.text_input("Username", key="l_user")
            pwd = st.text_input("Password", type="password", key="l_pwd")
            if st.button("Access Dashboard"):
                # login_user(user, pwd) logic here
                st.session_state.logged_in = True
                st.session_state.role = "Admin" # Temporary
                st.rerun()
        
        with tab2:
            st.text_input("New Username")
            st.text_input("New Password", type="password")
            st.selectbox("Account Type", ["User", "Admin"])
            st.button("Create Account")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    menu_icons = {
        "📊 Dashboard": "📊", "🔍 Detect": "🔍", "🌐 URL": "🌐", 
        "🎤 Voice": "🎤", "📸 Screenshot": "📸", "📝 Report": "📝", "🧠 Quiz": "🧠"
    }
    
    if st.session_state.role == "Admin":
        menu = list(menu_icons.keys())
    else:
        menu = ["🔍 Detect", "🌐 URL", "🎤 Voice", "📸 Screenshot", "📝 Report", "🧠 Quiz"]

    choice = st.radio("Select Module", menu, label_visibility="collapsed")
    
    st.markdown("---")
    if st.button("🚪 Logout System"):
        st.session_state.logged_in = False
        st.rerun()

# ---------- MODULES ----------

if choice == "📊 Dashboard":
    st.markdown("### System Health & Analytics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Scans", "1,284", "+12%")
    c2.metric("Threats Blocked", "412", "+5%")
    c3.metric("System Uptime", "99.9%", "0.01%")
    c4.metric("User Trust", "94%", "+2%")
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📈 Threat Analysis Trend")
    chart_data = pd.DataFrame({"Day": ["Mon", "Tue", "Wed", "Thu", "Fri"], "Threats": [12, 45, 30, 70, 40]})
    st.area_chart(chart_data.set_index("Day"), color="#38bdf8")
    st.markdown('</div>', unsafe_allow_html=True)

elif choice == "🔍 Detect":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("💬 Message Analysis")
        msg = st.text_area("Paste suspicious text or SMS content here...", height=200)
        email = st.text_input("Notify me at (Email)")
        if st.button("Run Deep Scan"):
            # result = predict_message(msg)
            st.info("Analyzing content pattern...")
            st.success("Analysis Complete: 98% Probablity of Safety")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 💡 Tips")
        st.write("Fraudsters often use urgency (e.g., 'Act Now!') to trick you.")
        st.markdown('</div>', unsafe_allow_html=True)

# ... (Continue implementing other sections within <div class="glass-card">)

# ---------- FOOTER ----------
st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: #64748b; font-size: 0.8rem;">
        Powered by Guardian AI Engines • 2026 Security Protocol • v2.4.0
    </div>
""", unsafe_allow_html=True)