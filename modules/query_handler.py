import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from modules.llm import get_llm_chain
from langchain.schema import BaseRetriever
from pydantic import Field
from typing import List, Optional

load_dotenv()

class SimpleRetriever(BaseRetriever):
    tags: Optional[List[str]] = Field(default_factory=list)
    metadata: Optional[dict] = Field(default_factory=dict)

    def __init__(self, documents: List[Document]):
        super().__init__()
        self._docs = documents

    def _get_relevant_documents(self, query: str) -> List[Document]:
        return self._docs

def ask_question(question: str):
    """Process a question and return answer with sources"""
    try:
        print(f"🔍 User query: {question}")
        
        # Initialize Pinecone
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index(os.getenv("PINECONE_INDEX_NAME", "babybot-medical-index"))
        
        # Initialize embeddings
        embed_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Embed the query
        embedded_query = embed_model.embed_query(question)
        
        # Query Pinecone with higher top_k for multi-document coverage
        res = index.query(vector=embedded_query, top_k=20, include_metadata=True)
        
        print(f"📊 Retrieved {len(res['matches'])} chunks from Pinecone")
        
        # Group chunks by source document
        chunks_by_source = {}
        for match in res["matches"]:
            text = match["metadata"].get("text", "").strip()
            if text:
                source = match["metadata"].get("source", "unknown")
                if source not in chunks_by_source:
                    chunks_by_source[source] = []
                chunks_by_source[source].append({
                    "text": text,
                    "metadata": match["metadata"],
                    "score": match.get("score", 0)
                })
        
        print(f"📁 Found chunks from {len(chunks_by_source)} different documents: {list(chunks_by_source.keys())}")
        
        # Build documents with clear source separation
        docs = []
        chunks_per_doc = max(3, 10 // len(chunks_by_source)) if chunks_by_source else 10
        
        for source, chunks in chunks_by_source.items():
            # Sort chunks by relevance score
            chunks.sort(key=lambda x: x["score"], reverse=True)
            
            # Add header to identify source
            source_filename = source.split('/')[-1] if '/' in source else source
            header_doc = Document(
                page_content=f"\n{'='*60}\n📄 RESUME SOURCE: {source_filename}\n{'='*60}\n",
                metadata={"source": source, "type": "header"}
            )
            docs.append(header_doc)
            
            # Add top chunks from this resume
            for chunk in chunks[:chunks_per_doc]:
                docs.append(Document(
                    page_content=chunk["text"],
                    metadata=chunk["metadata"]
                ))
        
        print(f"✅ Using {len(docs)} documents from {len(chunks_by_source)} source file(s)")
        
        if not docs:
            return {
                "response": "I couldn't find any relevant information in the uploaded documents.",
                "sources": []
            }
        
        # Create retriever and get LLM chain
        retriever = SimpleRetriever(docs)
        chain = get_llm_chain(retriever)
        
        # Get answer
        result = chain.invoke({"query": question})
        
        # Extract sources
        source_docs = result.get("source_documents", [])
        sources = list(set([
            doc.metadata.get("source", "Unknown") 
            for doc in source_docs 
            if doc.metadata.get("type") != "header"
        ]))
        
        return {
            "response": result["result"],
            "sources": sources
        }
        
    except Exception as e:
        print(f"❌ Error processing question: {str(e)}")
        raise e
