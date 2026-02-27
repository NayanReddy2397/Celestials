import streamlit as st
import time
import google.generativeai as genai
import uuid

st.set_page_config(layout="wide")

# -------------------- Styling --------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at 20% 30%, #1e1b4b, transparent 40%),
                radial-gradient(circle at 80% 70%, #0f766e, transparent 40%),
                linear-gradient(135deg, #0f172a, #020617);
    color: white;
}
.block-container {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border-radius: 15px;
    padding: 2rem;
    border: 1px solid rgba(255,255,255,0.1);#tech stack,problem statement,core functionality explanation
}
</style>
""", unsafe_allow_html=True)

# -------------------- Gemini Setup --------------------
genai.configure(api_key="AIzaSyAFm8eHbKs__kvU9xngyWdZWUWpB708zHw")
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------- Session Storage --------------------
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.current_chat = new_id
    st.session_state.chats[new_id] = []

# -------------------- Sidebar --------------------
with st.sidebar:
    st.header("⚙ Settings")

    language = st.selectbox(
        "Select Programming Language",
        ["Python", "C++", "Java", "JavaScript", "C", "Go", "Rust"]
    )

    st.markdown("---")
    st.header("💬 Previous Chats")

    for chat_id in st.session_state.chats.keys():
        if st.button(f"Chat {list(st.session_state.chats.keys()).index(chat_id)+1}"):
            st.session_state.current_chat = chat_id

    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.chats[new_id] = []
        st.session_state.current_chat = new_id

# -------------------- Header --------------------
st.markdown("""
<h1 style='text-align:center;
background: linear-gradient(90deg,#FF6B6B,#FFD93D);
-webkit-background-clip:text;
color:transparent;'>
🚀 Celestials CodeRefine
</h1>
<p style='text-align:center;font-size:18px;color:white;'>
AI-powered code review & optimization engine
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# -------------------- Display Current Chat --------------------
current_chat = st.session_state.current_chat
messages = st.session_state.chats[current_chat]

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------- Chat Input --------------------
code_input = st.chat_input("💻 Paste your unoptimized code here...")

if code_input:
    messages.append({
        "role": "user",
        "content": f"```{language.lower()}\n{code_input}\n```"
    })

    prompt = f"""
    You are a senior software engineer specialized in {language}.

    Analyze and optimize the following {language} code.

    Return strictly in this format:
    -->no comments in the code
    Original Code:
    {code_input}

    Optimized Code:
    <optimized {language} code>
    """

    with st.chat_message("assistant"):
        with st.spinner(f"🔍 CodeRefine AI is analyzing your {language} code..."):
            response = model.generate_content(prompt)
            time.sleep(2)
            st.markdown(response.text)

    messages.append({
        "role": "assistant",
        "content": response.text
    })

# -------------------- Clear Current Chat --------------------
st.markdown("---")
if st.button("🗑 Clear Current Chat"):
    st.session_state.chats[current_chat] = []
    st.rerun()
