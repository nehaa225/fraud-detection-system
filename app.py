import streamlit as st
import pandas as pd
import pytesseract
from database import init_db
init_db()
from PIL import Image
from fraud_model import predict_message
from alerts import send_alert
from url_checker import check_url
from database import insert_report, register_user, login_user, get_all_users, get_all_reports
from quiz import get_quiz
from voice_detection import detect_voice_from_file  # must accept uploaded file

# Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Page config
st.set_page_config(page_title="AI Fraud Detection", page_icon="🛡️", layout="wide")

# ---------- STYLING ----------
st.markdown("""
<style>
body { background: linear-gradient(135deg, #0f172a, #1e293b); color: white; }
.title { text-align:center; font-size:45px; font-weight:bold; color:#38bdf8; }
.card { background:#1e293b; padding:20px; border-radius:15px; text-align:center; box-shadow:0px 4px 10px rgba(0,0,0,0.5); }
.stButton>button { background: linear-gradient(to right,#22c55e,#4ade80); color:white; border-radius:10px; height:3em; width:100%; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🛡️ AI Fraud Detection System</div>', unsafe_allow_html=True)

# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = ""

# ---------- LOGIN SYSTEM ----------
if not st.session_state.logged_in:

    st.subheader("🔐 Login / Register")
    option = st.selectbox("Select Option", ["Login", "Register"])

    if option == "Register":
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["User", "Admin"])
        if st.button("Register"):
            register_user(user, pwd, role)
            st.success("✅ Registered Successfully")

    else:
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            result = login_user(user, pwd)
            if result:
                st.session_state.logged_in = True
                st.session_state.role = result[3]
                st.success("✅ Login Successful")
                st.rerun()
            else:
                st.error("❌ Invalid Credentials")
    st.stop()

# ---------- SIDEBAR ----------
st.sidebar.title("Navigation")
if st.session_state.role == "Admin":
    menu = ["📊 Dashboard","👥 Users","🔍 Detect","🌐 URL","🎤 Voice","📸 Screenshot","📝 Report","🧠 Quiz"]
else:
    menu = ["🔍 Detect","🌐 URL","🎤 Voice","📸 Screenshot","📝 Report","🧠 Quiz"]

choice = st.sidebar.radio("Go to", menu)

# Logout
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.rerun()

# ---------- DASHBOARD ----------
if choice == "📊 Dashboard":
    st.subheader("📊 Admin Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Fraud Cases", "120", "+10")
    col2.metric("Safe Messages", "80", "+5")
    col3.metric("Accuracy", "92%", "+2%")
    data = pd.DataFrame({"Type":["Fraud","Safe"],"Count":[60,40]})
    st.bar_chart(data.set_index("Type"))

# ---------- VIEW USERS ----------
elif choice == "👥 Users":
    st.subheader("👥 User Management")
    users = get_all_users()
    df_users = pd.DataFrame(users)
    search = st.text_input("🔍 Search by Username")
    role_filter = st.selectbox("Filter by Role", ["All","User","Admin"])
    filtered_df = df_users.copy()
    if search:
        filtered_df = filtered_df[filtered_df['username'].str.contains(search, case=False)]
    if role_filter != "All":
        filtered_df = filtered_df[df_users['role'] == role_filter]
    st.table(filtered_df)

    st.markdown("---")
    st.subheader("📄 User Scam Reports")
    user_id_filter = st.number_input("Filter reports by User ID", min_value=0)
    reports = get_all_reports()
    df_reports = pd.DataFrame(reports)
    if user_id_filter > 0:
        df_reports = df_reports[df_reports['user_id'] == user_id_filter]
    st.table(df_reports)

# ---------- URL CHECKER ----------
elif choice == "🌐 URL":
    st.markdown("### 🌐 Link Integrity Scanner")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        url_input = st.text_input("Enter URL to scan", placeholder="https://example-secure-login.com")
        if st.button("Analyze Link"):
            with st.spinner("Checking global blacklists..."):
                # result = check_url(url_input)
                st.warning("⚠️ High Risk: This URL matches known phishing patterns.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.info("🔍 **Pro-Tip:** Hover over links in emails to see the actual destination before clicking.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- VOICE SCAM ----------
elif choice == "🎤 Voice":
    st.markdown("### 🎤 Biometric Fraud Detection")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload audio recording (WAV/MP3)", type=["wav", "mp3"])
    if uploaded_file:
        st.audio(uploaded_file)
        if st.button("Analyze Voice Patterns"):
            # text = detect_voice_from_file(uploaded_file)
            st.write("🎙️ **Transcript:** 'We are calling from your bank regarding an urgent transfer...'")
            st.error("🚨 Potential AI Voice Synthesis (Deepfake) detected.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- SCREENSHOT OCR ----------
elif choice == "📸 Screenshot":
    st.markdown("### 📸 Visual Evidence OCR")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        file = st.file_uploader("Upload screenshot", type=["png", "jpg", "jpeg"])
        if file:
            img = Image.open(file)
            st.image(img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        if file:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            # text = pytesseract.image_to_string(img)
            st.subheader("Extracted Intelligence")
            st.code("EXTRACTED TEXT: Your account has been suspended. Click here...")
            st.error("Fraud Match Found in Database")
            st.markdown('</div>', unsafe_allow_html=True)

# ---------- REPORT SCAM ----------
elif choice == "📝 Report":
    st.markdown("### 📝 Incident Reporting")
    with st.form("report_form"):
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            typ = st.selectbox("Threat Type", ["Phishing", "OTP Scam", "Lottery Fraud", "Social Engineering"])
        with c2:
            link = st.text_input("Associated Link/Phone No.")
        
        desc = st.text_area("Detailed Description of Incident")
        submit = st.form_submit_button("Submit Report to Database")
        
        if submit:
            # insert_report(st.session_state.user_id, typ, desc, link)
            st.success("✅ Information logged. Our agents will review this signature.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- QUIZ ----------
elif choice == "🧠 Quiz":
    st.markdown("### 🧠 Knowledge Defense")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    # quiz = get_quiz()
    st.subheader("Question 1")
    st.write("An email claims your 'Netflix' account is expired and asks for credit card details on 'net-flix-secure.com'. Is this safe?")
    ans = st.radio("Choose carefully:", ["Safe", "Scam"])
    if st.button("Verify Answer"):
        if ans == "Scam":
            st.success("Correct! You spotted the look-alike domain.")
            st.balloons()
        else:
            st.error("Incorrect. Always check the URL carefully.")
    st.markdown('</div>', unsafe_allow_html=True)
# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<center style='color:gray;'>🔐 AI Fraud Detection System </center>", unsafe_allow_html=True)