import streamlit as st
import os
from modules.vectorstore import upload_pdfs_to_vectorstore, get_session_id, clear_session_data

def list_uploaded_documents(session_id):
    """List PDFs for current session"""
    upload_dir = f"./uploaded_docs/{session_id}"
    if not os.path.exists(upload_dir):
        return []
    
    files = []
    for filename in os.listdir(upload_dir):
        if filename.endswith('.pdf'):
            filepath = os.path.join(upload_dir, filename)
            size_mb = round(os.path.getsize(filepath) / (1024 * 1024), 2)
            files.append({
                'filename': filename,
                'size_mb': size_mb,
                'path': filepath
            })
    
    # Sort by filename
    files.sort(key=lambda x: x['filename'])
    return files

def render_uploader():
    st.sidebar.header("📚 Document Manager")
    
    # Get session ID
    session_id = get_session_id()
    
    # Show session info
    st.sidebar.caption(f"🔒 Session: {session_id[:8]}...")
    
    # Show already uploaded documents for this session
    st.sidebar.subheader("Your Uploaded PDFs")
    uploaded_docs = list_uploaded_documents(session_id)
    
    if uploaded_docs:
        st.sidebar.success(f"✅ {len(uploaded_docs)} document(s) in your session")
        for doc in uploaded_docs:
            with st.sidebar.expander(f"📄 {doc['filename']}"):
                st.write(f"**Size:** {doc['size_mb']} MB")
    else:
        st.sidebar.info("📭 No documents uploaded yet")
    
    st.sidebar.markdown("---")
    
    # Upload new documents
    st.sidebar.subheader("Upload New PDFs")
    uploaded_files = st.sidebar.file_uploader(
        "Upload multiple PDFs",
        type="pdf",
        accept_multiple_files=True,
        key="pdf_uploader"
    )
    
    if uploaded_files:
        st.sidebar.info(f"📁 {len(uploaded_files)} file(s) selected")
        for f in uploaded_files:
            st.sidebar.text(f"  • {f.name}")
    
    if st.sidebar.button("Upload to Database") and uploaded_files:
        with st.spinner(f"Uploading {len(uploaded_files)} file(s)..."):
            try:
                # Create session-specific directory
                upload_dir = f"./uploaded_docs/{session_id}"
                os.makedirs(upload_dir, exist_ok=True)
                
                saved_files = []
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(upload_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    saved_files.append(file_path)
                
                # Process and upload to vector store with session isolation
                result = upload_pdfs_to_vectorstore(saved_files, session_id)
                
                st.sidebar.success(f"✅ Successfully processed {len(uploaded_files)} PDF file(s)")
                st.sidebar.write("Files processed:")
                for fname in [f.name for f in uploaded_files]:
                    st.sidebar.write(f"  • {fname}")
                
                st.sidebar.info("ℹ️ Only your uploaded documents are visible to you")
                
                # Clear the uploader and refresh
                st.rerun()
                
            except Exception as e:
                st.sidebar.error(f"Error uploading files: {str(e)}")

    # Allow user to clear their own session data (namespace + uploaded files)
    if st.sidebar.button("🧹 Clear my session data"):
        with st.spinner("Clearing your session data..."):
            try:
                # Clear vectors in Pinecone for this session
                clear_session_data(session_id)

                # Remove uploaded files for this session
                upload_dir = f"./uploaded_docs/{session_id}"
                if os.path.exists(upload_dir):
                    for fname in os.listdir(upload_dir):
                        fp = os.path.join(upload_dir, fname)
                        if os.path.isfile(fp):
                            os.remove(fp)

                st.sidebar.success("✅ Your session data was cleared. No documents available.")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"Error clearing session data: {str(e)}")
