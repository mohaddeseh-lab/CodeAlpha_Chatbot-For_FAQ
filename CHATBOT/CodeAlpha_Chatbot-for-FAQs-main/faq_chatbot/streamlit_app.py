"""
streamlit_app.py
-----------------
Alternative chat UI built with Streamlit (simpler to run than Flask).

Install:  pip install streamlit
Run:      streamlit run streamlit_app.py
"""

import streamlit as st

from chatbot import FAQChatBot
from faq_data import FAQS

st.set_page_config(page_title="EduLearn Help Desk", page_icon="💬")

st.title("💬 EduLearn Help Desk")
st.caption("Ask a question about accounts, courses, payments, certificates, and more. "
           "Answers are matched from our FAQ library using TF-IDF + cosine similarity.")


@st.cache_resource
def load_bot():
    return FAQChatBot()


bot = load_bot()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! What can I help you with today?"}
    ]

# Sidebar: sample questions you can click
with st.sidebar:
    st.subheader("Try asking:")
    for faq in FAQS[:8]:
        if st.button(faq["question"], use_container_width=True):
            st.session_state.pending_question = faq["question"]

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


def handle_question(question: str):
    st.session_state.messages.append({"role": "user", "content": question})
    result = bot.get_response(question)
    st.session_state.messages.append({"role": "assistant", "content": result.answer})


# Handle a click from the sidebar
if "pending_question" in st.session_state:
    handle_question(st.session_state.pop("pending_question"))
    st.rerun()

# Chat input box
user_question = st.chat_input("Type your question here...")
if user_question:
    handle_question(user_question)
    st.rerun()