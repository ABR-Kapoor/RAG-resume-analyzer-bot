import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
import streamlit as st

load_dotenv()

def get_embeddings():
    """Initialize HuggingFace embeddings"""
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

def get_pinecone_index():
    """Initialize and return Pinecone index"""
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX_NAME", "babybot-medical-index")
    
    # Create index if it doesn't exist
    existing_indexes = [index['name'] for index in pc.list_indexes()]
    
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=384,  # all-MiniLM-L6-v2 dimension
            metric="dotproduct",
            spec=ServerlessSpec(
                cloud="aws",
                region=os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
            )
        )
    
    return pc.Index(index_name)

def upload_pdfs_to_vectorstore(file_paths):
    """Process PDFs and upload to Pinecone"""
    embed_model = get_embeddings()
    index = get_pinecone_index()
    
    all_texts = []
    all_metadatas = []
    
    for file_path in file_paths:
        # Load PDF
        loader = PyPDFLoader(file_path)
        docs = loader.load()
        
        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = text_splitter.split_documents(docs)
        
        # Prepare texts and metadata
        for chunk in chunks:
            all_texts.append(chunk.page_content)
            all_metadatas.append({
                "source": file_path,
                "text": chunk.page_content,
                "page": chunk.metadata.get("page", 0)
            })
        
        print(f"📄 Processed {os.path.basename(file_path)}: {len(chunks)} chunks")
    
    # Generate embeddings
    print(f"🔢 Generating embeddings for {len(all_texts)} chunks...")
    embeddings = embed_model.embed_documents(all_texts)
    
    # Prepare vectors for Pinecone
    vectors = []
    for i, (embedding, metadata) in enumerate(zip(embeddings, all_metadatas)):
        vectors.append({
            "id": f"doc_{i}_{hash(metadata['source'])}",
            "values": embedding,
            "metadata": metadata
        })
    
    # Upload to Pinecone in batches
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)
    
    print(f"✅ Successfully uploaded {len(file_paths)} file(s) with {len(all_texts)} total chunks to Pinecone")
    
    return {
        "files_count": len(file_paths),
        "total_chunks": len(all_texts)
    }
