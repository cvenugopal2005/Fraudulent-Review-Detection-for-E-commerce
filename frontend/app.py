import sys
import os
import requests
import streamlit as st

# ----------------------------
# FIX IMPORT PATH
# ----------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from chatbot.rag_chatbot import ask_chatbot

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="FraudDetect AI",
    page_icon="🛒",
    layout="wide"
)

# ----------------------------
# HIDE STREAMLIT UI
# ----------------------------
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
body, .main {
    background: radial-gradient(#0A0F1F, #1A1037);
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# CUSTOM CSS
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&family=Rajdhani:wght@400;600&display=swap');

h1,h2,h3 {
    font-family:'Orbitron', monospace;
    text-align:center;
    color:#00E5FF;
}

.card {
    background: linear-gradient(135deg, #1A1037, #2E1B5B);
    border-radius:15px;
    padding:20px;
    box-shadow:0 0 15px rgba(0,0,0,0.6);
    margin-bottom:20px;
}

.stButton>button {
    background: linear-gradient(135deg,#14FFEC,#7F5AF0);
    color:#0A0F1F;
    font-weight:700;
    border-radius:10px;
    width:100%;
}

/* Floating chatbot */
.chatbot-box {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 360px;
    background: linear-gradient(135deg,#1A1037,#3A1C60);
    border-radius:15px;
    padding:15px;
    box-shadow:0 0 25px rgba(0,0,0,0.8);
    z-index: 9999;
}

.chatbot-title {
    color:#14FFEC;
    font-weight:700;
    margin-bottom:10px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# SESSION STATE
# ----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================================
# MAIN PAGE — REVIEW DETECTION
# ==========================================================
st.title("🛒 Fraudulent Review Detection System")
st.markdown(
    "Analyze e-commerce reviews for authenticity using **AI & Machine Learning**."
)

st.markdown('<div class="card">', unsafe_allow_html=True)
review_text = st.text_area("Enter product review text", height=120)
detect_btn = st.button("🔍 Check Authenticity")
st.markdown('</div>', unsafe_allow_html=True)

if detect_btn and review_text.strip():
    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json={"review": review_text}
        ).json()

        label = response.get("label", "Unknown")
        confidence = response.get("confidence", 0.0)

        color = "#4CAF50" if label == "Genuine Review" else "#F44336"

        st.session_state.history.insert(0, {
            "review": review_text,
            "label": label,
            "confidence": confidence
        })

        st.markdown(f"""
        <div class="card" style="background:{color}; color:white;">
            <h3>{label}</h3>
            <p>Confidence Score: {confidence:.2f}%</p>
        </div>
        """, unsafe_allow_html=True)

    except:
        st.error("Backend not reachable. Please start FastAPI server.")

if st.session_state.history:
    st.markdown("### 🕒 Recent Reviews")
    for item in st.session_state.history[:5]:
        st.markdown(f"""
        <div class="card">
            <b>Review:</b> {item['review']}<br>
            <b>Prediction:</b> {item['label']} ({item['confidence']:.2f}%)
        </div>
        """, unsafe_allow_html=True)

# ==========================================================
# FLOATING CHATBOT (BOTTOM RIGHT)
# ==========================================================
st.markdown("""
<div class="chatbot-box">
    <div class="chatbot-title">🤖 AI Assistant</div>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown(
        "<div class='chatbot-box'>", unsafe_allow_html=True
    )
    user_q = st.text_input(
        "Ask a question",
        placeholder="e.g. My product is defective, what should I do?"
    )
    ask_btn = st.button("💬 Ask")

    if ask_btn and user_q.strip():
        with st.spinner("Thinking..."):
            answer = ask_chatbot(user_q)
            st.session_state.chat_history.insert(0, {
                "q": user_q,
                "a": answer
            })

    if st.session_state.chat_history:
        chat = st.session_state.chat_history[0]
        st.markdown(f"""
        <hr>
        <b>Q:</b> {chat['q']}<br><br>
        <b>A:</b> {chat['a']}
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
