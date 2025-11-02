import streamlit as st
import os
from modules.vectorstore import upload_pdfs_to_vectorstore

def list_uploaded_documents():
    """List all PDFs in uploaded_docs directory"""
    upload_dir = "./uploaded_docs"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
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
    
    # Show already uploaded documents
    st.sidebar.subheader("Already Uploaded PDFs")
    uploaded_docs = list_uploaded_documents()
    
    if uploaded_docs:
        st.sidebar.success(f"✅ {len(uploaded_docs)} document(s) in database")
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
                # Save files temporarily
                upload_dir = "./uploaded_docs"
                os.makedirs(upload_dir, exist_ok=True)
                
                saved_files = []
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(upload_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    saved_files.append(file_path)
                
                # Process and upload to vector store
                result = upload_pdfs_to_vectorstore(saved_files)
                
                st.sidebar.success(f"✅ Successfully processed {len(uploaded_files)} PDF file(s)")
                st.sidebar.write("Files processed:")
                for fname in [f.name for f in uploaded_files]:
                    st.sidebar.write(f"  • {fname}")
                
                # Clear the uploader and refresh
                st.rerun()
                
            except Exception as e:
                st.sidebar.error(f"Error uploading files: {str(e)}")
