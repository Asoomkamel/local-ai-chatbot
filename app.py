# app.py
import streamlit as st
import requests
from config import MODEL_OPTIONS, DEFAULT_MODEL, MAX_HISTORY_DEFAULT
from memory import init_memory, clear_memory, add_to_memory, get_limited_memory
from langchain_core.messages import HumanMessage

# Configure page
st.set_page_config(
    page_title="Local AI Chatbot",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Local AI Chatbot - Powered by LangChain, FastAPI, and ChromaDB"
    }
)

# Custom CSS for better styling
st.markdown("""
    <style>
        /* Main container styling */
        .main {
            padding-top: 2rem;
        }
        
        /* Chat message styling */
        .stChatMessage {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            padding: 2rem 1rem;
        }
        
        /* Developer section styling */
        .developer-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 0.75rem;
            color: white;
            margin-top: 2rem;
            text-align: center;
        }
        
        .developer-name {
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .developer-title {
            font-size: 0.9rem;
            opacity: 0.9;
            margin-bottom: 1rem;
        }
        
        .social-links {
            display: flex;
            justify-content: center;
            gap: 1rem;
        }
        
        .social-link {
            display: inline-block;
            width: 40px;
            height: 40px;
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background-color 0.3s;
            text-decoration: none;
            color: white;
            font-size: 1.5rem;
        }
        
        .social-link:hover {
            background-color: rgba(255, 255, 255, 0.4);
        }
        
        /* Upload section styling */
        .upload-section {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 0.75rem;
            margin-bottom: 1rem;
        }
        
        /* Settings section styling */
        .settings-section {
            background-color: #f9f9f9;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        
        /* Info box styling */
        .info-box {
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 1rem;
            border-radius: 0.25rem;
            margin-bottom: 1rem;
        }
        
        /* Success message styling */
        .success-message {
            background-color: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 1rem;
            border-radius: 0.25rem;
        }
    </style>
""", unsafe_allow_html=True)

import os
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
API_URL = f"http://{BACKEND_HOST}:8000/chat"
UPLOAD_URL = f"http://{BACKEND_HOST}:8000/upload-document"

# ---- UI Setup ---- #
st.title("🤖 Local AI Chatbot")
st.markdown("**Powered by:** Streamlit | FastAPI | LangChain | ChromaDB | Ollama")

# Initialize session state
init_memory(st.session_state)

# ---- Sidebar Configuration ---- #
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Settings section
    with st.container():
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        
        MODEL = st.selectbox(
            "🧠 Select LLM Model",
            MODEL_OPTIONS,
            index=0,
            help="Choose the language model to use for generating responses"
        )
        
        MAX_HISTORY = st.slider(
            "📝 Conversation History Length",
            min_value=1,
            max_value=20,
            value=MAX_HISTORY_DEFAULT,
            help="Number of previous messages to consider for context"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Clear history button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_memory(st.session_state)
            st.rerun()
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # Knowledge Base section
    st.header("📚 Knowledge Base")
    
    with st.expander("📄 Upload Documents", expanded=False):
        uploaded_file = st.file_uploader(
            "Choose a file (PDF or TXT)",
            type=["pdf", "txt"],
            help="Upload documents to expand the chatbot's knowledge base"
        )
        
        if uploaded_file is not None:
            file_details = f"""
            **File Details:**
            - Name: {uploaded_file.name}
            - Size: {uploaded_file.size / 1024:.2f} KB
            - Type: {uploaded_file.type}
            """
            st.info(file_details)
            
            if st.button("✅ Add to Knowledge Base", use_container_width=True):
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    try:
                        response = requests.post(UPLOAD_URL, files=files)
                        if response.status_code == 200:
                            st.success(f"✨ Successfully added {uploaded_file.name} to the knowledge base!")
                        else:
                            st.error(f"❌ Failed to add document: {response.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("🚨 Could not connect to the Backend API. Is api.py running?")
    
    st.divider()
    
    # Chat history viewer
    with st.expander("💬 View Chat History", expanded=False):
        if not st.session_state.chat_history:
            st.caption("💭 No messages yet. Start a conversation!")
        else:
            for i, msg in enumerate(st.session_state.chat_history):
                role = "👤 You" if isinstance(msg, HumanMessage) else "🤖 Assistant"
                preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                st.markdown(f"**{role}:** {preview}")
            
            st.divider()
            st.caption(f"📊 Total messages: {len(st.session_state.chat_history)}")
    
    st.divider()
    
    # Developer section
    st.markdown("""
        <div class="developer-section">
            <div class="developer-title">👨‍💻 Developer</div>
            <div class="developer-name">Eng Mutasim Alkamil</div>
            <div style="margin-top: 1rem;">
                <a href="https://github.com/Asoomkamel" target="_blank" style="text-decoration: none; color: white; margin: 0 0.5rem; font-size: 1.5rem;">
                    <span>🐙</span>
                </a>
                <a href="https://www.linkedin.com/in/mutasim-al-kamil-40a299318" target="_blank" style="text-decoration: none; color: white; margin: 0 0.5rem; font-size: 1.5rem;">
                    <span>💼</span>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ---- Main Chat Area ---- #
st.header("💬 Conversation")

# Display chat messages
for msg in st.session_state.chat_history:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role, avatar="👤" if role == "user" else "🤖"):
        st.markdown(msg.content)

# Chat input and processing
if user_input := st.chat_input("Type your message here...", key="chat_input"):
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    
    # Display assistant response
    with st.chat_message("assistant", avatar="🤖"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Prepare the request
        recent_memory = get_limited_memory(st.session_state, MAX_HISTORY)
        api_history = [
            {
                "role": "user" if isinstance(m, HumanMessage) else "assistant",
                "content": m.content
            }
            for m in recent_memory
        ]
        
        payload = {
            "input": user_input,
            "model": MODEL,
            "chat_history": api_history
        }
        
        # Call the backend API
        try:
            with requests.post(API_URL, json=payload, stream=True, timeout=60) as response:
                if response.status_code == 200:
                    # Stream the response
                    for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                        if chunk:
                            full_response += chunk
                            response_placeholder.markdown(full_response + "▌")
                else:
                    st.error(f"❌ API Error: {response.status_code} - {response.text}")
                    full_response = f"Error: {response.status_code}"
        except requests.exceptions.ConnectionError:
            st.error("🚨 Could not connect to the Backend API. Is api.py running?")
            full_response = "Connection Error: Backend API is not running"
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timeout. The backend took too long to respond.")
            full_response = "Timeout Error: Backend response took too long"
        
        # Finalize response
        response_placeholder.markdown(full_response)
    
    # Add to memory and rerun
    if full_response and not full_response.startswith("Error") and not full_response.startswith("Connection"):
        add_to_memory(st.session_state, user_input, full_response)
        st.rerun()

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #888; font-size: 0.85rem; margin-top: 2rem;">
        <p>🔒 <strong>Privacy First:</strong> All processing happens locally on your machine</p>
        <p>⚡ <strong>Powered by:</strong> Streamlit • FastAPI • LangChain • ChromaDB • Ollama</p>
    </div>
""", unsafe_allow_html=True)
