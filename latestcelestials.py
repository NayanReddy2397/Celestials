import streamlit as st
import time
import google.generativeai as genai
import uuid

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Celestials CodeRefine", page_icon="🚀", layout="wide")

# ================= CSS =================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 20% 30%, #1e1b4b, transparent 40%),
                radial-gradient(circle at 80% 70%, #0f766e, transparent 40%),
                linear-gradient(135deg, #0f172a, #020617);
    color:white;
}

.block-container {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding:2rem;
    border:1px solid rgba(255,255,255,0.08);
}

[data-testid="stChatMessage"]{
    background: rgba(255,255,255,0.05);
    border-radius:15px;
    padding:15px;
}

.card{
    padding:20px;
    border-radius:15px;
    background:rgba(255,255,255,0.05);
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ================= GEMINI =================
genai.configure(api_key="AIzaSyB6nOPW_JDMigbpaOmRLztiSRau_cXp1sw")
model = genai.GenerativeModel("gemini-2.5-flash")

# ================= SESSION =================
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    cid = str(uuid.uuid4())
    st.session_state.current_chat = cid
    st.session_state.chats[cid] = []

# ================= SIDEBAR =================
with st.sidebar:
    st.title("⚙ Control Panel")

    language = st.selectbox("Language", ["Python","C++","Java","JavaScript","C","Go","Rust"])

    st.divider()
    st.subheader("Modes")

    detect_bugs = st.checkbox("🐞 Bug Detection", True)
    explain = st.checkbox("📘 Explanation", True)
    score_mode = st.checkbox("📊 Performance Score", True)

    st.divider()
    st.subheader("Chats")

    for cid in st.session_state.chats:
        if st.button(f"Chat {list(st.session_state.chats).index(cid)+1}"):
            st.session_state.current_chat = cid

    if st.button("➕ New Chat"):
        cid = str(uuid.uuid4())
        st.session_state.chats[cid] = []
        st.session_state.current_chat = cid
        st.rerun()

# ================= HEADER =================
st.markdown("""
<h1 style='text-align:center;background: linear-gradient(90deg,#ff6b6b,#ffd93d,#6bcBef);
-webkit-background-clip:text;color:transparent;'>🚀 Celestials CodeRefine Ultra</h1>
<p style='text-align:center'>Next-gen AI Code Review & Optimization Engine</p>
""", unsafe_allow_html=True)

# ================= FEATURES =================
c1,c2,c3,c4 = st.columns(4)

c1.markdown("<div class='card'>⚡ Instant Optimization</div>", unsafe_allow_html=True)
c2.markdown("<div class='card'>🧠 AI Intelligence</div>", unsafe_allow_html=True)
c3.markdown("<div class='card'>🔒 Secure Review</div>", unsafe_allow_html=True)
c4.markdown("<div class='card'>📊 Performance Insights</div>", unsafe_allow_html=True)

st.divider()

# ================= CHAT =================
current_chat = st.session_state.current_chat
messages = st.session_state.chats[current_chat]

for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================= INPUT =================
code_input = st.chat_input("Paste code...")

if code_input:
    messages.append({"role":"user","content":f"```{language.lower()}\n{code_input}\n```"})

    prompt = f"""
You are CodeRefine Ultra.

Perform:
- Optimization
- Complexity analysis
- Bug detection if enabled
- Score evaluation
- Explanation if enabled

Return STRICT:

Original Code:
{code_input}

Optimized Code:

Complexity:

Bugs:

Score:

Explanation:
"""

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = model.generate_content(prompt)
            result = response.text
            st.markdown(result)

    messages.append({"role":"assistant","content":result})

    # ================= DIFF =================
    if "Optimized Code:" in result:
        try:
            original = result.split("Optimized Code:")[0].replace("Original Code:","")
            optimized = result.split("Optimized Code:")[1].split("Complexity:")[0]

            st.subheader("Side-by-Side Diff")
            d1,d2 = st.columns(2)
            d1.code(original, language=language.lower())
            d2.code(optimized, language=language.lower())

            st.download_button("⬇ Download Optimized", optimized, file_name="optimized.txt")

        except:
            pass

# ================= CLEAR =================
if st.button("🗑 Clear Chat"):
    st.session_state.chats[current_chat] = []
    st.rerun()
