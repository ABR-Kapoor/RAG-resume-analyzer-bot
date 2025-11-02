import streamlit as st
from modules.query_handler import ask_question
from modules.vectorstore import get_session_id

def render_chat():
    """Render the chat interface"""
    
    # Get session ID
    session_id = get_session_id()
    
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if available
            if message["role"] == "assistant" and "sources" in message and message["sources"]:
                with st.expander("📎 View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.text(f"{i}. {source}")
    
    # Chat input
    if prompt := st.chat_input("Ask about the resumes... (e.g., 'Name all candidates', 'Compare their skills')"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = ask_question(prompt, session_id)
                    response = result.get("response", "Sorry, I couldn't process your question.")
                    sources = result.get("sources", [])
                    
                    st.markdown(response)
                    
                    # Show sources
                    if sources:
                        with st.expander("📎 View Sources"):
                            for i, source in enumerate(sources, 1):
                                st.text(f"{i}. {source}")
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "sources": sources
                    })
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg,
                        "sources": []
                    })
    
    # Clear chat button in sidebar
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
