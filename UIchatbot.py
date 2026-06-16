
import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# ---------------------------
# Load Environment Variables
# ---------------------------
load_dotenv()

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="AI Personality Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------
# Custom CSS
# ---------------------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

.chat-title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    color:white;
}

.chat-subtitle{
    text-align:center;
    color:#cbd5e1;
    margin-bottom:20px;
}

.stChatMessage{
    border-radius:15px;
    padding:10px;
}

.mode-box{
    padding:10px;
    border-radius:12px;
    background:#1e293b;
    color:white;
    text-align:center;
    font-size:18px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Model
# ---------------------------
model = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.9,
    max_tokens=50
)

# ---------------------------
# Header
# ---------------------------
st.markdown(
    "<div class='chat-title'>🤖 AI Personality Chatbot</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='chat-subtitle'>Choose a personality and start chatting</div>",
    unsafe_allow_html=True
)

# ---------------------------
# Sidebar
# ---------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    choice = st.radio(
        "Choose AI Personality",
        [
            "😡 Angry Mode",
            "😂 Funny Mode",
            "😢 Sad Mode",
            "😊 Happy Mode"
        ]
    )

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------
# Personality Selection
# ---------------------------
if choice == "😡 Angry Mode":
    mode = "You have chosen Angry mode"

elif choice == "😂 Funny Mode":
    mode = "You have chosen Funny mode"

elif choice == "😢 Sad Mode":
    mode = "You have chosen Sad mode"

else:
    mode = "You have chosen Happy mode"

# ---------------------------
# Session State
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content=mode)
    ]

# Update system prompt if mode changes
if st.session_state.messages:
    st.session_state.messages[0] = SystemMessage(content=mode)

# ---------------------------
# Current Mode Display
# ---------------------------
st.markdown(
    f"<div class='mode-box'>{choice}</div>",
    unsafe_allow_html=True
)

st.write("")

# ---------------------------
# Display Chat History
# ---------------------------
for msg in st.session_state.messages:

    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

# ---------------------------
# Chat Input
# ---------------------------
prompt = st.chat_input("Type your message here...")

if prompt:

    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            response = model.invoke(
                st.session_state.messages
            )

            st.session_state.messages.append(
                AIMessage(content=response.content)
            )

            st.write(response.content)

