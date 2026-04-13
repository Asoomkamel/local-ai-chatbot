# memory.py

from langchain_core.messages import HumanMessage, AIMessage

def init_memory(session_state):
    if "chat_history" not in session_state:
        session_state.chat_history = []

def clear_memory(session_state):
    session_state.chat_history = []

def add_to_memory(session_state, user_input, ai_response):
    session_state.chat_history.append(HumanMessage(content=user_input))
    session_state.chat_history.append(AIMessage(content=ai_response))

def get_limited_memory(session_state, max_history):
    return session_state.chat_history[-(max_history * 2):]