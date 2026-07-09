import streamlit as st
import time
import os
from rag_pipeline import create_vectorstore, get_answer
from utils import save_conversation, load_conversations, create_new_chat, load_specific_chat

st.set_page_config(page_title="DocuMind", page_icon="🧠")

st.markdown("""
<style>
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }
.block-container { padding-top: 1rem !important; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    border-right: 1px solid rgba(255,255,255,0.1);
}

h1 {
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(167,139,250,0.4);
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.1);
    margin: 8px 0;
    padding: 8px;
}

[data-testid="stFileUploader"] {
    background: rgba(167,139,250,0.1);
    border-radius: 12px;
    border: 2px dashed rgba(167,139,250,0.4);
}

.stSuccess {
    background: rgba(52,211,153,0.1);
    border-radius: 12px;
}

[data-testid="stChatInput"] { border-radius: 20px; }
[data-testid="stChatInput"] textarea {
    border: 2px solid rgba(167,139,250,0.5) !important;
    border-radius: 20px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 DocuMind")
st.caption("*Your AI-powered document companion*")

if "conversations" not in st.session_state:
    st.session_state.conversations = load_conversations()
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "show_suggestions" not in st.session_state:
    st.session_state.show_suggestions = False
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None

with st.sidebar:
    st.markdown("### 🧠 DocuMind")
    st.caption("Your document companion")
    st.divider()

    if st.button("+New Chat"):
        st.session_state.current_chat = None
        st.session_state.vectorstore = None
        st.session_state.show_suggestions = False

    st.divider()

    uploaded_file = st.file_uploader("📎 Upload a document", type=["pdf","txt","docx","xlsx","csv","png","jpg","jpeg"], label_visibility="collapsed")

    st.divider()

    for conversation in st.session_state.conversations:
        col1, col2 = st.columns([8, 2])
        with col1:
            if st.button(conversation["title"], key=conversation["id"]):
                st.session_state.current_chat = conversation
        with col2:
            if st.button("🗑", key=f"del_{conversation['id']}"):
                os.remove(f"conversations/{conversation['id']}.json")
                st.session_state.conversations = load_conversations()
                st.session_state.current_chat = None
                st.rerun()

if st.session_state.current_chat is not None:
    messages = st.session_state.current_chat["messages"]
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if uploaded_file is not None and uploaded_file.name != st.session_state.get("uploaded_filename", ""):
    st.session_state.show_suggestions = False
    with st.spinner("Processing document..."):
        import tempfile
        original_name = uploaded_file.name
        file_extension = original_name.split(".")[-1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        try:
            st.session_state.vectorstore = create_vectorstore(tmp_path, file_extension)
            st.session_state.uploaded_filename = original_name
            st.session_state.show_suggestions = True
            st.success(f"✅ {original_name} uploaded successfully!")
            st.balloons()
            with st.chat_message("assistant"):
                st.write(f"🎉 **{original_name}** is ready! What would you like me to do?")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
        finally:
            os.unlink(tmp_path)

if st.session_state.show_suggestions:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄 Summarize", use_container_width=True):
            st.session_state.quick_prompt = "Summarize this document."
        if st.button("📝 Bullet Points", use_container_width=True):
            st.session_state.quick_prompt = "Create bullet-point notes."
        if st.button("🧒 Explain Simply", use_container_width=True):
            st.session_state.quick_prompt = "Explain this document in simple language."
    with col2:
        if st.button("🎯 Key Takeaways", use_container_width=True):
            st.session_state.quick_prompt = "What are the key takeaways?"
        if st.button("🔍 Find Important Info", use_container_width=True):
            st.session_state.quick_prompt = "Find all important dates, names, and numbers."
        if st.button("💬 Other", use_container_width=True):
            st.info("Type any question in the chat box below 👇")

user_input = st.session_state.pop("quick_prompt", None)
if user_input is None:
    user_input = st.chat_input("Ask anything about your document...")

if user_input:
    if st.session_state.current_chat is None:
        st.session_state.current_chat = create_new_chat()

    with st.chat_message("user"):
        st.write(user_input)

    answer, sources = get_answer(user_input, st.session_state.vectorstore)

    with st.chat_message("assistant"):
        if any(line.strip().startswith(('-', '*', '#')) for line in answer.split('\n')):
            st.markdown(answer)
        else:
            placeholder = st.empty()
            streamed_text = ""
            for word in answer.split():
                streamed_text += word + " "
                placeholder.markdown(streamed_text + "▌")
                time.sleep(0.03)
            placeholder.markdown(streamed_text)

        if sources:
            filename = st.session_state.get("uploaded_filename", "Uploaded document")
            st.write(f"📚 **Source:** {filename}")

    st.session_state.current_chat["messages"].append({"role": "user", "content": user_input})
    st.session_state.current_chat["messages"].append({"role": "assistant", "content": answer})

    if st.session_state.current_chat["title"] == "New Chat":
        st.session_state.current_chat["title"] = user_input[:30] + "..." if len(user_input) > 30 else user_input

    save_conversation(st.session_state.current_chat)