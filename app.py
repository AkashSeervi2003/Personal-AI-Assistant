import streamlit as st
from typing import List
from src.processor import PDFProcessor
from src.embedding import EmbeddingManager
from src.chat import ChatManager
from src.config import Config
from src.history import UserHistoryManager
from src.ui.theme import inject_global_css, app_header

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

history_manager = UserHistoryManager()

def initialize_session_state() -> bool:
    """Initialize core objects and session keys."""
    if "processor" not in st.session_state:
        st.session_state.processor = PDFProcessor()
    if "embedding_manager" not in st.session_state:
        st.session_state.embedding_manager = EmbeddingManager()
    if "chat_manager" not in st.session_state:
        if not Config.is_valid() or not Config.GOOGLE_API_KEY:
            st.error("Missing API key. Please set GEMINI_API_KEY in .env")
            return False
        st.session_state.chat_manager = ChatManager(Config.GOOGLE_API_KEY)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "documents" not in st.session_state:
        st.session_state.documents = []
    if "username" not in st.session_state:
        st.session_state.username = None
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = None
    elif st.session_state.username and not st.session_state.messages:
        load_current_conversation(st.session_state.username)
    return True

# ---------------- Conversation / History Helpers -----------------

def load_chat_history(username: str):
    """Legacy load of last conversation into messages list."""
    try:
        history = history_manager.fetch_history(username, limit=50)
        messages: List[dict] = []
        for question, answer, _ts in reversed(history):
            messages.append({"role": "user", "content": question})
            messages.append({"role": "assistant", "content": answer})
        st.session_state.messages = messages
    except Exception as e:  # pragma: no cover
        st.error(f"Error loading chat history: {e}")


def load_current_conversation(username: str):
    """Load most recent conversation and populate messages."""
    try:
        conversations = history_manager.get_conversations(username)
        if conversations:
            convo_id = conversations[0][0]
            st.session_state.current_conversation_id = convo_id
            data = history_manager.get_conversation_messages(convo_id)
            st.session_state.messages = [
                {"role": role, "content": content} for role, content, _ts in data
            ]
        else:
            convo_id = history_manager.create_conversation(username, "New Conversation")
            st.session_state.current_conversation_id = convo_id
            st.session_state.messages = []
    except Exception as e:  # pragma: no cover
        st.error(f"Error loading conversation: {e}")


def load_conversation(conversation_id: int):
    """Switch to a specific conversation id."""
    try:
        data = history_manager.get_conversation_messages(conversation_id)
        st.session_state.messages = [
            {"role": role, "content": content} for role, content, _ts in data
        ]
        st.session_state.current_conversation_id = conversation_id
    except Exception as e:  # pragma: no cover
        st.error(f"Error loading conversation: {e}")


def create_new_conversation(username: str) -> int:
    """Create a new empty conversation and reset chat manager memory."""
    convo_id = history_manager.create_conversation(username)
    st.session_state.current_conversation_id = convo_id
    st.session_state.messages = []
    st.session_state.chat_manager.reset_conversation()
    return convo_id

# ---------------- Document Processing -----------------

def process_documents(uploaded_files: List) -> bool:
    """Process uploaded PDFs, build embeddings, wire retriever."""
    try:
        with st.spinner("Processing documents..."):
            all_docs = []
            for file in uploaded_files:
                docs = st.session_state.processor.process_document(file)
                all_docs.extend(docs)
            st.session_state.documents = all_docs
            success = st.session_state.embedding_manager.create_embeddings(all_docs)
            if success:
                st.session_state.chat_manager.set_retriever(
                    st.session_state.embedding_manager.retriever
                )
                st.success(f"Processed {len(all_docs)} chunks")
                return True
            st.error("Failed to create embeddings")
            return False
    except Exception as e:
        st.error(f"Error processing documents: {e}")
        return False

# ---------------- Auth / Login -----------------

def show_login_page():
    """Render split hero + auth card using Streamlit columns (white background)."""
    col1, col2 = st.columns([1.05, 1])
    with col1:
        st.markdown(
            """
            <div class="auth-hero">
                            <div class="auth-hero-border"></div>
              <div class="auth-hero-icon">🤖</div>
              <h2>Unlock Knowledge,<br/>Chat Smarter</h2>
              <p>Your AI-powered document companion. Upload PDFs and get instant, contextual answers.</p>
              <p style="opacity:.85">Secure, fast, and memory-aware RAG chat for your workflow.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        # Sentinel + container approach so tabs truly render inside the visual card
        st.markdown('<span class="auth-card-sentinel"></span>', unsafe_allow_html=True)
        # Wrap all right-column content in a container immediately after sentinel to get gradient border
        with st.container():
            st.markdown('<div class="auth-card-border"></div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div class=\"auth-brand\">ScrapMate</div>
                <div class=\"auth-subtitle\">Welcome! Sign in to continue your journey</div>
                """,
                unsafe_allow_html=True,
            )
            tab_login, tab_signup = st.tabs(["Login", "Sign Up"])
            with tab_login:
                username = st.text_input("Username", key="login_username", placeholder="Enter username")
                password = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")
                if st.button("Login", key="btn_login"):
                    if not username or not password:
                        st.error("Fill all fields")
                    elif history_manager.login(username, password):
                        st.success("Logged in")
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
            with tab_signup:
                su_username = st.text_input("Username", key="signup_username", placeholder="Choose a username")
                su_password = st.text_input("Password", type="password", key="signup_password", placeholder="Create a password")
                su_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm", placeholder="Confirm password")
                if st.button("Create Account", key="btn_signup"):
                    if not su_username or not su_password:
                        st.error("Fill all fields")
                    elif len(su_password) < 6:
                        st.error("Password must be ≥ 6 chars")
                    elif su_password != su_confirm:
                        st.error("Passwords do not match")
                    else:
                        ok, msg = history_manager.signup(su_username, su_password)
                        if ok:
                            st.success("Account created. You can login now.")
                        else:
                            st.error(msg)
            st.markdown("""<div class=\"auth-footer\">🔒 Your conversations are private and stored locally.</div>""", unsafe_allow_html=True)

# ---------------- Sidebar -----------------

def render_sidebar():
    with st.sidebar:
        st.success(f"👤 {st.session_state.username}")
        # Use explicit keys to avoid StreamlitDuplicateElementId collisions
        if st.button("🚪 Logout", key="btn_logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown("---")
        st.header("Upload PDFs")
        uploads = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
        if uploads and st.button("Process Documents", key="btn_process_documents"):
            process_documents(uploads)
        if st.session_state.documents:
            st.success(f"{len(st.session_state.documents)} chunks ready")
            colA, colB = st.columns(2)
            with colA:
                if st.button("Clear Conversation", key="btn_clear_conversation"):
                    st.session_state.messages = []
                    st.session_state.chat_manager.reset_conversation()
                    st.rerun()
            with colB:
                if st.button("Clear File Chunks", key="btn_clear_chunks"):
                    st.session_state.documents = []
                    if hasattr(st.session_state.embedding_manager, "clear_embeddings"):
                        st.session_state.embedding_manager.clear_embeddings()
                    st.rerun()
        st.header("Conversations")
        if st.button("➕ New Conversation", key="btn_new_conversation"):
            create_new_conversation(st.session_state.username)
            st.rerun()
        if st.session_state.current_conversation_id:
            convs = history_manager.get_conversations(st.session_state.username)
        if st.session_state.current_conversation_id:
            conversations = history_manager.get_conversations(st.session_state.username)
            current_conv = next((conv for conv in conversations if conv[0] == st.session_state.current_conversation_id), None)
            if current_conv:
                st.subheader(f"Current: {current_conv[1]}")
                st.caption(f"Created: {current_conv[2][:19]}")

        st.markdown("---")

        # List all conversations
        conversations = history_manager.get_conversations(st.session_state.username)

        if conversations:
            st.subheader("Your Conversations")
            for conv_id, title, created_at, updated_at in conversations:
                is_current = conv_id == st.session_state.current_conversation_id
                c1, c2, c3 = st.columns([3, 1.3, 0.7])
                with c1:
                    label = f"💬 {title}"
                    if is_current:
                        st.markdown(
                            f"<div class='conv-item active'><div class='conv-title'>{label}</div></div>",
                            unsafe_allow_html=True,
                        )
                    else:
                        if st.button(label, key=f"open_{conv_id}"):
                            load_conversation(conv_id)
                            st.rerun()
                with c2:
                    st.caption(f"{updated_at[:19]}")
                with c3:
                    if st.button("🗑️", key=f"delete_{conv_id}"):
                        if st.session_state.current_conversation_id == conv_id:
                            st.warning("Cannot delete current conversation")
                        else:
                            history_manager.delete_conversation(conv_id)
                            st.rerun()
        else:
            st.info("No conversations yet. Start a new conversation!")

    # --- MAIN CHAT UI ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if query := st.chat_input("Ask your question"):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.write(query)

        if not st.session_state.documents:
            with st.chat_message("assistant"):
                st.write("Please upload and process PDF documents first!")
            st.session_state.messages.append({"role": "assistant", "content": "Please upload and process PDF documents first!"})
            return

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if hasattr(st.session_state.embedding_manager, 'retriever') and st.session_state.embedding_manager.retriever:
                    response = st.session_state.chat_manager.generate_response(query, [])
                else:
                    relevant_docs = st.session_state.embedding_manager.search(query)
                    response = st.session_state.chat_manager.generate_response(query, relevant_docs)
                
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Save to current conversation
                if st.session_state.current_conversation_id:
                    history_manager.save_message(st.session_state.current_conversation_id, "user", query)
                    history_manager.save_message(st.session_state.current_conversation_id, "assistant", response)
                else:
                    # Fallback to legacy method if no conversation exists
                    history_manager.save_history(st.session_state.username, query, response)

def main():
    """Main entry point: initialize, theme, auth gate, then render UI."""
    inject_global_css()
    init_ok = initialize_session_state()
    # Always allow reaching login UI even if API key missing
    if st.session_state.get("username") is None:
        show_login_page()
        return
    if not init_ok:
        # API key missing; stop after login page
        return
    app_header("📚 PDF Chat Assistant", "Chat with your PDFs using RAG")
    render_sidebar()

if __name__ == "__main__":
    main()