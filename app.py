import streamlit as st
import os
from components.upload import render_uploader
from components.chat import render_chat

# Page configuration
st.set_page_config(
    page_title="Noddy Bot - Resume Analyzer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">🤖 Noddy Bot - AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by Groq LLaMA 3.3 & Pinecone Vector DB</div>', unsafe_allow_html=True)

# Sidebar - Document Manager
render_uploader()

# Main content - Chat Interface
render_chat()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>"
    "💡 Developed by <b>Abeer Kapoor</b> | "
    "Using Groq API + HuggingFace Embeddings + Pinecone"
    "</div>",
    unsafe_allow_html=True
)
