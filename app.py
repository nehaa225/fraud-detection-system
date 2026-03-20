import streamlit as st
import pandas as pd
import pytesseract
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

# ---------- DETECT ----------
elif choice == "🔍 Detect":
    st.subheader("🔍 Fraud Detection")
    msg = st.text_area("Enter Message")
    email = st.text_input("Email for Alert")
    if st.button("Analyze"):
        result = predict_message(msg)
        if "Fraud" in result: st.error(result)
        else: st.success(result)
        if "Fraud" in result and email: send_alert(email,msg); st.warning("📧 Alert Sent")

# ---------- URL ----------
elif choice == "🌐 URL":
    st.subheader("🌐 URL Checker")
    url = st.text_input("Enter URL")
    if st.button("Check URL"):
        result = check_url(url)
        if "Suspicious" in result: st.error(result)
        else: st.success(result)

# ---------- SCREENSHOT ----------
elif choice == "📸 Screenshot":
    st.subheader("📸 Screenshot Detection")
    file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])
    if file:
        img = Image.open(file)
        st.image(img)
        text = pytesseract.image_to_string(img)
        st.write("Extracted Text:", text)
        st.write(predict_message(text))

# ---------- REPORT ----------
elif choice == "📝 Report":
    st.subheader("📝 Report Scam")
    uid = st.number_input("User ID", min_value=1)
    typ = st.selectbox("Type", ["Phishing","OTP","Lottery"])
    desc = st.text_area("Description")
    link = st.text_input("Link")
    if st.button("Submit"):
        insert_report(uid, typ, desc, link)
        st.success("✅ Report Saved")

# ---------- QUIZ ----------
elif choice == "🧠 Quiz":
    st.subheader("🧠 Cyber Awareness Quiz")
    quiz = get_quiz()
    st.info(quiz["question"])
    ans = st.radio("Choose", quiz["options"])
    if st.button("Submit"):
        if ans == quiz["answer"]: st.success("✅ Correct"); st.balloons()
        else: st.error("❌ Wrong")

# ---------- VOICE ----------
elif choice == "🎤 Voice":
    st.subheader("🎤 Voice Scam Detection (Upload Audio)")
    uploaded_file = st.file_uploader("Upload your audio file (wav/mp3)", type=["wav","mp3"])
    if uploaded_file:
        if st.button("Analyze Audio"):
            text = detect_voice_from_file(uploaded_file)
            st.write("🗣 Detected Speech:")
            st.success(text)
            result = predict_message(text)
            if "Fraud" in result: st.error(result)
            else: st.success(result)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<center style='color:gray;'>🔐 AI Fraud Detection System </center>", unsafe_allow_html=True)